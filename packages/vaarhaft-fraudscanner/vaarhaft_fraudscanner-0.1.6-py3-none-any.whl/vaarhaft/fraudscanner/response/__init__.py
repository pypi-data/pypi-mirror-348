"""
Response models for the Vaarhaft FraudScanner API.

This module contains the response models for the Vaarhaft FraudScanner API.
"""

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