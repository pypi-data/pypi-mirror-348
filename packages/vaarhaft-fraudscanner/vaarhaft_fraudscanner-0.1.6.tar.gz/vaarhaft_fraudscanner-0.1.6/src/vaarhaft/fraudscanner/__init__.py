"""
Vaarhaft FraudScanner SDK.

This module provides a client for interacting with the Vaarhaft FraudScanner API.
"""

from vaarhaft.fraudscanner.client import FraudScannerClient
from vaarhaft.fraudscanner.request import FraudScannerRequest, RequestHeaders
from vaarhaft.fraudscanner.response.base import FraudScannerResponse
from vaarhaft.fraudscanner.response.enums import (
    DetectionClass,
    FileType,
    ItemType,
    SuspicionLevel,
)
from vaarhaft.fraudscanner.response.models import (
    FraudScannerJsonResults,
    FileResult,
    ItemIdTuple,
    ResultItem,
)

__all__ = [
    "FraudScannerClient",
    "FraudScannerRequest",
    "RequestHeaders",
    "FraudScannerResponse",
    "FraudScannerJsonResults",
    "FileResult",
    "ItemIdTuple",
    "ResultItem",
    "DetectionClass",
    "FileType",
    "ItemType",
    "SuspicionLevel",
]