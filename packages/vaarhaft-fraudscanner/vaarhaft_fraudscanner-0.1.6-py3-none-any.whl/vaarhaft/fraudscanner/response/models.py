"""
Response models for the Vaarhaft FraudScanner API.

This module contains the Pydantic models for the FraudScanner API responses.
"""

from typing import Annotated, Any, Dict, List, NamedTuple, Optional, Tuple, Union

from pydantic import BaseModel, Field

from vaarhaft.fraudscanner.response.enums import (
    DetectionClass,
    FileType,
    ItemType,
    SuspicionLevel,
)


class ItemIdTuple(NamedTuple):
    """
    Tuple for the ID of an item.
    
    Consists of the name of the file the item is from and the item UUID.
    
    :ivar file_name: The name of the file the item is from.
    :ivar item_uuid: The UUID of the item.
    """

    file_name: str
    item_uuid: str


# Feature submodels
class CreationDateSubData(BaseModel):
    """
    Submodel used for the metadata results.
    
    :ivar cDate: Creation date.
    :ivar cTime: Creation time.
    :ivar isSus: Whether the creation date/time is suspicious.
    :ivar diffInDays: Difference in days from reference date.
    :ivar isTodayUsed: Whether today's date was used.
    :ivar refDate: Reference date.
    """

    cDate: Annotated[str, Field(default="-")]  # noqa: N815
    cTime: Annotated[str, Field(default="-")]  # noqa: N815
    isSus: Annotated[bool, Field(default=False)]  # noqa: N815
    diffInDays: Annotated[int, Field(default=0)]  # noqa: N815
    isTodayUsed: Annotated[bool, Field(default=False)]  # noqa: N815
    refDate: Annotated[str, Field(default="-")]  # noqa: N815


class AnalysedSubData(BaseModel):
    """
    Submodel used for the metadata results.
    
    :ivar creationDate: Creation date information.
    :ivar imgRanking: Image ranking.
    :ivar fieldsMarkedSus: Fields marked as suspicious.
    """

    creationDate: Annotated[CreationDateSubData, Field(default_factory=CreationDateSubData)]  # noqa: N815
    imgRanking: Annotated[Optional[int], Field(default=None)]  # noqa: N815
    fieldsMarkedSus: Annotated[Dict[Any, str], Field(default_factory=dict)]  # noqa: N815


class RawSubData(BaseModel):
    """
    Submodel used for the metadata results.
    
    :ivar Rating: Rating information.
    :ivar Dates: Date information.
    :ivar GPS: GPS information.
    :ivar Other: Other metadata.
    """

    Rating: Annotated[Dict[Any, int], Field(default_factory=dict)]
    Dates: Annotated[Dict[str, str], Field(default_factory=dict)]
    GPS: Annotated[Dict[str, Any], Field(default_factory=dict)]
    Other: Annotated[List[Dict], Field(default_factory=list)]


class C2PAData(BaseModel):
    """
    Submodel for C2PA metadata extraction data.
    
    :ivar is_valid: Whether the C2PA data is valid.
    :ivar suspicious_keywords: List of suspicious keywords found.
    :ivar validation_status_base64: Base64-encoded validation status.
    :ivar manifest_base64: Base64-encoded manifest.
    """

    is_valid: Annotated[bool, Field(default=True)]
    suspicious_keywords: Annotated[List[str], Field(default_factory=list)]
    validation_status_base64: Annotated[str, Field(default="")]
    manifest_base64: Annotated[str, Field(default="")]


# Feature sections
class ImageQualityResult(BaseModel):
    """
    Results model for the image quality feature.
    
    :ivar result: The result of the image quality check.
    :ivar error: Whether an error occurred during the check.
    """

    result: Annotated[bool, Field(default=False)]
    error: Annotated[bool, Field(default=True)]


