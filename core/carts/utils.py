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
