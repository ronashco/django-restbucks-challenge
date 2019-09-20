from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.template import loader
from .models import Product, Place, Order, OrderStatus


class Index(TemplateView):

    def get(self, *args, **kwargs):
        return render(self.request, 'handler/index.html')


class Login(TemplateView):
    def post(self, *args, **kwargs):
        decoded_request = QueryDict(self.request.body)
        """
        we consider username is email
        """
        username = decoded_request['email']
        password = decoded_request['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('/home/')
        else:
            return render(self.request, 'handler/incorrect.html')


decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class Home(TemplateView):

    def get(self, *args, **kwargs):
        template = loader.get_template('handler/home.html')
        context = {
            'username': self.request.user.username,
            'places': Place.objects.order_by('place'),
            'products': Product.objects.order_by('product'),
            'orders': Order.objects.filter(user=self.request.user)
        }
        return HttpResponse(template.render(context, self.request))


@method_decorator(decorators, name='dispatch')
class Logout(TemplateView):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/')


@method_decorator(decorators, name='dispatch')
class AddOrder(TemplateView):
    def post(self, *args, **kwargs):
        decoded_request = QueryDict(self.request.body)
        username = self.request.user.username
        product = decoded_request['product-choice']
        place = decoded_request['place-choice']
        option = decoded_request['option']
        new_order = Order.objects.create(user=User.objects.get(username=username),
                                         product=Product.objects.get(product=product),
                                         consume_place=Place.objects.get(place=place), option=option,
                                         status=OrderStatus.objects.get(status="waiting"))
        new_order.save()
        return redirect('/home/')


@method_decorator(decorators, name='dispatch')
class DeleteOrder(TemplateView):
    def get(self, *args, **kwargs):

        order_id = self.kwargs['order_id']
        try:
            order = Order.objects.get(id=order_id)
            if order is not None and order.user == self.request.user and str(order.status) == 'waiting':
                order.delete()
                return render(self.request, 'handler/successdelete.html')
            else:
                return render(self.request, 'handler/faileddelete.html')
        except:
            return render(self.request, 'handler/faileddelete.html')
