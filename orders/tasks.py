from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    order=Order.objects.get(id=order_id)
    subject=f'Order #{order_id}'
    msg= f'Dear {Order.firstname},\n\n' \
            f'You have successfully placed an order.' \
            f'Your order ID is {order_id}.'
    mail=send_mail(subject,msg,'admin@tripura.com',[order.email])

    return mail