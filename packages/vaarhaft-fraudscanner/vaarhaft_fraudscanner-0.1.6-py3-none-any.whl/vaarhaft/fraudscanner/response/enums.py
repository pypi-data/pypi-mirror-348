"""
Enums for the Vaarhaft FraudScanner API.

This module contains enum classes used in the FraudScanner API responses.
"""

import enum
from typing import List


class DetectionClass(str, enum.Enum):
    """
    Enum for the detection classes.
    
    :cvar NONE: No detection class assigned.
    :cvar REAL: The item is detected as real.
    :cvar TAMPERED: The item is detected as tampered.
    :cvar GENERATED: The item is detected as generated.
    """

    NONE = "-"
    REAL = "real"
    TAMPERED = "tp"
    GENERATED = "gen"


class SuspicionLevel(str, enum.Enum):
    """
    Enum for the suspicion level of an item, file, or request.
    
    :cvar GREEN: Low suspicion level.
    :cvar YELLOW: Medium suspicion level.
    :cvar RED: High suspicion level.
    """

    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"


class ItemType(str, enum.Enum):
    """
    Enum for the type of an item.
    
    :cvar UNKNOWN: Unknown item type.
    :cvar IMAGE: Image item type.
    :cvar DOCUMENT: Document item type.
    """

    UNKNOWN = "unknown"
    IMAGE = "image"
    DOCUMENT = "document"


class FileType(str, enum.Enum):
    """
    Enum for the type of a file.
    
    :cvar UNKNOWN: Unknown file type.
    :cvar PDF: PDF file type.
    :cvar PNG: PNG image file type.
    :cvar JPEG: JPEG image file type.
    :cvar TIFF: TIFF image file type.
    :cvar WEBP: WEBP image file type.
    :cvar HEIC: HEIC container file type.
    """

    UNKNOWN = "N/A"
    PDF = "PDF"
    PNG = "PNG (image file)"
    JPEG = "JPEG (image file)"
    TIFF = "TIFF (image file)"
    WEBP = "WEBP (image file)"
    HEIC = "HEIC (container file)"