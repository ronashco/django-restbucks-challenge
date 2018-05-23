from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


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
