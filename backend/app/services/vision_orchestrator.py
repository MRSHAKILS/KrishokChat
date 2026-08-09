"""Compatibility import for the modular vision router.

The active implementation is `app.api.vision` -> `app.application.vision_pipeline`.
This file remains only for older documentation/scripts that import its router.
"""

from app.api.vision import router

__all__ = ["router"]
