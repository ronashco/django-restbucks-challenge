# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView


from django.shortcuts import render

from customer.forms import OrderForm
from customer.models import Order
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def MainPageView(request):
    return render(request, "customer/Main_Page.html")

def ShowOrders(request):
    # order_list=[]
    order_list = Order.objects.all()

    return render(request, 'customer/Show_Orders.html', {'order_list': order_list,})

    # return render(request, "customer/Show_Orders.html")


class NewOrderView(TemplateView):
    template_name = 'customer/New_Order.html'

    def get(self, request, **kwargs):
        form = OrderForm()
        return render(request, self.template_name, {'form': form})
        # return render(request, "customer/New_Order.html")

    def post(self, request):
        form = OrderForm(request.POST)
        production = request.POST.get('production')
        consume_location = request.POST.get('consume_location')

        if form.is_valid():
            # form.save()
            order = Order.objects.create(ID_num = str(Order.ID_number), production = production, consume_location = consume_location, state = 'waiting')
            Order.ID_number = Order.ID_number + 1
            order.save()
            return HttpResponseRedirect(reverse('orders'))


class ChangeOrder(TemplateView):
    template_name = 'customer/New_Order.html'

    def get(self, request, **kwargs):
        form = OrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, ID_num):
        order = Order.objects.get(ID_num = ID_num)
        order.production = request.POST.get('production')
        order.consume_location = request.POST.get('consume_location')
        order.save()
        return HttpResponseRedirect(reverse('orders'))


def CancleOrder(request, ID_num):
    Order.objects.filter(ID_num=ID_num).delete()
    return HttpResponseRedirect(reverse('orders'))