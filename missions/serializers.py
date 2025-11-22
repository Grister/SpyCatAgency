from rest_framework import serializers
from .models import Mission, Target
from cats.models import Cat


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete']
        read_only_fields = ['id', 'complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(
        queryset=Cat.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete', 'targets']
        read_only_fields = ['complete']

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError('Mission must have 1 to 3 targets.')
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')

        cat = validated_data.get('cat')
        if cat and cat.active_mission:
            raise serializers.ValidationError('Cat already has an active mission.')

        mission = Mission.objects.create(**validated_data)

        for t in targets_data:
            Target.objects.create(mission=mission, **t)

        return mission


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete']
        read_only_fields = ['id', 'name', 'country']

    def validate(self, attrs):
        target = self.instance
        mission = target.mission

        if mission.complete:
            raise serializers.ValidationError('Mission already completed.')

        if target.complete:
            raise serializers.ValidationError('Target already completed.')

        return attrs

    def update(self, instance, validated_data):
        instance.notes = validated_data.get('notes', instance.notes)
        instance.complete = validated_data.get('complete', instance.complete)
        instance.save()

        mission = instance.mission
        if all(t.complete for t in mission.targets.all()):
            mission.complete = True
            mission.save()

        return instance


class MissionAssignCatSerializer(serializers.Serializer):
    cat_id = serializers.IntegerField()

    def validate_cat_id(self, cat_id):
        try:
            cat = Cat.objects.get(id=cat_id)
        except Cat.DoesNotExist:
            raise serializers.ValidationError('Cat not found.')

        if cat.active_mission:
            raise serializers.ValidationError('Cat already assigned to a mission.')

        return cat_id

    def update(self, instance, validated_data):
        if instance.complete:
            raise serializers.ValidationError('Cannot assign a cat to a completed mission.')

        cat = Cat.objects.get(id=validated_data['cat_id'])

        instance.cat = cat
        instance.save()

        cat.active_mission = instance
        cat.save()

        return instance
