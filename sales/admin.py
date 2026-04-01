from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(PaymentReceipt)
