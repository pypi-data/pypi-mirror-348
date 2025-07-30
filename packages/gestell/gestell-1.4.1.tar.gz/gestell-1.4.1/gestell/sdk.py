"""
Gestell SDK client

This module contains all Gestell features, which wires together every
first-class Gestell service (organization, collection, query, document, job).

Examples
--------
Basic usage in an async context:

    from gestell import Gestell

    sdk = Gestell(debug=True)  # Reads env vars automatically
    orgs = await sdk.organization.list()
    print(orgs)

For more patterns see the public docs: https://gestell.ai/docs
"""

import os
from typing import Optional
from dotenv import load_dotenv

from gestell.service import (
    OrganizationService,
    CollectionService,
    QueryService,
    DocumentService,
    JobService,
)


class Gestell:
    """
    **Gestell SDK client** - single entry-point for every Gestell API.

    Parameters
    ----------
    url :
        Base API endpoint. Falls back to the environment variable
        ``GESTELL_API_URL`` or the default
        ``https://platform.gestell.ai`` when omitted.
    key :
        Personal or project API key. Falls back to ``GESTELL_API_KEY``.
    debug :
        When *True*, logs verbose request/response details to stderr.

    Notes
    -----
    * All sub-services return *strongly-typed* response objects
      (``{ status, message, result, … }``) for first-class IDE support.
    * The constructor loads a ``.env`` file automatically so your IDE
      recognises environment variables during local development.
    """

    # ------------------------------------------------------------------ #
    # Construction helpers
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        *,
        url: Optional[str] = None,
        key: Optional[str] = None,
        debug: bool = False,
    ) -> None:
        load_dotenv()

        self.api_url: str = url or os.getenv(
            'GESTELL_API_URL', 'https://platform.gestell.ai'
        )
        self.api_key: str = key or os.getenv('GESTELL_API_KEY', '')
        self.debug: bool = debug

    # ------------------------------------------------------------------ #
    # Lazily-instantiated service clients
    # ------------------------------------------------------------------ #

    @property
    def organization(self) -> OrganizationService:
        """
        **Organization services**.

        * CRUD operations on organisations (list, get, update, members).
        * Admin privileges are required for updating organizations.

        Example
        -------
        ```python
        orgs = await sdk.organization.list()
        ```
        """
        return OrganizationService(self.api_key, self.api_url, self.debug)

    @property
    def collection(self) -> CollectionService:
        """
        **Collection services**.

        * Full CRUD plus category helpers.
        * See https://gestell.ai/docs/reference#collection for details.
        """
        return CollectionService(self.api_key, self.api_url, self.debug)

    @property
    def query(self) -> QueryService:
        """
        **Query services**.

        Semantic search, prompt streaming, feature/table helpers, exports.

        Example
        -------
        ```python
        res = await sdk.query.search(
            collection_id='UUID',
            prompt='Give me a summary of the ULTA filing from 2024',
        )
        ```
        """
        return QueryService(self.api_key, self.api_url, self.debug)

    @property
    def document(self) -> DocumentService:
        """
        **Document services**.

        Upload, list, export, update & delete documents.
        Supports streaming uploads and presigned URL helpers.
        """
        return DocumentService(self.api_key, self.api_url, self.debug)

    @property
    def job(self) -> JobService:
        """
        **Job services**.

        Inspect long-running tasks, cancel or reprocess jobs.
        """
        return JobService(self.api_key, self.api_url, self.debug)
