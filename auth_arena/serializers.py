from rest_framework import serializers
from authenticator.admin import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'email', 'address')

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                         email=validated_data['email'],
                                         role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return user
