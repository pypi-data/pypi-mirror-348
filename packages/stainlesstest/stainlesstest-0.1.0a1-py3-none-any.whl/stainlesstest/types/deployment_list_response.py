# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .deployment_response import DeploymentResponse

__all__ = ["DeploymentListResponse"]


class DeploymentListResponse(BaseModel):
    next: Optional[str] = None
    """A URL pointing to the next page of deployment objects if any"""

    previous: Optional[str] = None
    """A URL pointing to the previous page of deployment objects if any"""

    results: Optional[List[DeploymentResponse]] = None
    """An array containing a page of deployment objects"""
