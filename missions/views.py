from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Mission, Target
from .serializers import (
    MissionSerializer,
    TargetUpdateSerializer,
    MissionAssignCatSerializer
)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response(
                {'error': 'Cannot delete mission assigned to a cat.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=MissionAssignCatSerializer,
        responses=MissionSerializer
    )
    @action(detail=True, methods=['patch'], url_path='assign-cat')
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        serializer = MissionAssignCatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.update(mission, serializer.validated_data)
        return Response(MissionSerializer(mission).data, status=200)


class TargetUpdateViewSet(viewsets.GenericViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        target = self.get_object()
        serializer = self.get_serializer(target, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
