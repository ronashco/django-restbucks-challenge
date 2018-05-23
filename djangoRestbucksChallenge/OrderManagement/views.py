from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product, CustomizedProduct, Order, OrderLine


@login_required
def signout(request):
    current_user = request.user
    if current_user is not None:
        logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def panel(request):
    return render(request, 'panel.html')


@login_required
def new_order(request):
    if request.method == 'GET':
        return render(request, 'new_order.html', {'products': get_products_dict_from_database()})
    elif request.method == 'POST':  # TODO no option exception
        new_order = Order(customer=request.user, location=request.POST.get('location'))
        new_order.save()
        for piece, type in request.POST.items():
            if not piece == 'csrfmiddlewaretoken' and not piece == 'location':
                idx = piece.find('-')
                product = Product.objects.get(pk=int(piece[:idx]))
                if piece[idx+1:] == 'nooption':
                    try:
                        CustomizedProduct.objects.get(product=product)
                        return render(request, 'new_order.html', {'error_message': 'an error happened. try again.'})
                    except:
                        cp = CustomizedProduct(product=product, option='None', type='None')
                        cp.save()
                        line = OrderLine(order=new_order, customized_product=cp)
                        line.save()
                else:
                    cp = CustomizedProduct.objects.get(product=product, option=piece[idx + 1:], type=type)
                    line = OrderLine(order=new_order, customized_product=cp)
                    line.save()

        return HttpResponseRedirect(reverse('panel'))


@login_required
def view_orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'view_orders.html', {'orders': orders})


def get_order_details(id):
    order = Order.objects.get(pk=id)
    price = OrderLine.objects.filter(order=order).aggregate(Sum('customized_product__product__price'))
    price = price['customized_product__product__price__sum']
    return order, price


@login_required
def view_an_order(request):
    order, price = get_order_details(request.GET.get('id'))
    products = Product.objects.all()

    my_customized_products_id = [orderline.customized_product.id for orderline in order.orderline_set.all()]
    return render(request, 'view_an_order.html', {'order': order, 'price': price, 'products': products,
                                                  'my_customized_products_id' : my_customized_products_id})

