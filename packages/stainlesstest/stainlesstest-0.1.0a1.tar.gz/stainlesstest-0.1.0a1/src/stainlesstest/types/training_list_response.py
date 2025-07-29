# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .models.schemas_training import SchemasTraining

__all__ = ["TrainingListResponse"]


class TrainingListResponse(BaseModel):
    next: Optional[str] = None
    """URL to the next page of results"""

    previous: Optional[str] = None
    """URL to the previous page of results"""

    results: Optional[List[SchemasTraining]] = None
