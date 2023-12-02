from django.db import models
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField()
    is_active=models.BooleanField(default=True)

    class Meta:
        ordering=['name']
        indexes=[
            models.Index(fields=['name']),
        ]

        verbose_name='Category'
        verbose_name_plural='Categories'


    def __str__(self):
        return self.name   

     
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug ])

 
    


class Product(models.Model):

    name=models.CharField(max_length=100)
    slug=models.SlugField()
    description=models.TextField(blank=True)  
    category=models.ForeignKey(Category,related_name='product',on_delete=models.RESTRICT)
  
    class Meta:
        ordering=['name']
        indexes=[
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            
        ]
    def __str__(self):
        return self.name  
    
    

class SubProduct(models.Model):
    product=models.ForeignKey(Product,related_name="subproduct",on_delete=models.CASCADE,db_index=True)

    name=models.CharField(max_length=200,help_text="variant specific name.(Eg. productname=mirchipowder ,subproductname=packed200gm)",null=True)
    slug=models.SlugField()
    is_active=models.BooleanField(default=True,help_text="Product visible")
    is_default=models.BooleanField(default=False,help_text="main item to show")
    cost_price=models.DecimalField(max_digits=6,decimal_places=2,help_text="max 9999.99 ")
    selling_price=models.DecimalField(max_digits=6,decimal_places=2,help_text="max 9999.99 ")
    created_at=models.DateTimeField(auto_now_add=True,editable=False)
    updated_at=models.DateTimeField(auto_now=True)
    

    
    def __str__(self):
        return f'{self.product.name}{self.name}'
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[ self.id ,self.product.slug])
   
    def get_discount(self):
        if self.selling_price<self.cost_price:
            dis=self.cost_price-self.selling_price
            return int((dis/self.cost_price)*100)
    
    

class Attribute(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class AttributeValue(models.Model):
    value=models.CharField(max_length=50)
    attribute=models.ForeignKey(Attribute,related_name="attributevalue",on_delete=models.RESTRICT)
    subproduct=models.ForeignKey(SubProduct,related_name="attributevalue",on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.value    

class StockControl(models.Model):
    last_checked=models.DateField(auto_now_add=True,editable=False)
    units=models.IntegerField(default=0)     
    subproduct=models.OneToOneField(SubProduct,related_name="stock",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="stock control"

    def __str__(self) -> str:
        return str(self.units)    

class Image(models.Model):
    image=models.ImageField(upload_to='products/%Y/%m/%d',blank=True)    
    alternative_text=models.CharField(max_length=50)
    is_feature=models.BooleanField(default=False,help_text="main image to show")
    subproduct=models.ForeignKey(SubProduct,related_name="images",on_delete=models.CASCADE)   

    def __str__(self) -> str:
        return self.alternative_text 
    
   
    




