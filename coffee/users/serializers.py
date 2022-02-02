from rest_framework import serializers
from users.models import User

class UserListSerializer(serializers.ModelSerializer):
    """Serializer for all user fields"""
    class Meta():
        model = User
        exclude = ()
        fields = "__all__"

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation procedure"""
    class Meta():
        model = User
        fields = ("first_name",
                  "last_name",
                  'email',
                  'password')

    def create(self, validated_data):
        """Create user function"""
        user = User.objects.create_user(**validated_data)
        return user
