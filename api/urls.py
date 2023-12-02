
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import shop,cart,orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls',namespace='shop')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('orders/',include('orders.urls',namespace='orders' )),
    path('account/',include('account.urls',namespace='account'))
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)