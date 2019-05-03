from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order, ProductOrderType, OrderProduct
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from collections import namedtuple
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from coffeeshop.common.utils import default_send_mail
from coffeeshop.common.responses import bad_request, not_found, ok, ErrorCode, forbidden, created

def prepareOrderItems(items):
    Pair = namedtuple("Pair", ["product", "product_order_type", "product_count"])
    order_product_list = list()

    for item in items:
        try:
            product_id = item["product"]
            product_order_type_id = item["type"]
            product_count = item["count"]
        except:
            return None, bad_request(ErrorCode.DATA_FIELD_NOT_FOUND)

        if type(product_count) is not int or product_count < 1:
            return None, bad_request(ErrorCode.PRODUCT_COUNT_INVALID)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None, not_found(ErrorCode.PRODUCT_NOT_FOUND)

        product_order_type = None
        if product_order_type_id is not None:
            try:
                product_order_type = ProductOrderType.objects.get(pk=product_order_type_id)
            except ProductOrderType.DoesNotExist:
                return None, not_found(ErrorCode.PRODUCT_ORDER_NOT_FOUND)
            if product_order_type.product_type != product.type:
                return None, bad_request(ErrorCode.PRODUCT_INVALID_ORDER_TYPE)

        if product_order_type is None and product.type is not None:
            return None, bad_request(ErrorCode.PRODUCT_INVALID_ORDER_TYPE)

        order_product_list.append(Pair(product, product_order_type, product_count))
    return order_product_list, None


class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return ok(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return created(serializer.data)
        return bad_request(ErrorCode.INVALID_DATA)


class ProductDetail(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return ok(serializer.data)


class OrderEntryView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        items = request.data.get('items', list())
        if type(items) is not list or len(items) == 0:
            return bad_request(ErrorCode.NOT_ITEM_IN_ORDER)

        consume_location = request.data.get('consume_location', None)
        if consume_location not in dict(Order.CONSUME_LOCATION_CHOICE):
            return bad_request(ErrorCode.CONSUME_LOCATION_NOT_FOUND)

        order_product_list, error = prepareOrderItems(items)
        if error is not None:
            return error

        with transaction.atomic():
            total_price = 0
            order = Order(consume_location=consume_location, total_price=total_price, user=user)
            order.save()

            for item in order_product_list:
                order_product = OrderProduct(product=item.product, order=order,
                                             product_order_type=item.product_order_type, price=item.product.price,
                                             count=item.product_count)
                order_product.save()
                total_price += (item.product.price * item.product_count)

            order.total_price = total_price
            order.save()
            transaction.on_commit(default_send_mail(to=user.email, status=order.status))

        return ok(OrderSerializer(order).data)


class OrderDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)

        serializer = OrderSerializer(order)
        return ok(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        order = self.get_object(pk)
        if order.status != Order.STATUS_WAITING:
            return bad_request(ErrorCode.CHANGE_NOT_WAITING_ORDER)

        if order.user != user:
            return forbidden(ErrorCode.NOT_FOR_YOU)

        items = request.data.get('items', list())
        if type(items) is not list or len(items) == 0:
            return bad_request(ErrorCode.NOT_ITEM_IN_ORDER)

        order_product_list, error = prepareOrderItems(items)
        if error is not None:
            return error

        with transaction.atomic():
            total_price = 0
            pre_order_items = OrderProduct.objects.filter(order=order, deleted=False)
            pre_order_items.update(deleted=True)
            for item in order_product_list:
                order_product = OrderProduct(product=item.product, order=order,
                                             product_order_type=item.product_order_type, price=item.product.price,
                                             count=item.product_count)
                order_product.save()
                total_price += (item.product.price * item.product_count)

            order.total_price = total_price
            order.save()

        serializer = OrderSerializer(order)
        return ok(serializer.data)

    def delete(self, request, pk, format=None):
        user = request.user

        order = self.get_object(pk)

        if order.status != Order.STATUS_WAITING:
            return bad_request(ErrorCode.CANCEL_NOT_WAITING_ORDER)

        if order.user != user:
            return forbidden(ErrorCode.NOT_FOR_YOU)

        order.status = Order.STATUS_CANCEL
        order.save()

        return ok()