from rest_framework import serializers
from people.models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "document_number",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]