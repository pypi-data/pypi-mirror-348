# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ConnectionGetResponse"]


class ConnectionGetResponse(BaseModel):
    id: str

    created_at: float = FieldInfo(alias="createdAt")

    provider: str

    expires_at: Optional[float] = FieldInfo(alias="expiresAt", default=None)

    metadata: Optional[Dict[str, object]] = None
