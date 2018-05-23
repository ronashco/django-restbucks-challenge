from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum

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
def menu(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})


def get_products_dict_from_database():
    products = Product.objects.all()
    products_dict = {}
    for p in products:
        products_dict[p] = dict()
    custom_products = CustomizedProduct.objects.all()
    for cp in custom_products:
        d = products_dict[cp.product]
        if cp.option in d:
            d[cp.option].append(cp.type)
        else:
            d[cp.option] = list()
            d[cp.option].append(cp.type)
    return products_dict


@login_required
def new_order(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'new_order.html', {'products': products})
    elif request.method == 'POST':  # TODO no option exception
        new_order = Order(customer=request.user, location=request.POST.get('location'))
        new_order.save()
        for piece, type in request.POST.items():
            if not piece == 'csrfmiddlewaretoken' and not piece == 'location':
                idx = type.find('-')
                product = Product.objects.get(pk=int(piece))
                cp = CustomizedProduct.objects.get(product=product, option=type[:idx], type=type[idx+1:])
                line = OrderLine(order=new_order, customized_product=cp)
                line.save()

        return HttpResponseRedirect(reverse('view_an_order') + '?id=' + str(new_order.pk))



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


@login_required
def cancel_order(request):
    order = Order.objects.get(pk=request.GET.get('id'))
    order.delete()
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'view_orders.html', {'orders': orders,
                                                'success_message': 'order canceled successfully'})


@login_required
def change_order(request):
    if request.method == 'GET':
        order, price = get_order_details(request.GET.get('id'))
        products = Product.objects.all()
        my_customized_products_id = [orderline.customized_product.id for orderline in order.orderline_set.all()]
        return render(request, 'change_order.html', {'order': order, 'price': price,
                                                  'products': products, 'my_customized_products_id': my_customized_products_id})
    elif request.method == 'POST':  # TODO no option exception
        new_order = Order.objects.get(pk=request.GET.get('id'))
        new_order.location = request.POST.get('location')
        new_order.save()
        for piece, type in request.POST.items():
            if not piece == 'csrfmiddlewaretoken' and not piece == 'location':
                idx = type.find('-')
                product = Product.objects.get(pk=int(piece))
                cp = CustomizedProduct.objects.get(product=product, option=type[:idx], type=type[idx+1:])
                try:
                    line = OrderLine.objects.get(order_id=new_order.pk, customized_product__product=product)
                    line.customized_product = cp
                    line.save()
                except OrderLine.DoesNotExist:
                    OrderLine.objects.create(order=new_order, customized_product = cp)

        return HttpResponseRedirect(reverse('view_an_order') + '?id=' + str(new_order.pk))
