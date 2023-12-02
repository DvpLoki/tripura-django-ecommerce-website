from django.conf import settings
from shop.models import SubProduct
from decimal import Decimal


class Cart:
    def __init__(self,request):
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def add(self,product,quantity):
        p_id=str(product.id)
        if p_id not in self.cart:
            self.cart[p_id]={'quantity':0,'price':str(product.selling_price)}   
            
        self.cart[p_id]['quantity']=quantity 

        self.save()



    def remove(self,p_id):
        p_id=str(p_id)
       
        if p_id in self.cart:
            del self.cart[p_id]
            self.save()
        

    def __iter__(self):
        p_ids=self.cart.keys()
        products=SubProduct.objects.filter(id__in=p_ids)
        cart=self.cart.copy()
        for p in products:
            cart[str(p.id)]['product']=p

        for item in cart.values():
            item['price']=Decimal(item['price'])  
            item['total_price']=item['price'] * item['quantity']  
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())   

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())    

    def clear(self):
        del self.session[settings.CART_SESSION_ID] 
        self.save()


    def save(self):
        self.session.modified=True
                           


def cart_context(request):
    return {'cart':Cart(request)}