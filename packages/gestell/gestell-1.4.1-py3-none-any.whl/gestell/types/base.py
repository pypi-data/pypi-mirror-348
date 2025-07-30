from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

StatusType = Literal['OK', 'ERROR']


class BaseRequest(BaseModel):
    """
    Base schema for all API requests.

    Defines the common fields every request to the Gestell API must include.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )

    api_key: str = Field(..., description='API key used for request authentication.')
    api_url: str = Field(..., description='Base URL of the Gestell API endpoint.')
    debug: bool = Field(
        False, description='Flag to enable verbose logging for debugging.'
    )


class BaseResponse(BaseModel):
    """
    Base schema for all API responses.

    Defines the common fields returned in every response from the Gestell API.
    """

    status: StatusType = Field(
        ...,
        description="Indicates whether the request succeeded ('OK') or failed ('ERROR').",
    )
    message: Optional[str] = Field(
        None,
        description='Optional human-readable message with additional details or error info.',
    )
