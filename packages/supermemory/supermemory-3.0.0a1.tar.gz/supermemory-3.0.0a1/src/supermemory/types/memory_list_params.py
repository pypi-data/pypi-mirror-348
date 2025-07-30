# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["MemoryListParams"]


class MemoryListParams(TypedDict, total=False):
    filters: str
    """Optional filters to apply to the search"""

    limit: str
    """Number of items per page"""

    order: Literal["asc", "desc"]
    """Sort order"""

    page: str
    """Page number to fetch"""

    sort: Literal["createdAt", "updatedAt"]
    """Field to sort by"""
