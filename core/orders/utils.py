from core.orders.models import Cart, OrderProduct


def user_cart_detail(cart_query_set):
    # Return count/total price/product objects from a collection of carts.
    count = len(cart_query_set)
    try:
        total_price = sum(map(lambda card: card.product.price, cart_query_set))
    except AttributeError:
        total_price = 0
    products = []
    for cart in cart_query_set:
        cart.product.selected_item = cart.customization
        products.append(cart.product)
    return count, total_price, products


def merge_cart_to_order(order_object):
    """
    ‌Create order from cart items, remove cart items and return OrderProduct objects
    :param order_object:
    :return:
    """
    carts = Cart.objects.select_related('product').filter(user=order_object.user)
    p = [OrderProduct(order=order_object,
                      product=cart.product,
                      customization=cart.customization,
                      price=cart.product.price)
         for cart in carts]
    carts.delete()
    return OrderProduct.objects.bulk_create(p)
