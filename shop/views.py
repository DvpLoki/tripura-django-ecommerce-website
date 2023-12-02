from django.shortcuts import render,get_object_or_404
from django.template import RequestContext
from django.http import Http404,HttpResponse
from .models import Category, Product,SubProduct
from cart.forms import CartAddProduct
from django.db.models import Prefetch
from render_block import render_block_to_string



def home(request):

    products= (
        Product.objects
        .filter(subproduct__is_active=True)
       
    )

    return render(request,
                  'shop/Home.html',
                  {'products':products}
                  )  


def product_list(request,slug=None):
    category=None
    categories=Category.objects.all()
    
    base_query=SubProduct.objects.select_related('product','stock').filter(is_active=True).prefetch_related('attributevalue','images')

    # Get the category or raise a 404 error if not found
    category = get_object_or_404(Category, slug=slug) if slug else None
    # Modify the query based on the presence of the slug
    products = base_query.filter(product__category=category) if category else base_query

    context={'category':category,'categories':categories,'products':products}
   
    return render(request,
                  'shop/products/list.html',
                  context
                  )    


def product_detail(request,id,slug): 
    product =SubProduct.objects.select_related('product','stock').filter(id=id,product__slug=slug,is_active=True).prefetch_related('attributevalue','images').first()
        
    if not product:
        raise Http404
   
    variations=SubProduct.objects.filter(product__id=product.product.id).prefetch_related('attributevalue')
    form=CartAddProduct()
    context={'product':product,'cart_product_form':form, 'variations':variations}
    if request.htmx:
        reqcontext=RequestContext(request,context)
        html=render_block_to_string('shop/products/detail.html','content',reqcontext)
        return HttpResponse(html)

    return render(request,
                  'shop/products/detail.html',context
                    )