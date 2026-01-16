"""Arena PLM API client with session authentication."""

import httpx
from typing import Any


class ArenaClient:
    """Client for Arena PLM REST API."""

    BASE_URL = "https://api.arenasolutions.com/v1"

    def __init__(self) -> None:
        self._session_id: str | None = None
        self._workspace_id: int | None = None
        self._http = httpx.Client(timeout=30.0)

    @property
    def is_authenticated(self) -> bool:
        return self._session_id is not None

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._session_id:
            headers["arena_session_id"] = self._session_id
        return headers

    def login(self, email: str, password: str, workspace_id: int | None = None) -> dict[str, Any]:
        """Authenticate with Arena API and establish session.

        Args:
            email: User email address
            password: User password
            workspace_id: Optional workspace ID to use

        Returns:
            Login response with session info

        Raises:
            httpx.HTTPStatusError: If login fails
        """
        payload: dict[str, Any] = {"email": email, "password": password}
        if workspace_id:
            payload["workspaceId"] = workspace_id

        response = self._http.post(
            f"{self.BASE_URL}/login",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        data = response.json()
        self._session_id = data["arenaSessionId"]
        self._workspace_id = data.get("workspaceId")
        return data

    def logout(self) -> None:
        """End the current session."""
        if self._session_id:
            self._http.put(f"{self.BASE_URL}/logout", headers=self._headers())
            self._session_id = None
            self._workspace_id = None

    def search_items(
        self,
        name: str | None = None,
        number: str | None = None,
        description: str | None = None,
        category_guid: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search for items in Arena.

        Args:
            name: Filter by item name (partial match)
            number: Filter by item number (partial match)
            description: Filter by description (partial match)
            category_guid: Filter by category GUID
            limit: Max results to return (default 20, max 400)
            offset: Starting position in results

        Returns:
            Search results with count and items array

        Raises:
            RuntimeError: If not authenticated
            httpx.HTTPStatusError: If request fails
        """
        if not self.is_authenticated:
            raise RuntimeError("Not authenticated. Call login() first.")

        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if number:
            params["number"] = number
        if description:
            params["description"] = description
        if category_guid:
            params["category.guid"] = category_guid

        response = self._http.get(
            f"{self.BASE_URL}/items",
            params=params,
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()
