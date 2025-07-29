# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .prediction_response import PredictionResponse

__all__ = ["PredictionListResponse"]


class PredictionListResponse(BaseModel):
    next: Optional[str] = None

    previous: Optional[str] = None

    results: Optional[List[PredictionResponse]] = None
