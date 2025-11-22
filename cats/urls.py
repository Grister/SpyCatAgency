from rest_framework.routers import DefaultRouter
from .views import CatViewSet


router = DefaultRouter()
router.register('', CatViewSet)

urlpatterns = router.urls
