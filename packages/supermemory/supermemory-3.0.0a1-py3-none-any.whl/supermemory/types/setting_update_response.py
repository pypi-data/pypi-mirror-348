# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SettingUpdateResponse", "Settings"]


class Settings(BaseModel):
    exclude_items: Optional[List[str]] = FieldInfo(alias="excludeItems", default=None)

    filter_prompt: Optional[str] = FieldInfo(alias="filterPrompt", default=None)

    filter_tags: Optional[Dict[str, List[str]]] = FieldInfo(alias="filterTags", default=None)

    include_items: Optional[List[str]] = FieldInfo(alias="includeItems", default=None)

    should_llm_filter: Optional[bool] = FieldInfo(alias="shouldLLMFilter", default=None)


class SettingUpdateResponse(BaseModel):
    message: str

    settings: Settings
