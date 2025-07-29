# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .file import File
from .._models import BaseModel

__all__ = ["FileListResponse"]


class FileListResponse(BaseModel):
    next: Optional[str] = None

    previous: Optional[str] = None

    results: Optional[List[File]] = None
