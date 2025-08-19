from rest_framework import serializers

class PokemonListItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()

class PokemonListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(required=False, allow_null=True)
    previous = serializers.URLField(required=False, allow_null=True)
    results = serializers.ListSerializer(child=PokemonListItemSerializer())