class GeneratedDetectionResult(BaseModel):
    """
    Results model for the generated detection feature.
    
    :ivar predictedClassName: The predicted class name.
    :ivar confidence: The confidence score.
    :ivar error: Whether an error occurred during detection.
    :ivar enabled: Whether the feature is enabled.
    """

    predictedClassName: Annotated[DetectionClass, Field(default=DetectionClass.NONE)]  # noqa: N815
    confidence: Annotated[float, Field(default=-1.0)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class TamperedDetectionResult(BaseModel):
    """
    Results model for the tampered detection feature.
    
    :ivar predictedClassName: The predicted class name.
    :ivar confidence: The confidence score.
    :ivar error: Whether an error occurred during detection.
    :ivar enabled: Whether the feature is enabled.
    """

    predictedClassName: Annotated[DetectionClass, Field(default=DetectionClass.NONE)]  # noqa: N815
    confidence: Annotated[float, Field(default=-1.0)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class DoubletCheckResult(BaseModel):
    """
    Base model for the doublet check feature results.
    
    :ivar result: The result of the doublet check.
    :ivar internal: Whether the check was internal.
    :ivar caseNumber: The case number for the check.
    :ivar error: Whether an error occurred during the check.
    :ivar enabled: Whether the feature is enabled.
    """

    result: Annotated[bool, Field(default=False)]
    internal: Annotated[bool, Field(default=False)]
    caseNumber: Annotated[str, Field(default="")]  # noqa: N815
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class ReverseSearchResult(BaseModel):
    """
    Base model for the reverse search feature results.
    
    :ivar matches: List of matches found.
    :ivar error: Whether an error occurred during the search.
    :ivar enabled: Whether the feature is enabled.
    """

    matches: Annotated[List[Tuple[str, float]], Field(default_factory=list)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class PhoneNumberResult(BaseModel):
    """
    Results model for the phone number detection feature.
    
    :ivar result: The result of the phone number detection.
    :ivar text: The detected phone number text.
    :ivar error: Whether an error occurred during detection.
    :ivar enabled: Whether the feature is enabled.
    """

    result: Annotated[bool, Field(default=False)]
    text: Annotated[str, Field(default="")]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class LinkResult(BaseModel):
    """
    Results model for the link detection feature.
    
    :ivar result: The result of the link detection.
    :ivar text: The detected link text.
    :ivar error: Whether an error occurred during detection.
    :ivar enabled: Whether the feature is enabled.
    """

    result: Annotated[bool, Field(default=False)]
    text: Annotated[str, Field(default="")]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class QrCodeResult(BaseModel):
    """
    Results model for the QR code detection feature.
    
    :ivar result: The result of the QR code detection.
    :ivar error: Whether an error occurred during detection.
    :ivar enabled: Whether the feature is enabled.
    """

    result: Annotated[bool, Field(default=False)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class MetadataResult(BaseModel):
    """
    Model for metadata-feature output.
    
    :ivar analysed: Analyzed metadata.
    :ivar gpsInfo: GPS information.
    :ivar raw: Raw metadata.
    :ivar error: Whether an error occurred during analysis.
    :ivar enabled: Whether the feature is enabled.
    """

    analysed: Annotated[Optional[AnalysedSubData], Field(default=None)]
    gpsInfo: Annotated[Optional[Dict[str, Any]], Field(default=None)]  # noqa
    raw: Annotated[Optional[RawSubData], Field(default=None)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


class C2paResult(BaseModel):
    """
    Model for C2PA metadata extraction results.
    
    :ivar c2pa_extracted: Whether C2PA data was extracted.
    :ivar reason: Reason for extraction result.
    :ivar data: Extracted C2PA data.
    :ivar error: Whether an error occurred during extraction.
    :ivar enabled: Whether the feature is enabled.
    """

    c2pa_extracted: Annotated[bool, Field(default=False)]
    reason: Annotated[str, Field(default="")]
    data: Annotated[Optional[C2PAData], Field(default=None)]
    error: Annotated[bool, Field(default=False)]
    enabled: Annotated[bool, Field(default=False)]


# File level analyses
class FileLevelAnalysis_PDFStructure(BaseModel):
    """
    Model for PDF structure analysis results.
    
    :ivar mod_dates: List of modification dates found in the PDF metadata.
    :ivar xmlModDate_later_infoModDate: Whether the XML modification date is later than the info modification date.
    :ivar editing_tools: List of editing tools found in the PDF metadata.
    :ivar annotation_layer_found: Whether an annotation layer was found in the PDF.
    :ivar error: Whether an error occurred during the analysis.
    """

    mod_dates: Annotated[
        List[str],
        Field(
            default_factory=list,
            description="List of modification dates found in the PDF metadata.",
        ),
    ]
    
    xmlModDate_later_infoModDate: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the XML modification date is later than the info modification date.",
        ),
    ]
    editing_tools: Annotated[
        List[str],
        Field(
            default_factory=list,
            description="List of editing tools found in the PDF metadata.",
        ),
    ]
    annotation_layer_found: Annotated[
        bool,
        Field(
            default=False,
            description="Whether an annotation layer was found in the PDF.",
        ),
    ]
    error: Annotated[
        bool,
        Field(
            default=True,
            description="Whether an error occurred during the analysis.",
        ),
    ]


class FileLevelAnalysis_PDFVersions(BaseModel):
    """
    Model for PDF version analysis results.
    
    :ivar found: Number of PDF versions found (excluding the submitted one).
    :ivar extracted: Number of old PDF versions extracted.
    :ivar error: Whether an error occurred during the analysis.
    """

    found: Annotated[
        int,
        Field(
            default=0,
            description="Number of PDF versions found (excluding the submitted one).",
        ),
    ]
    extracted: Annotated[
        int,
        Field(
            default=0,
            description="Number of old PDF versions extracted. Any extracted versions will be returned as a zip attachment.",
        ),
    ]
    error: Annotated[
        bool,
        Field(
            default=True,
            description="Whether an error occurred during the analysis.",
        ),
    ]


class PDF_FileLevelAnalyses(BaseModel):
    """
    Model for PDF file level analyses.
    
    :ivar versions: Results of the PDF file level analyses.
    :ivar structure: Results of the PDF metadata analysis.
    """

    versions: Annotated[
        Optional[FileLevelAnalysis_PDFVersions],
        Field(
            default=None,
            description="Results of the PDF file level analyses.",
        ),
    ]
    structure: Annotated[
        Optional[FileLevelAnalysis_PDFStructure],
        Field(
            default=None,
            description="Results of the PDF metadata analysis.",
        ),
    ]


class FileLevelAnalyses(BaseModel):
    """
    Model for file level analyses.
    
    :ivar pdf_analyses: Results of the file-level analyses.
    """

    pdf_analyses: Annotated[
        Optional[PDF_FileLevelAnalyses],
        Field(
            default=None,
            description="Results of the file-level analyses.",
        ),
    ]


# Item analyses
class ImageAnalysesResults(BaseModel):
    """
    Model for image analyses results.
    
    :ivar imageQuality: Results of the image quality check.
    :ivar metadata: Results of the metadata analysis.
    :ivar c2pa: Results of the C2PA extraction.
    :ivar doubletCheck: Results of the doublet check.
    :ivar reverseSearch: Results of the reverse image search.
    :ivar generatedDetection: Results of the generation detection.
    :ivar tamperedDetection: Results of the tampering detection.
    :ivar phoneNumber: Results of the phone number detection.
    :ivar qrCode: Results of the QR code detection.
    :ivar link: Results of the link detection.
    """

    imageQuality: Annotated[  # noqa
        ImageQualityResult,
        Field(
            default_factory=ImageQualityResult,
            description="Results of the image quality check",
        ),
    ]
    metadata: Annotated[
        MetadataResult,
        Field(
            default_factory=MetadataResult,
            description="Results of the metadata analysis",
        ),
    ]
    c2pa: Annotated[
        C2paResult,
        Field(
            default_factory=C2paResult,
            description="Results of the C2PA extraction",
        ),
    ]
    doubletCheck: Annotated[  # noqa
        DoubletCheckResult,
        Field(
            default_factory=DoubletCheckResult,
            description="Results of the doublet check",
        ),
    ]
    reverseSearch: Annotated[  # noqa
        ReverseSearchResult,
        Field(
            default_factory=ReverseSearchResult,
            description="Results of the reverse image search",
        ),
    ]
    generatedDetection: Annotated[  # noqa
        GeneratedDetectionResult,
        Field(
            default_factory=GeneratedDetectionResult,
            description="Results of the generation detection",
        ),
    ]
    tamperedDetection: Annotated[  # noqa
        TamperedDetectionResult,
        Field(
            default_factory=TamperedDetectionResult,
            description="Results of the tampering detection",
        ),
    ]
    phoneNumber: Annotated[  # noqa
        PhoneNumberResult,
        Field(
            default_factory=PhoneNumberResult,
            description="Results of the phone number detection",
        ),
    ]
    qrCode: Annotated[  # noqa
        QrCodeResult,
        Field(
            default_factory=QrCodeResult,
            description="Results of the QR code detection",
        ),
    ]
    link: Annotated[
        LinkResult,
        Field(
            default_factory=LinkResult,
            description="Results of the link detection",
        ),
    ]


class DocumentAnalysesResults(BaseModel):
    """
    Class that aggregates the results of different analyses for a document item.
    
    :ivar tamperedDetection: Results of the tampered detection.
    """

    tamperedDetection: Annotated[  # noqa
        TamperedDetectionResult,
        Field(
            default_factory=TamperedDetectionResult,
            description="Results of the tampered detection",
        ),
    ]


class ResultItem(BaseModel):
    """
    A single item's analysis results.
    
    :ivar id: ID of the item.
    :ivar item_type: Type of the item.
    :ivar position: Position of the item in the file, if applicable.
    :ivar suspicion_level: Suspicion level of the item.
    :ivar analyses: Results of the different analysis features.
    """

    id: Annotated[
        str,
        Field(
            description="ID of the item",
        ),
    ]
    item_type: Annotated[
        ItemType,
        Field(
            description="Type of the item",
        ),
    ]
    position: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Position of the item in the file, if applicable (e.g. the page of the given PDF document that the item was extracted from).",
        ),
    ]
    suspicion_level: Annotated[
        SuspicionLevel,
        Field(
            default=SuspicionLevel.GREEN,
            description="Suspicion level of the item, oriented on a traffic light system (green/yellow/red)",
        ),
    ]
    analyses: Annotated[
        Union[ImageAnalysesResults, DocumentAnalysesResults],
        Field(
            default=None,
            description="Results of the different analysis features, depending on the item type",
        ),
    ]


# File result
class FileResult(BaseModel):
    """
    Results for a file (which may contain multiple items).
    
    :ivar file_type: Type of the file.
    :ivar suspicion_level: Suspicion level of the file.
    :ivar file_level_analyses: Results of the file-level analysis.
    :ivar items: Dictionary of items in the file.
    """

    file_type: Annotated[
        FileType,
        Field(
            default=FileType.UNKNOWN,
            description="Type of the file",
        ),
    ]
    suspicion_level: Annotated[
        SuspicionLevel,
        Field(
            default=SuspicionLevel.GREEN,
            description="Suspicion level of the file, based on the suspicion level of the contained items",
        ),
    ]
    file_level_analyses: Annotated[
        Optional[FileLevelAnalyses],
        Field(
            default=None,
            description="Results of the file-level analysis (only available for certain file types, e.g. PDF)",
        ),
    ]
    items: Annotated[
        List[ResultItem],
        Field(
            default_factory=list,
            description="Dictionary of items in the file (uuid -> ResultItem)",
        ),
    ]


# Response model
class FraudScannerJsonResults(BaseModel):
    """
    Class that aggregates the results of processing multiple files.
    
    :ivar suspicion_level: Overall suspicion level of the request.
    :ivar Files: Dictionary/mapping of filenames to corresponding results.
    :ivar caseNumber: Case number for the analysis.
    :ivar sessionId: Session ID for the request.
    :ivar modelVersions: Versions of the models used for analysis.
    """

    suspicion_level: Annotated[
        SuspicionLevel,
        Field(
            default=SuspicionLevel.GREEN,
            description="Overall suspicion level of the request, based on the suspicion levels of the submitted files. Follows a traffic light system: Green, Yellow, Red.",
        ),
    ]
    Files: Annotated[
        Dict[str, FileResult],
        Field(
            default_factory=dict,
            description="Dictionary/mapping of filenames to corresponding results.",
        ),
    ]
    caseNumber: Annotated[  # noqa: N815
        str,
        Field(
            description="Case number for the analysis.",
        ),
    ]
    sessionId: Annotated[  # noqa: N815
        str,
        Field(
            description="Session ID for the request.",
        ),
    ]
    modelVersions: Annotated[  # noqa: N815
        Dict[str, str],
        Field(
            description="Versions of the models used for analysis.",
        ),
    ]

    def get_all_items(self, type: Optional[Union[ItemType, str]] = None) -> Dict[ItemIdTuple, ResultItem]:
        """
        Get all items from the response.
        
        :param type: Optional filter for item type.
        :return: Dictionary of items (filename, item_uuid) -> ResultItem.
        """
        items = {}
        if type is not None and isinstance(type, str):
            try:
                type = ItemType(type)
            except ValueError:
                raise ValueError(f"Invalid item type: {type}. Must be one of {list(ItemType)}.")
        for file_name, file_result in self.Files.items():
            for item in file_result.items:
                if type is None or item.item_type == type:
                    items[ItemIdTuple(file_name=file_name, item_uuid=item.id)] = item
        return items