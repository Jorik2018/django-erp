from rest_framework.viewsets import ModelViewSet

from people.models import Person
from .serializers import PersonSerializer


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all().order_by("-created_at")
    serializer_class = PersonSerializer