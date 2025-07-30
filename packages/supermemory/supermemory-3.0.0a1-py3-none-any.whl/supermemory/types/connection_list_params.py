# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ConnectionListParams"]


class ConnectionListParams(TypedDict, total=False):
    end_user_id: Annotated[str, PropertyInfo(alias="endUserId")]
