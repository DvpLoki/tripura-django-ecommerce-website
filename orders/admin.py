from django.contrib import admin
from .models import Order,OrderItem,DeliveryLocation
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

def export_to_csv(modeladmin,request,queryset):
    opt=modeladmin.model._meta
    content_disposition=f'attachment;filename={opt.verbose_name}.csv'
    response=HttpResponse(content_type='text/csv')
    response['content-Disposition']=content_disposition
    writer=csv.writer(response)
    fields=[field for field in opt.get_fields() if not \
            field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row=[]
        for field in fields:
            value=getattr(obj,field.name)
            if isinstance(value,datetime.datetime):
                value=value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response

export_to_csv.short_description='Export to CSV'


def order_detail(obj):
    url=reverse('orders:admin_order_detail',args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url=reverse('orders:order_pdf',args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description='Invoice'

@admin.register(DeliveryLocation)
class DeliveryAdmin(admin.ModelAdmin):
    list_display=['pincode','name','active']

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    raw_id_fields=['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'paid' ,'delivered','deliverydate', order_detail,'pincode','created','modified',order_pdf]

    list_filter=['paid','created','pincode','delivered','deliverydate']
    inlines=[OrderItemInline]
    actions=[export_to_csv]
    list_editable=['paid','delivered','deliverydate']