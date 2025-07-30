"""
Schemas and type‐aliases for Gestell collections, categories, and PII controls.
"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

# Type Aliases
CollectionType = Literal[
    'frame',  # OCR outputs only
    'searchable-frame',  # Lighter search‐optimized version
    'canon',  # Full canonized dataset
    'features',  # Feature‐extraction mode
]

PiiType = Literal[
    'generic',  # Standard personal data
    'legal',  # Legal or regulatory context
    'medical',  # Protected health information
]

CategoryType = Literal[
    'content',  # Filter content by instructions
    'concepts',  # Conceptual summaries
    'features',  # Label extraction
    'table',  # Tabular data
]

PiiIdentifierOption = Literal[
    'Name',
    'Geographic Data',
    'Dates',
    'Phone Number',
    'Fax Number',
    'Email Address',
    'Social Security Number',
    'Medical Record Number',
    'Health Plan Beneficiary Number',
    'Account Number',
    'Certificate/License Number',
    'Vehicle Identifier',
    'Device Identifier',
    'Web URL',
    'IP Address',
    'Biometric Identifier',
    'Full-face Photograph',
    'Unique Identifier Code',
]

PII_IDENTIFIER_OPTIONS: List[PiiIdentifierOption] = [
    # List of allowed PII identifiers
    'Name',
    'Geographic Data',
    'Dates',
    'Phone Number',
    'Fax Number',
    'Email Address',
    'Social Security Number',
    'Medical Record Number',
    'Health Plan Beneficiary Number',
    'Account Number',
    'Certificate/License Number',
    'Vehicle Identifier',
    'Device Identifier',
    'Web URL',
    'IP Address',
    'Biometric Identifier',
    'Full-face Photograph',
    'Unique Identifier Code',
]


class Category(BaseModel):
    """
    A named grouping within a collection, with instructions and entry rules.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Unique category identifier.')
    collection_id: str = Field(
        ..., alias='collectionId', description='Parent collection identifier.'
    )
    name: str = Field(..., description='Display name.')
    type: CategoryType = Field(..., description='One of the defined category types.')
    instructions: str = Field(..., description='Markdown‐friendly instructions.')
    single_entry: bool = Field(
        ...,
        alias='singleEntry',
        description='If true, only one entry per document is allowed.',
    )
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last‐updated timestamp.'
    )

    @field_serializer('date_created', mode='plain')
    def _ser_date_created(self, dt: datetime, _info):
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _ser_date_updated(self, dt: datetime, _info):
        return dt.isoformat()


class CreateCategoryPayload(BaseModel):
    """
    Data required to create a new category.
    """

    name: str = Field(..., description='Category display name.')
    type: CategoryType = Field(..., description='Category type.')
    instructions: str = Field(
        ..., description='Markdown instructions for category behavior.'
    )
    single_entry: Optional[bool] = Field(
        False,
        alias='singleEntry',
        description='If true, only one entry per document is allowed.',
    )


class Collection(BaseModel):
    """
    Represents a document collection and its configuration.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Unique collection identifier.')
    organization_id: str = Field(
        ..., alias='organizationId', description='Parent organization identifier.'
    )
    name: str = Field(..., description='Collection display name.')
    type: CollectionType = Field(
        ..., description='One of the defined collection types.'
    )
    description: str = Field(..., description='Purpose or summary.')
    pii: bool = Field(..., description='Whether collection contains PII.')
    pii_type: PiiType = Field(
        ..., alias='piiType', description='Type of PII contained.'
    )
    pii_controls: List[PiiIdentifierOption] = Field(
        ..., alias='piiControls', description='Controls for PII handling in UI.'
    )
    tags: List[str] = Field(..., description='Search/filter tags.')
    instructions: str = Field(..., description='General usage instructions.')
    graph_instructions: str = Field(
        ..., alias='graphInstructions', description='Graph‐specific instructions.'
    )
    prompt_instructions: str = Field(
        ..., alias='promptInstructions', description='Prompt‐based instructions.'
    )
    search_instructions: str = Field(
        ..., alias='searchInstructions', description='Search operation instructions.'
    )

    organization: Optional[dict] = Field(
        None, description='Populated when fetching collection details.'
    )
    categories: Optional[List[Category]] = Field(
        None, description='Category list when in extended view.'
    )
    documents: Optional[List[dict]] = Field(
        None, description='Document list when in extended view.'
    )

    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last‐updated timestamp.'
    )

    @field_serializer('date_created', mode='plain')
    def _ser_date_created(self, dt: datetime, _info):
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _ser_date_updated(self, dt: datetime, _info):
        return dt.isoformat()


class CollectionStats(BaseModel):
    """
    Aggregate statistics for a collection's content and processing.
    """

    docs: int = Field(..., description='Total number of indexed documents.')
    size: int = Field(..., description='Total storage size in bytes.')
    nodes: int = Field(..., description='Total number of graph nodes.')

    class Status(BaseModel):
        """
        Breakdown of processing counts by stage.
        """

        documents: int = Field(..., description='Processed document count.')
        nodes: int = Field(..., description='Processed node count.')
        edges: int = Field(..., description='Processed edge count.')
        vectors: int = Field(..., description='Generated vector count.')
        category: int = Field(..., description='Processed category count.')

    status: Status = Field(..., description='Per-stage processing counts.')
