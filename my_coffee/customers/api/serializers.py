from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from productions.api.serializers import MenuSerializer
from productions.models import Menu
from ..models import Order

from django.contrib.auth import get_user_model


class OrderListSerializer(serializers.ModelSerializer):
    ordered_productions = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'location',
            'address',
            'created_at',
            'updated_at',
            'ordered_productions',
            'status',
            'id'
        ]
        read_only_fields = [
            'status',
        ]


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    ordered_productions = MenuSerializer(many=True)

    def create(self, validated_data):
        ordered_productions_data = validated_data.pop("ordered_productions")
        order = Order.objects.create(**validated_data)
        for order_p_data in ordered_productions_data:
            Menu.objects.create(order=order, **order_p_data)
        return order

    class Meta:
        model = Order
        fields = [
            'location',
            'address',
            'created_at',
            'updated_at',
            'ordered_productions',
            'status',
            'id'
        ]
        read_only_fields = [
            'status',
        ]


User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        return data
