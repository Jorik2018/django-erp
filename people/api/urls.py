from rest_framework.routers import DefaultRouter

from .views import PersonViewSet


router = DefaultRouter()

router.register(
    "people",
    PersonViewSet,
    basename="people",
)


urlpatterns = router.urls