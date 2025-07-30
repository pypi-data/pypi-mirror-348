from typing import Literal, Optional, List, Union, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict

StatusType = Literal['OK', 'ERROR']


class BaseRequest(BaseModel):
    api_key: str
    api_url: str
    debug: bool = False  # Added default value


class BaseResponse(BaseModel):
    status: StatusType
    message: Optional[str] = None


CategoryType = Literal['content', 'concepts', 'features', 'table']


class Category(BaseModel):
    id: str
    collectionId: str
    name: str
    type: CategoryType
    instructions: str
    dateCreated: str
    dateUpdated: str


class CreateCategoryPayload(BaseModel):
    name: str
    type: CategoryType
    instructions: str


LayoutPosition = List[int]


class DocumentLayoutOutput(BaseModel):
    position: LayoutPosition
    type: Literal['title', 'subtitle', 'list', 'text', 'table', 'image']
    content: str


class DocumentLayout(DocumentLayoutOutput):
    index: int
    page: int


class AudioLayout(BaseModel):
    index: int
    start: str
    end: str
    narrator: str
    description: str
    content: str


class PhotoLayout(BaseModel):
    position: LayoutPosition
    type: str
    description: str


class VideoLayout(BaseModel):
    index: int
    start: str
    end: str
    audio: str
    narration: str
    narrator: str
    objects: List[PhotoLayout]


LayoutType = Literal['document', 'photo', 'audio', 'video']


class FeatureLayout(BaseModel):
    position: List[int]
    label: str
    description: str
    model_config = ConfigDict(extra='allow')


JobType = Literal['status', 'nodes', 'vectors', 'edges', 'category']
JobStatusType = Literal[
    'processing', 'error', 'ready', 'cancelled', 'unprocessed', 'partial', 'all'
]


class Job(BaseModel):
    id: str
    collectionId: str
    collection: Optional['Collection'] = None
    documentId: str
    document: Optional['Document'] = None
    status: JobStatusType
    nodes: JobStatusType
    edges: JobStatusType
    vectors: JobStatusType
    category: JobStatusType
    message: str
    dateCreated: datetime
    dateUpdated: datetime


class Document(BaseModel):
    id: str
    collectionId: str
    path: str
    name: str
    type: str
    layoutType: str
    layoutNodes: int
    instructions: str
    job: Optional[Job] = None
    layout: Optional[
        Union[
            List[DocumentLayout],
            List[PhotoLayout],
            List[VideoLayout],
            List[AudioLayout],
        ]
    ] = None
    dateCreated: str
    dateUpdated: str


CollectionType = Literal['frame', 'searchable-frame', 'canon', 'features']


class Collection(BaseModel):
    id: str
    organizationId: str
    organization: 'Organization'
    name: str
    type: CollectionType
    description: str
    tags: List[str]
    instructions: Optional[str] = None
    graphInstructions: Optional[str] = None
    promptInstructions: Optional[str] = None
    searchInstructions: Optional[str] = None
    categories: Optional[List[Category]] = None
    documents: Optional[List[Document]] = None
    dateCreated: str
    dateUpdated: str


class CollectionStats(BaseModel):
    docs: int
    size: int
    nodes: int
    status: Dict


MembershipType = Literal['member', 'admin']


class Member(BaseModel):
    id: str
    accountId: str
    organizationId: str
    role: MembershipType
    dateCreated: str
    dateUpdated: str
    account: Dict


class Organization(BaseModel):
    id: str
    name: str
    description: str
    members: Optional[List[Member]] = None
    collections: Optional[List[Collection]] = None
    dateCreated: datetime
    dateUpdated: datetime


class OrganizationMemberPayload(BaseModel):
    id: str
    role: MembershipType


SearchType = Literal['summary', 'phrase', 'keywords']
SearchMethod = Literal['fast', 'normal', 'precise']


class QueryPayload(BaseModel):
    collection_id: str
    prompt: str
    category_id: Optional[str] = None
    method: Optional[SearchMethod] = None
    type: Optional[SearchType] = None
    vectorDepth: Optional[int] = None
    nodeDepth: Optional[int] = None
    maxQueries: Optional[int] = None
    maxResults: Optional[int] = None
    includeContent: Optional[bool] = None
    includeEdges: Optional[bool] = None


class PromptMessage(BaseModel):
    """Single message in a prompt-driven interaction.

    Attributes:
        role: Origin of the message ('user', 'model', or 'system').
        content: Textual content of the message.
    """

    role: Literal['user', 'model', 'system']
    content: str


class PromptPayload(BaseModel):
    collection_id: str
    prompt: str
    category_id: Optional[str] = None
    method: Optional[SearchMethod] = None
    type: Optional[SearchType] = None
    vectorDepth: Optional[int] = None
    nodeDepth: Optional[int] = None
    maxQueries: Optional[int] = None
    maxResults: Optional[int] = None
    template: Optional[str] = None
    cot: Optional[bool] = None
    threadId: Optional[str] = None
    chat: Optional[bool] = None


class QueryDefaults(BaseModel):
    type: str
    vectorDepth: int
    nodeDepth: int
    maxQueries: int
    maxResults: int


QueryFast = QueryDefaults(
    type='phrase', vectorDepth=10, nodeDepth=1, maxQueries=1, maxResults=10
)
QueryNormal = QueryDefaults(
    type='summary', vectorDepth=8, nodeDepth=2, maxQueries=3, maxResults=10
)
QueryPrecise = QueryDefaults(
    type='summary', vectorDepth=10, nodeDepth=5, maxQueries=3, maxResults=10
)


QueryKV = {'fast': QueryFast, 'normal': QueryNormal, 'precise': QueryPrecise}


class SearchResult(BaseModel):
    content: str
    citation: str
    reason: str
