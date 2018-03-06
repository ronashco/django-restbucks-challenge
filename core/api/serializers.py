from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from core.products.models import Product
from core.orders.models import Cart, Order, OrderProduct

User = get_user_model()


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'option']


class ProductListSerializer(BaseProductSerializer):
    """
    Product model serialization.
    """
    class Meta(BaseProductSerializer.Meta):
        fields = BaseProductSerializer.Meta.fields + ['items', 'id']


class RegisterSerializer(serializers.ModelSerializer):
    """
    User model serialization.
    """
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
            raise serializers.ValidationError('The email is taken.')
        return value

    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 letters.')
        return value

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        # We won't to store raw passwords,
        # we use user.set_password to hash passwords.
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShowCartsSerializer(serializers.Serializer):
    """
    We want to use the ShowCartsSerializer only for show cart data in api,
    so we won't to create/update Cart objects using it.
    """

    class CartProductSerializer(BaseProductSerializer):
        """
        This object has been used as a part of ShowCartsSerializer.
        """
        selected_item = serializers.CharField()

        class Meta(BaseProductSerializer.Meta):
            fields = BaseProductSerializer.Meta.fields + ['selected_item', 'id']
            read_only_fields = fields  # all fields are read only

    count = serializers.CharField()
    total_price = serializers.CharField()
    products = CartProductSerializer(many=True)

    class Meta:
        fields = ('count', 'total_price', 'products')
        read_only_fields = '__all__'

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CartSerializer(serializers.ModelSerializer):
    """
    core.carts.models.Cart model serialization.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ('product', 'user', 'customization')

    def validate(self, attrs):
        cart = self.Meta.model(**attrs)
        # Apply custom model's level validations.
        try:
            cart.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs


class OrderListSerializer(serializers.ModelSerializer):
    """
    We will use it for create/retrieve order objects.
    """
    url = serializers.HyperlinkedIdentityField(view_name='api:order',
                                               lookup_field='id',
                                               lookup_url_kwarg='order_id')
    date = serializers.DateTimeField(format='%d %b %Y-%H:%M', required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('id', 'status', 'date', 'location', 'user', 'total_price', 'url')
        read_only_fields = ('id', 'status', 'date', 'total_price', 'url')

    def validate(self, attrs):
        if not Cart.objects.filter(user=attrs.get('user')).exists():
            raise serializers.ValidationError("Cart is empty.")
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    """
    Order detail serialization.
    We will use it for show order with all details (products/date/location and everything),
    The order object(s) must have a order_products attribute,
    otherwise the serializer will raise AttributeError.
    The order_products attribute is a container of core.orders.models.OrderProductApiModel objects.
    We use OrderProductApiModel here instead of main Product model to serialize products.
    We use this serializer for update a waiting order too.
    """
    class ProductSerializer(BaseProductSerializer):
        item = serializers.CharField()

        class Meta(BaseProductSerializer.Meta):
            fields = BaseProductSerializer.Meta.fields + ['item', 'id']

    products = ProductSerializer(many=True, source='order_products', read_only=True)
    date = serializers.DateTimeField(format='%d %b %Y-%H:%M')

    class Meta:
        model = Order
        fields = ('total_price', 'status', 'location', 'date', 'products')
        read_only_fields = ('total_price', 'status', 'date', 'products')

    def validate(self, attrs):
        if self.instance.status != 'w':
            raise serializers.ValidationError("You can only change waiting orders")
        return attrs


class OrderProductSerializer(serializers.ModelSerializer):
    """
    We use it for update/delete a order's product (product customization),
    Users can edit a waiting order (order object with w status value).
    We divided order modification to 2 parts:
    the first one for general order information (e.g location),
    and the second one for either update products customization or fully remove it
    from the order, this serializer handles the second part.
    """
    class Meta:
        model = OrderProduct
        fields = ('customization',)

    def validate(self, attrs):
        if self.instance.order.status != 'w':
            #  users can update a product if and only if
            # it belongs to a waiting order.
            raise serializers.ValidationError("You can only change waiting orders")

        #  run model level validation.
        model = OrderProduct(
            product=self.instance.product,
            order=self.instance.order,
            customization=attrs.get('customization'),
            price=self.instance.price
        )
        try:
            model.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError({'customization': e.messages})

        return attrs
