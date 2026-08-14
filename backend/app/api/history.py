"""Saved-history routes (premium lane, P4 decision 1).

Consumes the P3 auth dependency (`require_user`) — verified Supabase tokens
only. New routes only; existing demo endpoints are untouched and ungated.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status

from app.api.dependencies import HistoryServiceDep, RequiredUserDep
from app.application.history import HistoryUnavailableError
from app.models.schemas import SavedQueryIn, SavedQueryOut

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=dict)
def list_history(
    claims: RequiredUserDep,
    service: HistoryServiceDep,
) -> dict:
    """List the current user's saved queries, newest first."""
    try:
        items = service.list(claims["sub"])
    except HistoryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"items": items, "enabled": True}


@router.post("", response_model=SavedQueryOut, status_code=status.HTTP_201_CREATED)
def create_history(
    payload: SavedQueryIn,
    claims: RequiredUserDep,
    service: HistoryServiceDep,
) -> SavedQueryOut:
    """Save a Q&A pair for the current user."""
    try:
        row = service.create(claims["sub"], payload.model_dump())
    except HistoryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return SavedQueryOut.model_validate(row)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(
    item_id: str,
    claims: RequiredUserDep,
    service: HistoryServiceDep,
) -> Response:
    """Delete one of the current user's saved queries (ownership enforced)."""
    try:
        deleted = service.delete(claims["sub"], item_id)
    except HistoryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Saved query not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)