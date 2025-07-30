"""
Client for the Vaarhaft FraudScanner API.

This module contains the client for interacting with the Vaarhaft FraudScanner API.
"""

import os
from os import PathLike
from typing import Optional, Union

from vaarhaft.fraudscanner.request import FraudScannerRequest, RequestHeaders
from vaarhaft.fraudscanner.response.base import FraudScannerResponse


class FraudScannerClient:
    """
    Client for the FraudScanner API that can be used as an async context manager.
    
    This class provides a convenient interface for sending requests to the FraudScanner API.
    It can be used as an async context manager to ensure proper resource cleanup.
    
    Example:
        .. code-block:: python
        
            async with FraudScannerClient(api_key="your_api_key") as client:
                response = await client.send(
                    case_number="1234567",
                    issue_date="2023-10-01",
                    file_path="/path/to/file.zip",
                )
    """

    def __init__(self, api_key: str, attachments_output_dir: Optional[str] = None) -> None:
        """
        Initialize the client with an API key and an optional output directory.
        
        :param api_key: The API key for authenticating with the FraudScanner API.
        :param attachments_output_dir: Optional directory to save attachments to. If not provided, attachments will not be saved.
        """
        self.api_key = api_key
        self.output_dir = attachments_output_dir

    async def __aenter__(self) -> "FraudScannerClient":
        """
        Enter the async context manager.
        
        Creates the output directory if it doesn't exist.
        
        :returns: The client instance.
        """
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the async context manager.
        
        :param exc_type: The exception type, if an exception was raised.
        :param exc_val: The exception value, if an exception was raised.
        :param exc_tb: The exception traceback, if an exception was raised.
        """
        pass

    async def send(
        self, 
        case_number: str, 
        file_path: Optional[Union[str, PathLike[str]]], 
        issue_date: Optional[str] = None,
        contact_email: Optional[str] = None
    ) -> FraudScannerResponse:
        """
        Send a request to the FraudScanner API.
        
        :param case_number: The case number for the request.
        :param file_path: Optional path to the file to be scanned. If not provided, no file will be sent.
        :param issue_date: Optional issue date for the request.
        :param contact_email: Optional contact email for the request.
        :returns: The response from the FraudScanner API.
        """
        headers = RequestHeaders(
            api_key=self.api_key,
            case_number=case_number,
            issue_date=issue_date,
            contact_email=contact_email
        )

        # Create a request with headers, optional file_path, and output_dir
        request = FraudScannerRequest(headers=headers, file_path=file_path, output_dir=self.output_dir)

        return await request.send()