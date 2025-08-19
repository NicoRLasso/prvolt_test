"""Pokemon API views."""

import asyncio
from typing import Any

from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from pokemon.serializers.list import PokemonListSerializer
from pokemon.serializers.core import PokemonSerializer, HealthSerializer, NamesListSerializer
from pokemon.service import PokeAPIService


DEFAULT_POKEMON_LIMIT: int = 20


def run_async(coro: Any) -> Any:
    """Run async function in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)



@extend_schema(
    tags=["pokemon"],
    responses={200: PokemonSerializer, 400: OpenApiResponse(description="Bad request")},
)
@api_view(["GET"])
def get_pokemon_by_id(request: Request, pokemon_id: int) -> Response:
    service = PokeAPIService()
    try:
        payload = run_async(service.get_pokemon_by_id(pokemon_id))
    except Exception as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        run_async(service.close())

    serializer = PokemonSerializer(data=payload)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["pokemon"],
    responses={200: PokemonSerializer, 400: OpenApiResponse(description="Bad request")},
)
@api_view(["GET"])
def get_pokemon_by_name(request: Request, name: str) -> Response:
    service = PokeAPIService()
    try:
        payload = run_async(service.get_pokemon_by_name(name))
    except Exception as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        run_async(service.close())

    serializer = PokemonSerializer(data=payload)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["pokemon"],
    parameters=[
        OpenApiParameter(
            name="limit", type=int, required=False,
            description="Items per page", default=DEFAULT_POKEMON_LIMIT
        ),
        OpenApiParameter(
            name="offset", type=int, required=False,
            description="Offset for pagination", default=0
        ),
    ],
    responses={200: PokemonListSerializer, 400: OpenApiResponse(description="Bad request")},
)
@api_view(["GET"])
def get_pokemon_list(request: Request) -> Response:
    limit = int(request.GET.get("limit", DEFAULT_POKEMON_LIMIT))
    offset = int(request.GET.get("offset", 0))

    service = PokeAPIService()
    try:
        payload = run_async(service.get_pokemon_list(limit, offset))
    except Exception as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        run_async(service.close())

    serializer = PokemonListSerializer(data=payload)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["pokemon"],
    responses={200: NamesListSerializer, 400: OpenApiResponse(description="Bad request")},
)
@api_view(["GET"])
def get_pokemon_by_type(request: Request, pokemon_type: str) -> Response:
    service = PokeAPIService()
    try:
        names = run_async(service.get_pokemon_by_type(pokemon_type))
    except Exception as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        run_async(service.close())

    return Response({"results": names})


@extend_schema(tags=["health"], responses={200: HealthSerializer})
@api_view(["GET"])
def health_check(request: Request) -> Response:
    return Response({"status": "healthy"})
