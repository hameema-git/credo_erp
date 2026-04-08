# from django.urls import path
# from .views import (
#     create_quotation, quotation_detail,
#     add_customer, add_service,
#     invoice_detail, quotation_pdf,
#     invoice_list, invoice_pdf,
#     dashboard, update_payment,
#     payment_receipt_pdf,
#     search_ajax, search_results,
#     receipt_preview,
#     create_invoice ,edit_invoice,edit_quotation,customer_detail ,edit_customer,
#      service_detail,edit_service,delete_invoice,delete_quotation,delete_customer,delete_service 
#      create_lpo,lpo_detail,lpo_pdf# ✅ NEW
# )

# from django.urls import path
# from .views import (
#     create_quotation, quotation_detail,
#     add_customer, add_service,
#     invoice_detail, quotation_pdf,
#     invoice_list, invoice_pdf,
#     dashboard, update_payment,
#     payment_receipt_pdf,
#     search_ajax, search_results,
#     receipt_preview,
#     create_invoice, edit_invoice, edit_quotation,
#     customer_detail, edit_customer,
#     service_detail, edit_service,
#     delete_invoice, delete_quotation,
#     delete_customer, delete_service,   # ✅ FIXED HERE
#     create_lpo, lpo_detail, lpo_pdf    # ✅ NEW
# )

from django.urls import path
from .views import (
    create_quotation, quotation_detail,
    add_customer, add_service,
    invoice_detail, quotation_pdf,
    invoice_list, invoice_pdf,
    dashboard, update_payment,
    payment_receipt_pdf,
    search_ajax, search_results,
    receipt_preview,
    create_invoice, edit_invoice, edit_quotation,
    customer_detail, edit_customer,
    service_detail, edit_service,
    delete_invoice, delete_quotation,
    delete_customer, delete_service,   # ✅ comma added
    create_lpo, lpo_detail, lpo_pdf ,edit_lpo,add_supplier,edit_supplier,delete_supplier,supplier_detail   # ✅ clean line
)
urlpatterns = [

    # -------- QUOTATION --------
    path('quotation/create/', create_quotation, name='create_quotation'),
    path('quotation/<int:pk>/', quotation_detail, name='quotation_detail'),
    path('quotation/pdf/<int:pk>/', quotation_pdf, name='quotation_pdf'),
    path('quotation/<int:pk>/edit/', edit_quotation, name='edit_quotation'),


    # -------- INVOICE --------
    path('invoice/create/', create_invoice, name='create_invoice'),  # 🔥 NEW
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/pdf/<int:pk>/', invoice_pdf, name='invoice_pdf'),
    path('invoices/', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/edit/', edit_invoice, name='edit_invoice'),

    # -------- CUSTOMER & SERVICE --------
    path('add-customer/', add_customer, name='add_customer'),
    path('customer/<int:pk>/', customer_detail, name='customer_detail'),
    path('customer/<int:pk>/edit/', edit_customer, name='edit_customer'),
    path('add-service/', add_service, name='add_service'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
    path('service/<int:pk>/edit/', edit_service, name='edit_service'),

    # -------- PAYMENT --------
    path('invoice/<int:pk>/update-payment/', update_payment, name='update_payment'),
    path('receipt/<int:pk>/pdf/', payment_receipt_pdf, name='receipt_pdf'),
    path('receipt-preview/<int:pk>/', receipt_preview, name='receipt_preview'),

    # -------- SEARCH --------
    path('search/', search_ajax, name='search_ajax'),
    path('search-results/', search_results, name='search_results'),

    # -------- DASHBOARD --------
    path('', dashboard, name='dashboard'),
    path('quotation/delete/<int:pk>/', delete_quotation, name='delete_quotation'),
    path('invoice/delete/<int:pk>/', delete_invoice, name='delete_invoice'),
    path('customer/delete/<int:pk>/', delete_customer, name='delete_customer'),
    path('service/delete/<int:pk>/', delete_service, name='delete_service'),


    path('lpo/create/', create_lpo, name='create_lpo'),
    path('lpo/<int:pk>/', lpo_detail, name='lpo_detail'),
    path('lpo/<int:pk>/pdf/', lpo_pdf, name='lpo_pdf'),
    path('lpo/edit/<int:pk>/', edit_lpo, name='edit_lpo'),

    path('supplier/add/', add_supplier, name='add_supplier'),

    path('supplier/<int:pk>/edit/', edit_supplier, name='edit_supplier'),
    path('supplier/<int:pk>/delete/', delete_supplier, name='delete_supplier'),
    path('supplier/<int:pk>/', supplier_detail, name='supplier_detail'),
]