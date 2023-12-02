from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from io import BytesIO
from xhtml2pdf import pisa
from .models import OrderItem,Order,DeliveryLocation
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

def order_create(request):
    cart=Cart(request)
    if request.method=='POST':
        if cart.get_total_price()>0:
            form=OrderCreateForm(request.POST)
            if form.is_valid():
                order=form.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                        )
                cart.clear()  
                #order_created.delay(order.id)

                return render(request,
                            'orders/created.html',
                            {'order':order}
                            )
        else:
            return redirect(reverse('shop:product_list'))
    else:
        form=OrderCreateForm()

    return render(request,
                  'orders/create.html',
                  {'cart':cart,'order_form':form}
                  )        



@staff_member_required
def admin_order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order':order}
                  )


def order_pdf(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    html=render_to_string('orders/pdf.html',{'order':order})
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']=f'filename=order_{order.id}.pdf'
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    if pisa_status.err:
        return HttpResponse('We had some errors')
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def checkdelivery(request):
    if request.POST:
        pincode=request.POST['pincode']
        if len(pincode) == 6  :
            delivery=DeliveryLocation.objects.filter(pincode=pincode).first()
            if delivery:
                if delivery.active:
                    return HttpResponse(f'<p >{delivery.name} {delivery.pincode} </p>')
                else:
                    return HttpResponse(f'<p class="text-red-500">{pincode} Currently UnAvailable</p>')
                
            else:
                return HttpResponse(f'<p class="text-red-500">{pincode} UnAvailable</p>')
        else:
            return HttpResponse(f'<p class="text-red-500 " >{pincode} invalid Pincode</p>') 
            
    