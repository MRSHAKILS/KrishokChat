"""Storage infrastructure (premium lane): Supabase PostgREST adapter."""

from app.infrastructure.storage.postgrest import PostgrestSavedHistoryStore

__all__ = ["PostgrestSavedHistoryStore"]