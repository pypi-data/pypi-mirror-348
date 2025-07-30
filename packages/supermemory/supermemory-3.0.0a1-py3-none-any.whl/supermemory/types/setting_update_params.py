# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SettingUpdateParams"]


class SettingUpdateParams(TypedDict, total=False):
    exclude_items: Annotated[List[str], PropertyInfo(alias="excludeItems")]

    filter_prompt: Annotated[str, PropertyInfo(alias="filterPrompt")]

    filter_tags: Annotated[Dict[str, List[str]], PropertyInfo(alias="filterTags")]

    include_items: Annotated[List[str], PropertyInfo(alias="includeItems")]

    should_llm_filter: Annotated[bool, PropertyInfo(alias="shouldLLMFilter")]
