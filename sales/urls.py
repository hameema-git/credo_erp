from django.urls import path
# from .views import create_quotation,quotation_detail,quotation_pdf
from .views import create_quotation, quotation_detail,add_customer,add_service,convert_to_invoice,invoice_detail,quotation_pdf,invoice_list,invoice_pdf,dashboard,update_payment,payment_receipt_pdf,search_ajax,search_results,receipt_preview
urlpatterns = [
    path('create/', create_quotation, name='create_quotation'),

    path('detail/<int:pk>/', quotation_detail, name='quotation_detail'),
    # path('pdf/<int:pk>/', quotation_pdf, name='quotation_pdf'),

    path('add_cus/', add_customer,name='add_customer'),

    path('add_ser/', add_service, name='add_service'),
    path('convert-to-invoice/<int:pk>/', convert_to_invoice, name='convert_to_invoice'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),

    path('pdf/<int:pk>/', quotation_pdf, name='quotation_pdf'),

    path('invoice/pdf/<int:pk>/', invoice_pdf, name='invoice_pdf'),
    path('invoices/', invoice_list, name='invoice_list'),
    path('', dashboard, name='dashboard'),
    path('invoice/<int:pk>/update-payment/', update_payment, name='update_payment'),
    path('receipt/<int:pk>/pdf/', payment_receipt_pdf, name='receipt_pdf'),
    path('search/', search_ajax, name='search_ajax'), path('search-results/', search_results, name='search_results'),
    path('receipt-preview/<int:pk>/', receipt_preview, name='receipt_preview'),
]