from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        cat = self.get_object()
        if cat.active_mission:
            return Response(
                {"error": "Cannot delete cat with an active mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

