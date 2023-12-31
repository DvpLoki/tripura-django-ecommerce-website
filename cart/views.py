from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProduct
from shop.models import SubProduct


@require_POST
def cart_add(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(SubProduct,id=product_id)
    form=CartAddProduct(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'])

    return redirect('cart:cart_detail')    

@require_POST
def cart_remove(request,product_id):
   
    cart=Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart=Cart(request)

    for item in cart:
        item['update_quantity_form']=CartAddProduct(initial={
            'quantity': item['quantity']
        })

    if request.htmx:
        updatecartitemcount=True
        return render(request,'cart/partialdetail.html',{'cart':cart,'updatecartitemcount':updatecartitemcount})    
    
    return render(request,'cart/detail.html',{'cart':cart})