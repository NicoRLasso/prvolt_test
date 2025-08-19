"""Pokemon app URLs."""

from django.urls import path

from pokemon.views import get_pokemon_by_id, get_pokemon_by_name, get_pokemon_list, get_pokemon_by_type, health_check

urlpatterns = [
    path("pokemon/id/<int:pokemon_id>/",get_pokemon_by_id, name="pokemon-by-id"),
    path("pokemon/name/<str:name>/",get_pokemon_by_name, name="pokemon-by-name"),
    path("pokemon/",get_pokemon_list, name="pokemon-list"),
    path(
        "pokemon/type/<str:pokemon_type>/",
       get_pokemon_by_type,
        name="pokemon-by-type",
    ),
    path("health/",health_check, name="health-check"),
]
