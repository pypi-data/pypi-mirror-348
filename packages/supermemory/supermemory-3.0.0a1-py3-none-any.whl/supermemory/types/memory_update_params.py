# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MemoryUpdateParams"]


class MemoryUpdateParams(TypedDict, total=False):
    content: Required[str]

    container_tags: Annotated[List[str], PropertyInfo(alias="containerTags")]

    metadata: Dict[str, Union[str, float, bool]]
