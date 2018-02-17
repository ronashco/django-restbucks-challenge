from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError
from core.products.models import Product

User = get_user_model()


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'option', 'items')


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    @staticmethod
    def validate_email(value):
        """check for uniqueness in database"""
        if User.objects.filter(email=value).exists():
            raise ValidationError('The email is taken.')
        return value

    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise ValidationError('Password must be contains at least 8 letters.')
        return value

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
