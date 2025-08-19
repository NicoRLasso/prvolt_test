from rest_framework import serializers

class PokemonSpriteSerializer(serializers.Serializer):
    front_default = serializers.URLField(required=False, allow_null=True)
    back_default = serializers.URLField(required=False, allow_null=True)

class PokemonTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()

class PokemonTypeSlotSerializer(serializers.Serializer):
    slot = serializers.IntegerField()
    type = PokemonTypeSerializer()

class PokemonStatSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()

class PokemonStatSlotSerializer(serializers.Serializer):
    base_stat = serializers.IntegerField()
    effort = serializers.IntegerField()
    stat = PokemonStatSerializer()

class PokemonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    base_experience = serializers.IntegerField(required=False, allow_null=True)
    sprites = PokemonSpriteSerializer()
    types = PokemonTypeSlotSerializer(many=True)
    stats = PokemonStatSlotSerializer(many=True)

class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()


class NamesListSerializer(serializers.Serializer):
    results = serializers.ListField(child=serializers.CharField())
