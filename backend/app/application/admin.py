"""Application-layer admin service (amendment 02).

Additive and optional: routes using this service are new and never gate the
demo. When the store is unavailable (no Supabase configuration) the service
fails closed with a clear error — admin capabilities are never implicitly
granted. Role checks always go through this service (service-role lookup of
the caller's profile row); the client-supplied token only identifies the
user, it never asserts the role.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.storage.postgrest_admin import PostgrestAdminStore

VALID_ROLES = frozenset({"user", "admin"})
VALID_PLANS = frozenset({"free", "premium"})


class AdminUnavailableError(RuntimeError):
    """Raised when admin storage is not configured (no Supabase env)."""


class NotAdminError(PermissionError):
    """Raised when the caller's profile role is not 'admin' (fail closed)."""


class AdminService:
    """Role-aware admin operations over the profiles + admin_actions tables."""

    def __init__(self, store: PostgrestAdminStore | None = None) -> None:
        self._store = store

    def _require_store(self) -> PostgrestAdminStore:
        if self._store is None:
            raise AdminUnavailableError("Admin console is not configured on this server")
        return self._store

    # -- role gate ----------------------------------------------------------

    def require_admin(self, user_id: str) -> dict[str, Any]:
        """Return the caller's profile when role == 'admin'; raise otherwise.

        Fail-closed: unconfigured storage, a missing profile row, or a
        transport error all deny admin access.
        """
        store = self._require_store()
        profile = store.get_profile(user_id)
        if profile is None:
            raise NotAdminError("No profile for the authenticated user")
        if profile.get("role") != "admin":
            raise NotAdminError("Admin role required")
        return profile

    # -- self profile (account surface) --------------------------------------

    def get_profile(self, user_id: str, email: str = "") -> dict[str, Any] | None:
        """The caller's own profile, lazily created on first lookup.

        Lazy creation mirrors the 001 design (no auth hooks); the insert is
        on-conflict-ignore so an existing row keeps its role/plan.
        """
        store = self._require_store()
        profile = store.get_profile(user_id)
        if profile is None and email:
            store.upsert_profile_defaults(user_id, email)
            profile = store.get_profile(user_id)
        return profile

    # -- user management ------------------------------------------------------

    def list_users(self, page: int, page_size: int, search: str = "") -> dict[str, Any]:
        rows, total = self._require_store().list_profiles(page, page_size, search)
        return {"items": rows, "total": total, "page": page, "page_size": page_size}

    def update_user(
        self,
        acting_admin_id: str,
        target_user_id: str,
        role: str | None = None,
        plan: str | None = None,
    ) -> dict[str, Any]:
        """Change a user's role and/or plan; every change is audited."""
        if role is not None and role not in VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        if plan is not None and plan not in VALID_PLANS:
            raise ValueError(f"Invalid plan: {plan}")
        changes: dict[str, Any] = {}
        if role is not None:
            changes["role"] = role
        if plan is not None:
            changes["plan"] = plan
        if not changes:
            raise ValueError("Nothing to update (provide role and/or plan)")
        store = self._require_store()
        updated = store.patch_profile(target_user_id, changes)
        if updated is None:
            updated = store.get_profile(target_user_id)
        store.record_action(
            actor_id=acting_admin_id,
            action="update_user",
            target_type="profile",
            target_id=target_user_id,
            payload=changes,
        )
        if updated is None:
            raise ValueError("Target user not found")
        return updated

    # -- audit ----------------------------------------------------------------

    def audit(
        self,
        actor_id: str,
        action: str,
        target_type: str,
        target_id: str,
        payload: dict[str, Any],
    ) -> None:
        """Append to the admin_actions audit trail (amendment 02 §4)."""
        self._require_store().record_action(actor_id, action, target_type, target_id, payload)

    def list_actions(self, limit: int = 20) -> list[dict[str, Any]]:
        return self._require_store().list_actions(limit)
