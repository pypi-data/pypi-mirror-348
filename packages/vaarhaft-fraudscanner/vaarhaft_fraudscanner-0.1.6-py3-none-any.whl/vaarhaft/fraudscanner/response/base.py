"""
Base response class for the Vaarhaft FraudScanner API.

This module contains the base response class for the Vaarhaft FraudScanner API.
"""

from typing import Dict, Any, Optional, Union, Tuple

from vaarhaft.fraudscanner.response.enums import ItemType, SuspicionLevel
from vaarhaft.fraudscanner.response.models import (
    FraudScannerJsonResults,
    ItemIdTuple,
    ResultItem,
)


class FraudScannerResponse:
    """
    Response from the FraudScanner API.
    
    This class wraps the JSON response from the FraudScanner API and provides
    convenient access to the response data.
    """

    def __init__(
        self, 
        json_data: Dict[str, Any], 
        attachments: Optional[Dict[str, str]] = None, 
        status_code: Optional[int] = None, 
        duration: Optional[float] = None
    ) -> None:
        """
        Initialize the response with JSON data and attachments.
        
        :param json_data: The JSON data from the response.
        :param attachments: A dictionary mapping filenames to their paths on disk.
        :param status_code: The HTTP status code of the response.
        :param duration: The duration of the request in seconds.
        """
        self._json_data = json_data
        self._attachments = attachments or {}
        self._results = None
        self._status_code = status_code
        self._duration = duration

    @property
    def raw_json(self) -> Dict[str, Any]:
        """
        Get the raw JSON data from the response.
        
        :returns: The raw JSON data.
        """
        return self._json_data

    @property
    def results(self) -> FraudScannerJsonResults:
        """
        Get the parsed pydantic model from the response.
        
        :returns: The parsed response model.
        """
        if self._results is None:
            self._results = FraudScannerJsonResults.model_validate(self._json_data)
        return self._results

    @property
    def attachments(self) -> Dict[str, str]:
        """
        Get information about the attachments in the response.
        
        :returns: A dictionary mapping filenames to their paths on disk.
        """
        return self._attachments

    @property
    def status_code(self) -> Optional[int]:
        """
        Get the HTTP status code of the response.
        
        :returns: The HTTP status code.
        """
        return self._status_code

    @property
    def duration(self) -> Optional[float]:
        """
        Get the duration of the request in seconds.
        
        :returns: The duration in seconds.
        """
        return self._duration

    # Direct access to fields from the results model
    @property
    def Files(self) -> Dict[str, Any]:
        """
        Get the files from the response.
        
        :returns: A dictionary of filename to file result pairs.
        """
        return self.results.Files.items()
    
    @property
    def Files_dict(self) -> Dict[str, Any]:
        """
        Get the files from the response as a dictionary.
        
        :returns: A dictionary of filename to file result pairs.
        """
        return self.results.Files

    @property
    def suspicion_level(self) -> SuspicionLevel:
        """
        Get the overall suspicion level of the request.
        
        :returns: The suspicion level.
        """
        return self.results.suspicion_level

    @property
    def caseNumber(self) -> str:
        """
        Get the case number for the analysis.
        
        :returns: The case number.
        """
        return self.results.caseNumber

    @property
    def sessionId(self) -> str:
        """
        Get the session ID for the request.
        
        :returns: The session ID.
        """
        return self.results.sessionId

    @property
    def modelVersions(self) -> Dict[str, str]:
        """
        Get the versions of the models used for analysis.
        
        :returns: A dictionary of model names to version strings.
        """
        return self.results.modelVersions
    
    def get_all_items(self, type: Optional[Union[ItemType, str]] = None) -> Dict[ItemIdTuple, ResultItem]:
        """
        Get all items from the response.
        
        :param type: Optional filter for item type.
        :returns: A dictionary mapping (filename, item_id) tuples to item results.
        """
        return self.results.get_all_items(type).items()

    def get_all_items_dict(self, type: Optional[Union[ItemType, str]] = None) -> Dict[ItemIdTuple, ResultItem]:
        """
        Get all items from the response as a dictionary.
        
        :param type: Optional filter for item type.
        :returns: A dictionary mapping (filename, item_id) tuples to item results.
        """
        return self.results.get_all_items(type)