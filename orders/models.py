from django.db import models
from shop.models import SubProduct
from account.models import CustomUser


class Order(models.Model):

    paymentchoices=[('COD','COD'),('other','other')]

    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100,null=True)
    user=models.ForeignKey(CustomUser,related_name="orders" ,on_delete=models.CASCADE)

    paymentmethod=models.CharField(max_length=5,choices=paymentchoices)

    email=models.EmailField(null=True)
    mobilenumber=models.CharField(max_length=10)

    address=models.CharField(max_length=250)
    pincode=models.CharField(max_length=20)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)

    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)

    delivered=models.BooleanField(default=False)
    deliverydate=models.DateTimeField()

    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {str(self.id)}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)    
    product=models.ForeignKey(SubProduct,related_name='orderitem',on_delete=models.RESTRICT)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price*self.quantity
    

class DeliveryLocation(models.Model):
    pincode=models.CharField(max_length=6,unique=True)
    name=models.CharField(max_length=50,null=True)
    active=models.BooleanField(default=True)  
    estimateddelivery=models.IntegerField(null=True,help_text="delivery in days(eg: 4 = product delivered within 4 days )")  
    deliverycharges=models.DecimalField(max_digits=4,decimal_places=2,help_text="max 99.99 ")

    def __str__(self) -> str:
        return self.pincode
        
