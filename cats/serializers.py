from rest_framework import serializers
from .models import Cat
from .services.the_cat_api import validate_breed


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary', 'active_mission']
        read_only_fields = ['active_mission']

    def validate(self, attrs):
        if self.instance is None:
            breed = attrs.get('breed')
            if breed and not validate_breed(breed):
                raise serializers.ValidationError({'breed': 'Unknown cat breed.'})
        return attrs

    def update(self, instance, validated_data):
        if len(validated_data.keys()) > 1 or 'salary' not in validated_data:
            raise serializers.ValidationError('Only salary can be updated.')

        instance.salary = validated_data['salary']
        instance.save()
        return instance
