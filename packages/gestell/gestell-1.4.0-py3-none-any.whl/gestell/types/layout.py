"""
Layout schemas for parsed document, image, audio, video, and feature elements.
"""

from typing import List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field

# Type Aliases

LayoutType = Literal[
    'document',  # Standard paginated document (e.g., PDF, Word)
    'photo',  # Single-image input (e.g., JPG, PNG)
    'audio',  # Audio file input for transcription or segmentation
    'video',  # Video file input for frame and audio-layout processing
]

# [x, y, width, height] in pixels relative to the top-left corner of the page or image
LayoutPosition = Tuple[float, float, float, float]

# Common document element types
DocumentElementType = Literal[
    'title',  # Document title
    'subtitle',  # Section subtitle
    'list',  # Bullet or numbered list
    'text',  # Regular text paragraph
    'table',  # Tabular data
    'image',  # Embedded image
    'csv',  # CSV data
]


class DocumentLayoutOutput(BaseModel):
    """
    Base parsed layout element.

    Defines the bounding box, element type, and raw content for
    a single layout element extracted from a document or image.
    """

    position: LayoutPosition = Field(
        ..., description='Bounding box [x, y, width, height] in pixels.'
    )
    type: Union[DocumentElementType, str] = Field(
        ...,
        description=(
            'Element kind. One of:\n'
            "- 'title', 'subtitle', 'list', 'text', 'table', 'image', 'csv'\n"
            '- or a custom string label'
        ),
    )
    content: str = Field(..., description='Raw text or data content of this element.')


class DocumentLayout(DocumentLayoutOutput):
    """
    Parsed layout element with ordering and pagination metadata.

    Extends DocumentLayoutOutput by adding the element's index
    in the document flow and the 1-based page number.
    """

    index: int = Field(
        ..., ge=0, description='Zero-based index of this element in the document flow.'
    )
    page: int = Field(
        ..., ge=1, description='One-based page number where this element appears.'
    )


class AudioLayout(BaseModel):
    """
    Parsed segment from an audio file.

    Represents a single segment with time codes, speaker info,
    descriptive context, and transcription.
    """

    index: int = Field(..., ge=0, description='Zero-based segment index.')
    start: str = Field(..., description="Segment start time (ISO 8601 or 'HH:MM:SS').")
    end: str = Field(..., description="Segment end time (ISO 8601 or 'HH:MM:SS').")
    narrator: str = Field(..., description='Identifier of the speaker or narrator.')
    description: str = Field(
        ..., description='Non-verbal context or description for this segment.'
    )
    content: str = Field(..., description='Transcribed text of the audio segment.')


class PhotoLayout(BaseModel):
    """
    Parsed region from a single image.

    Defines a bounding box and an optional descriptive label
    for a detected region in a photo.
    """

    position: LayoutPosition = Field(
        ..., description='Bounding box [x, y, width, height] in pixels.'
    )
    description: str = Field(
        ..., description='Description of the visual content (objects or scene).'
    )
    type: Optional[str] = Field(
        None, description='Optional detected label for this region.'
    )


class VideoLayout(BaseModel):
    """
    Parsed segment from a video file.

    Combines timestamped audio transcription, narration text,
    speaker info, and detected visual regions.
    """

    index: int = Field(..., ge=0, description='Zero-based segment index.')
    start: str = Field(..., description="Segment start time (ISO 8601 or 'HH:MM:SS').")
    end: str = Field(..., description="Segment end time (ISO 8601 or 'HH:MM:SS').")
    audio: str = Field(..., description='Extracted or transcribed audio content.')
    narration: str = Field(
        ..., description='Narration or descriptive text for this segment.'
    )
    narrator: str = Field(..., description='Identifier of the speaker or narrator.')
    objects: List[PhotoLayout] = Field(
        default_factory=list,
        description='Detected visual regions within the video frame.',
    )


class FeatureLayout(BaseModel):
    """
    Layout for discrete feature annotations.

    Used for point-based or key-value feature extraction
    (e.g., landmarks, form fields).
    """

    position: List[float] = Field(
        ..., description='Coordinates or numeric values representing the feature.'
    )
    label: str = Field(..., description='Identifier label for the feature.')
    description: str = Field(
        ..., description='Additional metadata or explanation for the feature.'
    )
