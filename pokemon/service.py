from typing import Any, Dict, List, Optional

import httpx
from rest_framework import status
from rest_framework.exceptions import ValidationError

async def _http_get(
    client: httpx.AsyncClient,
    base_url: str,
    path: str,
    *,
    query_params: Optional[Dict[str, Any]] = None,
) -> httpx.Response:
    """Make HTTP GET request with basic error handling."""
    url = f"{base_url}{path}"
    try:
        return await client.get(url, params=query_params)
    except httpx.RequestError as exc:
        raise ValidationError({"detail": "Failed to connect to PokeAPI"}) from exc


def _parse_json_or_error(response: httpx.Response) -> Dict[str, Any]:
    """Parse JSON response or raise ValidationError on failure."""
    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise ValidationError({"detail": "Resource not found"})
    if response.is_error:
        raise ValidationError({"detail": "Failed to fetch Pokemon data"})
    return response.json()


def _ensure_positive(number: int, *, field: str) -> None:
    """Validate positive integer."""
    if number <= 0:
        raise ValidationError({"detail": f"{field} must be positive"})


def _normalize_non_empty(text: str, *, field: str) -> str:
    """Normalize and validate non-empty text."""
    cleaned_text = text.strip().lower()
    if not cleaned_text:
        raise ValidationError({"detail": f"{field} cannot be empty"})
    return cleaned_text


class PokeAPIService:
    """Service for interacting with PokeAPI."""

    base_url = "https://pokeapi.co/api/v2"

    def __init__(self, client: Optional[httpx.AsyncClient] = None) -> None:
        """Initialize the service."""
        timeout_seconds = 30.0
        self.client = client or httpx.AsyncClient(timeout=timeout_seconds)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_pokemon_by_id(self, pokemon_id: int) -> Dict[str, Any]:
        """Get Pokemon by ID."""
        _ensure_positive(pokemon_id, field="Pokemon ID")

        response = await _http_get(self.client, self.base_url, f"/pokemon/{pokemon_id}")
        try:
            payload = _parse_json_or_error(response)
        except ValidationError as exc:
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise ValidationError({"detail": f"Pokemon with ID {pokemon_id} not found"}) from exc
            raise
        return payload

    async def get_pokemon_by_name(self, name: str) -> Dict[str, Any]:
        """Get Pokemon by name."""
        normalized_name = _normalize_non_empty(name, field="Pokemon name")

        response = await _http_get(self.client, self.base_url, f"/pokemon/{normalized_name}")
        try:
            payload = _parse_json_or_error(response)
        except ValidationError as exc:
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise ValidationError({"detail": f'Pokemon with name "{normalized_name}" not found'}) from exc
            raise
        return payload

    async def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get list of Pokemon."""
        if not (1 <= limit <= 1000):
            raise ValidationError({"detail": "Limit must be between 1 and 1000"})
        if offset < 0:
            raise ValidationError({"detail": "Offset must be non-negative"})

        response = await _http_get(
            self.client,
            self.base_url,
            "/pokemon",
            query_params={"limit": limit, "offset": offset},
        )
        return _parse_json_or_error(response)

    async def get_pokemon_by_type(self, pokemon_type: str) -> List[str]:
        """Get Pokemon names by type."""
        normalized_type = _normalize_non_empty(pokemon_type, field="Pokemon type")

        response = await _http_get(self.client, self.base_url, f"/type/{normalized_type}")
        try:
            payload = _parse_json_or_error(response)
        except ValidationError as exc:
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise ValidationError({"detail": f'Pokemon type "{normalized_type}" not found'}) from exc
            raise

        return [entry["pokemon"]["name"] for entry in payload.get("pokemon", [])]
