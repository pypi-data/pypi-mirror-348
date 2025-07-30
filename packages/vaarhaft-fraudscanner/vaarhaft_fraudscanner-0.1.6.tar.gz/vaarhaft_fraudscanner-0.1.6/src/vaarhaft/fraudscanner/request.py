"""
Request classes for the Vaarhaft FraudScanner API.

This module contains the request classes for the Vaarhaft FraudScanner API.
"""

import dataclasses
import datetime
import os
import re
import uuid
from os import PathLike
from typing import Optional, Union

import aiofiles
import aiohttp

from vaarhaft.fraudscanner.config import FS_ENDPOINT
from vaarhaft.fraudscanner.response.base import FraudScannerResponse


@dataclasses.dataclass
class RequestHeaders:
    """
    The model for the request headers.
    
    :ivar api_key: The API key for authenticating with the FraudScanner API.
    :ivar case_number: The case number for the request.
    :ivar issue_date: Optional issue date for the request.
    :ivar contact_email: Optional contact email for the request.
    """

    api_key: str
    case_number: str
    issue_date: Optional[str] = None
    contact_email: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Validate the headers after initialization.
        
        :raises ValueError: If the headers are invalid.
        """
        # Validate the headers
        if not self.api_key or not self.case_number:
            raise ValueError("Could not create request: API key and CaseNumber not given.")
        if len(self.api_key) != 40:
            raise ValueError("Could not create request: API key has to be exactly 40 characters long. If you don't have an API key yet, "
                             "please contact VAARHAFT.")
        if len(self.case_number) < 4 or len(self.case_number) > 35:
            raise ValueError("Could not create request: CaseNumber has to be between 4 and 35 characters long.")
        if self.contact_email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.contact_email):
                raise ValueError("Could not create request: The provided contact email is not a valid email address.")


class FraudScannerRequest:
    """
    The model for the request to the fraud scanner.
    
    This class handles creating and sending requests to the FraudScanner API.
    """

    def __init__(self, headers: RequestHeaders, file_path: Optional[Union[str, PathLike[str]]], output_dir: Optional[str] = None) -> None:
        """
        Initialize the request with headers and an optional file path.
        
        :param headers: The headers for the request.
        :param file_path: Optional path to the file to be scanned.
        :param output_dir: Optional directory to save attachments to.
        """
        self.headers = headers
        self.file_path = file_path
        self.output_dir = output_dir
        self.request_timestamp = datetime.datetime.now()

    @staticmethod
    def sanitize_directory_name(name: str) -> str:
        """
        Sanitize a string to be used as a directory name across Windows, Linux, and macOS.
        
        :param name: The string to sanitize.
        :returns: A sanitized string that can be used as a directory name.
        """
        # Replace characters that are invalid in Windows filenames
        # Windows is the most restrictive, so we'll use its rules
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(invalid_chars, '_', name)

        # Remove leading/trailing spaces and dots (problematic in Windows)
        sanitized = sanitized.strip('. ')

        # Ensure the name is not empty or just dots/spaces
        if not sanitized or sanitized.isspace():
            sanitized = "unnamed"

        return sanitized

    def get_timestamp_string(self) -> str:
        """
        Get a formatted timestamp string for the current request.
        
        :returns: A timestamp string in the format YYYY-MM-DD HH:mm:SS
        """
        return self.request_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    async def send(self) -> FraudScannerResponse:
        """
        Send the request to the FraudScanner API.
        
        :returns: The response from the FraudScanner API.
        :raises aiohttp.ClientResponseError: If the API returns an error response.
        """
        request_headers = {
            "x-api-key": self.headers.api_key,
            "caseNumber": self.headers.case_number,
        }
        # Have to set optionals separately so they don't exist at all if not set
        if self.headers.issue_date:
            request_headers["issueDate"] = self.headers.issue_date
        if self.headers.contact_email:
            request_headers["contactEmail"] = self.headers.contact_email

        data = None
        if self.file_path:
            async with aiofiles.open(self.file_path, "rb") as f:
                file_data = await f.read()
                filename = os.path.basename(self.file_path)
                data = aiohttp.FormData()
                data.add_field('file', file_data, filename=filename, content_type="application/zip")

        # Record the start time
        start_time = datetime.datetime.now()

        async with aiohttp.ClientSession() as session:
            async with session.post(FS_ENDPOINT, data=data, headers=request_headers) as response:
                response.raise_for_status()
                # Calculate the duration
                duration = (datetime.datetime.now() - start_time).total_seconds()
                return await self._handle_response(response, duration)

    async def _handle_response(self, response: aiohttp.ClientResponse, duration: Optional[float] = None) -> FraudScannerResponse:
        """
        Handle the response from the FraudScanner API.
        
        :param response: The response from the FraudScanner API.
        :param duration: The duration of the request in seconds.
        :returns: The processed response.
        :raises ValueError: If the response format is unexpected.
        """
        content_type = response.headers.get("Content-Type", "")
        status_code = response.status

        if content_type.startswith("application/json"):
            # JSON response
            json_data = await response.json()
            return FraudScannerResponse(json_data=json_data, status_code=status_code, duration=duration)
        elif content_type.startswith("multipart/"):
            # Multipart response
            multipart = aiohttp.MultipartReader.from_response(response)
            json_data = {}
            attachments = {}

            async for part in multipart:
                # Identify the part by content type, name, or headers as needed
                part_headers = dict(part.headers)
                if part_headers.get("Content-Type") == "application/json":
                    json_data = await part.json()
                elif part_headers.get("Content-Type") == "application/zip":
                    # Save the zip file to the output directory if provided
                    zip_bytes = await part.read()
                    if self.output_dir:
                        # Get the filename from the Content-Disposition header if available
                        content_disposition = part_headers.get("Content-Disposition", "")
                        filename = None
                        if content_disposition:
                            # Extract filename from Content-Disposition header
                            match = re.search(r'filename="?([^"]+)"?', content_disposition)
                            if match:
                                filename = match.group(1)

                        # If no filename in header, generate a unique one
                        if not filename:
                            filename = f"attachment_{uuid.uuid4()}.zip"

                        # Create directory structure: output_dir/sanitized_case_number/timestamp/
                        sanitized_case_number = self.sanitize_directory_name(self.headers.case_number)
                        timestamp_str = self.get_timestamp_string()

                        # Create case number directory
                        case_dir = os.path.join(self.output_dir, sanitized_case_number)
                        if not os.path.exists(case_dir):
                            os.makedirs(case_dir)

                        # Create timestamp directory
                        timestamp_dir = os.path.join(case_dir, timestamp_str)
                        if not os.path.exists(timestamp_dir):
                            os.makedirs(timestamp_dir)

                        # Save the file to the timestamp directory
                        file_path = os.path.join(timestamp_dir, filename)
                        async with aiofiles.open(file_path, "wb") as f:
                            await f.write(zip_bytes)

                        # Add to attachments dictionary
                        attachments[filename] = file_path
                else:
                    # Handle other parts as needed
                    pass

            return FraudScannerResponse(json_data=json_data, attachments=attachments, status_code=status_code, duration=duration)
        else:
            raise ValueError(f"Received unexpected response format from the FraudScanner API: {content_type}")