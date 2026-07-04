from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q
from weasyprint import HTML
from num2words import num2words
from sales.google_drive import GoogleDriveService
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tasks.models import WorkRequest
from .models import Customer, Quotation, QuotationItem, Service


import logging

from sales.google_drive import GoogleDriveService, DOCUMENT_TYPES

logger = logging.getLogger(__name__)

from .models import *
from .utils import generate_quotation_number, generate_invoice_number, generate_receipt_number,generate_lpo_number


# # ---------------- DASHBOARD ----------------
# def dashboard(request):
#     query = request.GET.get('q')

#     customers = Customer.objects.all()
#     quotations = Quotation.objects.all()
#     invoices = Invoice.objects.all()
#     suppliers = Supplier.objects.all()

#     search_type = request.GET.get('type', 'all')

#     if query:
#         if search_type in ['all', 'customer']:
#             customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))

#         if search_type in ['all', 'quotation']:
#             quotations = quotations.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

#         if search_type in ['all', 'invoice']:
#             invoices = invoices.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

#     return render(request, "sales/dashboard.html", {
#         "customers_count": customers.count(),
#         "quotations_count": quotations.count(),
#         "invoices_count": invoices.count(),
#         "recent_quotations": quotations.order_by('-id')[:5],
#         "recent_invoices": invoices.order_by('-id')[:5],
#         "query": query
#     })


from .models import Supplier,PaymentReceipt

def dashboard(request):
    query = request.GET.get('q')

    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()   # ✅ ADD
    quotations = Quotation.objects.all()
    invoices = Invoice.objects.all()
    lpos = LPO.objects.all()
    services=Service.objects.all()
    receipts = PaymentReceipt.objects.all()   # ✅ ADD

    search_type = request.GET.get('type', 'all')

    if query:
        if search_type in ['all', 'customer']:
            customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))

        if search_type in ['all', 'quotation']:
            quotations = quotations.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

        if search_type in ['all', 'invoice']:
            invoices = invoices.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

        if search_type in ['all', 'supplier']:
            suppliers = suppliers.filter(Q(name__icontains=query))  
        if search_type in ['all', 'service']:
            services = services.filter(Q(name__icontains=query))      

        if search_type in ['all', 'lpo']:
            lpos = lpos.filter(Q(number__icontains=query)) 

    return render(request, "sales/dashboard.html", {
        "customers_count": customers.count(),
        "supplier_count": suppliers.count(),   # ✅ ADD THIS 🔥
        "quotations_count": quotations.count(),
        "services_count":services.count(),
        "lpos_count": lpos.count(),
        "invoices_count": invoices.count(),
        "receipts_count": receipts.count(),   # ✅ ADD


        "recent_quotations": quotations.order_by('-id')[:5],
        "recent_invoices": invoices.order_by('-id')[:5],
        "query": query,
        "recent_customers": customers.order_by('-id')[:5],
        "recent_suppliers": suppliers.order_by('-id')[:5],
        "recent_services": services.order_by('-id')[:5],
        "recent_lpos": lpos.order_by('-id')[:5],
        "recent_receipts": receipts.order_by('-id')[:5],
        
    })

# ---------------- CUSTOMER ----------------
def add_customer(request):
    if request.method == "POST":
        Customer.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            trn_number=request.POST.get("trn_number")  # ✅ ADD
        )
        return redirect('dashboard')   # 🔥 updated

    return render(request, "customers/add_customer.html")

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)

    quotations = customer.quotation_set.all()
    invoices = customer.invoice_set.all()

    return render(request, "sales/customer_detail.html", {
        "customer": customer,
        "quotations": quotations,
        "invoices": invoices
    })

def edit_customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)

    if request.method == "POST":
        customer.name = request.POST.get("name")
        customer.phone = request.POST.get("phone")
        customer.email = request.POST.get("email")
        customer.address = request.POST.get("address")
        customer.trn_number = request.POST.get("trn_number")

        customer.save()

        return redirect("dashboard")  # or customer_detail if you created it

    return render(request, "sales/edit_customer.html", {
        "customer": customer
    })


# ---------------- SERVICE ----------------
def add_service(request):
    if request.method == "POST":
        Service.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description")
        )
        return redirect('dashboard')   # 🔥 updated

    return render(request, "services/add_service.html")
def service_detail(request, pk):
    service = get_object_or_404(Service, id=pk)

    return render(request, "sales/service_detail.html", {
        "service": service
    })

def edit_service(request, pk):
    service = get_object_or_404(Service, id=pk)

    if request.method == "POST":
        service.name = request.POST.get("name")
        service.price = request.POST.get("price")
        service.description = request.POST.get("description")

        service.save()

        return redirect("dashboard")

    return render(request, "sales/edit_service.html", {
        "service": service
    })

# ---------------- QUOTATION ----------------
def create_quotation(request):
    customers = Customer.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        customer = Customer.objects.get(id=request.POST.get("customer"))
        note = request.POST.get("note")

        quotation = Quotation.objects.create(
            number=generate_quotation_number(),
            customer=customer,
            attention=request.POST.get("attention") or "",
            sales_person=request.POST.get("sales_person") or "",
            note=note 
            # trn_number=customer.trn_number   # ✅ ADD HERE
        )

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = 0

        for i in range(len(quantities)):
            qty = int(quantities[i])
            price = float(prices[i])
            total = qty * price

            QuotationItem.objects.create(
                quotation=quotation,
                description=descriptions[i],
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        quotation.subtotal = subtotal
        quotation.vat = subtotal * 0.05
        quotation.total = quotation.subtotal + quotation.vat
        quotation.save()

        return redirect("quotation_detail", pk=quotation.id)

    return render(request, "sales/create_quotation.html", {
        "customers": customers,
        "services": services
    })


def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, id=pk)

    return render(request, "sales/quotation_detail.html", {
        "quotation": quotation
    })


# def quotation_pdf(request, pk):
#     quotation = get_object_or_404(Quotation, id=pk)

#     html = render_to_string("sales/quotation_pdf.html", {
#         "quotation": quotation
#     })

#     pdf = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="quotation_{quotation.number}.pdf"'

#     return response


# def quotation_pdf(request, pk):
#     quotation = get_object_or_404(Quotation, id=pk)

#     # html = render_to_string(
#     #     "sales/quotation_pdf.html",
#     #     {"quotation": quotation},
#     #     request=request   # ✅ ADD THIS
#     # )

#     # pdf = HTML(
#     #     string=html,
#     #     base_url=request.build_absolute_uri('/')  # OK
#     # ).write_pdf()

#     html = render_to_string(
#     "sales/quotation_pdf.html",
#     {
#         "quotation": quotation,
#         "base_url": request.build_absolute_uri('/')   # ✅ ADD THIS
#     },
#         request=request
#     )

#     pdf = HTML(
#         string=html,
#         base_url=request.build_absolute_uri()
#     ).write_pdf()

#     return HttpResponse(pdf, content_type='application/pdf')

# def quotation_pdf(request, pk):
#     quotation = get_object_or_404(Quotation, id=pk)

#     base_url = f"{request.scheme}://{request.get_host()}/"

#     html = render_to_string(
#         "sales/quotation_pdf.html",
#         {
#             "quotation": quotation,
#             "base_url": base_url
#         },
#         request=request
#     )

#     pdf = HTML(
#         string=html,
#         base_url=base_url   # ✅ CRITICAL
#     ).write_pdf()

#     return HttpResponse(pdf, content_type='application/pdf')

import os
from django.conf import settings
from weasyprint import HTML

# def quotation_pdf(request, pk):
#     quotation = get_object_or_404(Quotation, id=pk)

#     html = render_to_string(
#         "sales/quotation_pdf.html",
#         {
#             "quotation": quotation,
#             "static_path": settings.STATIC_ROOT  # ✅ IMPORTANT
#         },
#         request=request
#     )

#     pdf = HTML(string=html).write_pdf()

#     return HttpResponse(pdf, content_type='application/pdf')

# def quotation_pdf(request, pk):
#     quotation = get_object_or_404(Quotation, id=pk)

#     html = render_to_string(
#         "sales/quotation_pdf.html",
#         {
#             "quotation": quotation,
#             "static_path": settings.STATIC_ROOT
#         },
#         request=request
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = (
#         f'inline; filename="quotation_{quotation.number}.pdf"'
#     )

#     return response

# def quotation_pdf(request, pk):
#     """
#     Generate Quotation PDF, upload it to Google Drive,
#     and return the PDF to the browser.
#     """

#     quotation = get_object_or_404(Quotation, id=pk)

#     html = render_to_string(
#         "sales/quotation_pdf.html",
#         {
#             "quotation": quotation,
#             "static_path": settings.STATIC_ROOT,
#         },
#         request=request,
#     )

#     pdf = HTML(
#         string=html,
#         base_url=request.build_absolute_uri("/"),
#     ).write_pdf()

#     # -------------------------------------------------------
#     # Backup PDF to Google Drive
#     # -------------------------------------------------------
#     try:
#         drive_result = GoogleDriveService().upload_document(
#             customer_name=quotation.customer.company_name,
#             document_type=DOCUMENT_TYPES["quotation"],
#             file_name=f"{quotation.number}.pdf",
#             pdf_bytes=pdf,
#         )

#         logger.info(
#             "Quotation '%s' uploaded to Google Drive successfully. URL: %s",
#             quotation.number,
#             drive_result["url"],
#         )

#     except Exception:
#         # Do NOT stop the user from downloading the PDF
#         logger.exception(
#             "Failed to upload Quotation '%s' to Google Drive.",
#             quotation.number,
#         )

#     response = HttpResponse(
#         pdf,
#         content_type="application/pdf",
#     )

#     response["Content-Disposition"] = (
#         f'inline; filename="{quotation.number}.pdf"'
#     )

#     return response

def quotation_pdf(request, pk):
    """
    Generate Quotation PDF, upload it to Google Drive,
    and return the PDF to the browser.
    """

    quotation = get_object_or_404(Quotation, id=pk)

    html = render_to_string(
        "sales/quotation_pdf.html",
        {
            "quotation": quotation,
            "static_path": settings.STATIC_ROOT,
        },
        request=request,
    )

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # -------------------------------------------------------
    # Backup PDF to Google Drive
    # -------------------------------------------------------
    try:
        drive_result = GoogleDriveService().upload_document(
            customer_name=quotation.customer.name,
            document_type=DOCUMENT_TYPES["quotation"],
            file_name=f"{quotation.number}.pdf",
            pdf_bytes=pdf,
        )

        # Save Google Drive URL
        quotation.google_drive_url = drive_result["url"]
        quotation.save(update_fields=["google_drive_url"])

        logger.info(
            "Quotation '%s' uploaded successfully to Google Drive.",
            quotation.number,
        )

    except Exception:
        logger.exception(
            "Failed to upload Quotation '%s' to Google Drive.",
            quotation.number,
        )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{quotation.number}.pdf"'
    )

    return response

# ---------------- INVOICE (NEW FLOW) ----------------
def create_invoice(request):
    customers = Customer.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        customer = Customer.objects.get(id=request.POST.get("customer"))
        note = request.POST.get("note")

        invoice = Invoice.objects.create(
            number=generate_invoice_number(),
            customer=customer,
            attention=request.POST.get("attention") or "",
            sales_person=request.POST.get("sales_person") or "",
            note=note
            # trn_number=customer.trn_number   # ✅ ADD HERE
        )

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = 0

        for i in range(len(quantities)):
            qty = int(quantities[i])
            price = float(prices[i])
            total = qty * price

            InvoiceItem.objects.create(
                invoice=invoice,
                description=descriptions[i],
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        invoice.subtotal = subtotal
        invoice.vat = subtotal * 0.05
        invoice.total = invoice.subtotal + invoice.vat
        invoice.save()

        return redirect("invoice_detail", pk=invoice.id)

    return render(request, "sales/create_invoice.html", {
        "customers": customers,
        "services": services
    })


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

    return render(request, "sales/invoice_detail.html", {
        "invoice": invoice,
        "receipt": receipt
    })


def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-id')

    return render(request, "sales/invoice_list.html", {
        "invoices": invoices
    })


# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     # html = render_to_string("sales/invoice_pdf.html", {
#     #     "invoice": invoice
#     # })

#     html = render_to_string(
#     "sales/invoice_pdf.html",
#     {"invoice": invoice},
#     request=request   # ✅ ADD THIS
# )

#     pdf = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="invoice_{invoice.number}.pdf"'

#     return response

# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     html = render_to_string(
#         "sales/invoice_pdf.html",
#         {
#             "invoice": invoice,
#             "static_path": settings.STATIC_ROOT   # ✅ IMPORTANT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT   # ✅ CRITICAL FIX
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="invoice_{invoice.number}.pdf"'

#     return response

# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     html = render_to_string(
#         "sales/invoice_pdf.html",
#         {
#             "invoice": invoice,
#             "static_path": settings.STATIC_ROOT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     # Google Drive upload will be added here

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = (
#         f'inline; filename="invoice_{invoice.number}.pdf"'
#     )

#     return response

# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     html = render_to_string(
#         "sales/invoice_pdf.html",
#         {
#             "invoice": invoice,
#             "static_path": settings.STATIC_ROOT,
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     # -------------------------------------------------------
#     # Automatically upload PDF to Google Drive
#     # -------------------------------------------------------
#     try:
#         drive_result = GoogleDriveService().upload_document(
#             customer_name=invoice.customer.company_name,
#             document_type=DOCUMENT_TYPES["invoice"],
#             file_name=f"{invoice.number}.pdf",
#             pdf_bytes=pdf,
#         )

#         logger.info(
#             "Invoice uploaded successfully to Google Drive: %s",
#             drive_result["url"],
#         )

#         # Optional:
#         # invoice.google_drive_url = drive_result["url"]
#         # invoice.save(update_fields=["google_drive_url"])

#     except Exception:
#         logger.exception(
#             "Failed to upload invoice '%s' to Google Drive.",
#             invoice.number,
#         )

#     response = HttpResponse(
#         pdf,
#         content_type="application/pdf",
#     )

#     response["Content-Disposition"] = (
#         f'inline; filename="invoice_{invoice.number}.pdf"'
#     )

#     return response


def invoice_pdf(request, pk):
    """
    Generate Invoice PDF, upload it to Google Drive,
    and return the PDF to the browser.
    """

    invoice = get_object_or_404(Invoice, id=pk)

    html = render_to_string(
        "sales/invoice_pdf.html",
        {
            "invoice": invoice,
            "static_path": settings.STATIC_ROOT,
        }
    )

    pdf = HTML(
        string=html,
        base_url=settings.STATIC_ROOT,
    ).write_pdf()

    # -------------------------------------------------------
    # Backup PDF to Google Drive
    # -------------------------------------------------------
    # try:
    #     drive_result = GoogleDriveService().upload_document(
    #         customer_name=invoice.customer.company_name,
    #         document_type=DOCUMENT_TYPES["invoice"],
    #         file_name=f"{invoice.number}.pdf",
    #         pdf_bytes=pdf,
    #     )

    #     logger.info(
    #         "Invoice '%s' uploaded to Google Drive successfully. URL: %s",
    #         invoice.number,
    #         drive_result["url"],
    #     )

    # except Exception:
    #     # Do NOT stop the user from downloading the PDF
    #     logger.exception(
    #         "Failed to upload Invoice '%s' to Google Drive.",
    #         invoice.number,
    #     )

    try:
        drive_result = GoogleDriveService().upload_document(
            customer_name=invoice.customer.name,
            document_type=DOCUMENT_TYPES["invoice"],
            file_name=f"{invoice.number}.pdf",
            pdf_bytes=pdf,
        )

        invoice.google_drive_url = drive_result["url"]
        invoice.save(update_fields=["google_drive_url"])

        logger.info(
            "Invoice '%s' uploaded successfully to Google Drive.",
            invoice.number,
        )

    except Exception:
        logger.exception(
            "Failed to upload Invoice '%s' to Google Drive.",
            invoice.number,
        )

    # -------------------------------------------------------
    # Return PDF to browser
    # -------------------------------------------------------
    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{invoice.number}.pdf"'
    )

    return response


# ---------------- PAYMENT ----------------
# def update_payment(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     if request.method == "POST":
#         paid = request.POST.get("paid_amount")

#         if paid:
#             invoice.paid_amount = float(paid)
#             invoice.save()

#             PaymentReceipt.objects.create(
#                 invoice=invoice,
#                 receipt_number=generate_receipt_number(),
#                 amount_paid=invoice.paid_amount,
#                 payment_method=invoice.payment_method or 'bank',
#                 # received_by="Admin"
#                 received_by=request.POST.get("received_by", "Admin")
#             )

#     return redirect('invoice_detail', pk=pk)

def update_payment(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)

    if request.method == "POST":
        paid = request.POST.get("paid_amount")

        if paid:
            invoice.paid_amount = float(paid)
            invoice.save()

    return redirect('invoice_detail', pk=pk)


# def payment_receipt_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)
#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     amount_words = num2words(receipt.amount_paid, lang='en').title() + " AED Only"

#     html = render_to_string("sales/payment_receipt_pdf.html", {
#         "receipt": receipt,
#         # "custom_description": custom_description, 
#         # "short_discription":short_discription,
    
#         "amount_words": amount_words
#     })

#     pdf = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

#     return response

# def payment_receipt_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)
#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     amount_words = num2words(receipt.amount_paid, lang='en').title() + " AED Only"

#     html = render_to_string(
#         "sales/payment_receipt_pdf.html",
#         {
#             "receipt": receipt,
#             "amount_words": amount_words,
#             "static_path": settings.STATIC_ROOT   # ✅ VERY IMPORTANT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT   # ✅ CRITICAL FIX
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

#     return response

# def payment_receipt_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)
#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     if not receipt:
#         return HttpResponse("No payment receipt found for this invoice")

#     amount_words = num2words(receipt.amount_paid, lang='en').title() + " AED Only"

#     html = render_to_string(
#         "sales/payment_receipt_pdf.html",
#         {
#             "receipt": receipt,
#             "amount_words": amount_words,
#             "static_path": settings.STATIC_ROOT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

#     return response


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from num2words import num2words
from django.conf import settings

from .models import PaymentReceipt


# def payment_receipt_pdf(request, pk):

#     # ✅ GET RECEIPT DIRECTLY
#     receipt = get_object_or_404(
#         PaymentReceipt,
#         id=pk
#     )

#     amount_words = (
#         num2words(
#             receipt.amount_paid,
#             lang='en'
#         ).title()
#         + " AED Only"
#     )

#     html = render_to_string(
#         "sales/payment_receipt_pdf.html",
#         {
#             "receipt": receipt,
#             "amount_words": amount_words,
#             "static_path": settings.STATIC_ROOT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     response = HttpResponse(
#         pdf,
#         content_type='application/pdf'
#     )

#     response['Content-Disposition'] = (
#         f'inline; filename="receipt_{receipt.receipt_number}.pdf"'
#     )

#     return response


def payment_receipt_pdf(request, pk):
    """
    Generate Payment Receipt PDF, upload it to Google Drive,
    and return the PDF to the browser.
    """

    receipt = get_object_or_404(
        PaymentReceipt,
        id=pk
    )

    amount_words = (
        num2words(
            receipt.amount_paid,
            lang="en"
        ).title()
        + " AED Only"
    )

    html = render_to_string(
        "sales/payment_receipt_pdf.html",
        {
            "receipt": receipt,
            "amount_words": amount_words,
            "static_path": settings.STATIC_ROOT,
        }
    )

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # -------------------------------------------------------
    # Backup PDF to Google Drive
    # -------------------------------------------------------
    try:
        drive_result = GoogleDriveService().upload_document(
            customer_name=receipt.invoice.customer.name,
            document_type=DOCUMENT_TYPES["receipt"],
            file_name=f"{receipt.receipt_number}.pdf",
            pdf_bytes=pdf,
        )

        # Save Google Drive URL
        receipt.google_drive_url = drive_result["url"]
        receipt.save(update_fields=["google_drive_url"])

        logger.info(
            "Receipt '%s' uploaded successfully to Google Drive.",
            receipt.receipt_number,
        )

    except Exception:
        logger.exception(
            "Failed to upload Receipt '%s' to Google Drive.",
            receipt.receipt_number,
        )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{receipt.receipt_number}.pdf"'
    )

    return response

# ---------------- SEARCH ----------------
# def search_ajax(request):
#     query = request.GET.get('q')

#     customers = list(Customer.objects.filter(name__icontains=query).values('id','name')[:5])
#     quotations = list(Quotation.objects.filter(number__icontains=query).values('id','number')[:5])
#     invoices = list(Invoice.objects.filter(number__icontains=query).values('id','number')[:5])

#     return JsonResponse({
#         "customers": customers,
#         "quotations": quotations,
#         "invoices": invoices
#     })

def search_ajax(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')

    customers = []
    quotations = []
    invoices = []
    services = []
    lpos = []
    suppliers=[]
    receipts=[]
    

    if search_type == "customer" or not search_type:
        customers = list(Customer.objects.filter(name__icontains=query).values('id','name')[:5])

    if search_type == "quotation" or not search_type:
        quotations = list(Quotation.objects.filter(number__icontains=query).values('id','number')[:5])

    if search_type == "invoice" or not search_type:
        invoices = list(Invoice.objects.filter(number__icontains=query).values('id','number')[:5])
    if search_type == "service" or not search_type:
        services = list(Service.objects.filter(name__icontains=query).values('id','name')[:5])

    if search_type == "supplier" or not search_type:
        suppliers = list(Supplier.objects.filter(name__icontains=query).values('id','name')[:5])

    if search_type == "lpo" or not search_type:
        lpos = list(LPO.objects.filter(number__icontains=query).values('id','number')[:5])

    if search_type == "receipt" or not search_type:
        receipts = list(
            PaymentReceipt.objects.filter(
                receipt_number__icontains=query
            ).values('id', 'receipt_number')[:20]
        )

    return JsonResponse({
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices,
        "services":services,
        "suppliers":suppliers,
        "lpos":lpos,
        "receipts": receipts,
    })


# def search_results(request):
#     query = request.GET.get('q')

#     return render(request, "sales/search_results.html", {
#         "customers": Customer.objects.filter(name__icontains=query),
#         "quotations": Quotation.objects.filter(number__icontains=query),
#         "invoices": Invoice.objects.filter(number__icontains=query),
#         "query": query
#     })


# def search_results(request):
#     # query = request.GET.get('q')
#     query = request.GET.get('q', '').strip()
#     search_type = request.GET.get('type')  # 🔥 ADD THIS

#     customers = Customer.objects.none()
#     quotations = Quotation.objects.none()
#     invoices = Invoice.objects.none()
#     services = Service.objects.none()
#     suppliers = Supplier.objects.none()
#     lpos = LPO.objects.none()
#     receipts = PaymentReceipt.objects.none()

#     # 🔥 APPLY FILTER
# #     if search_type == "customer":
# #         customers = Customer.objects.filter(name__icontains=query)

# #     elif search_type == "quotation":
# #         quotations = Quotation.objects.filter(number__icontains=query)

# #     elif search_type == "invoice":
# #         invoices = Invoice.objects.filter(number__icontains=query)
# #     elif search_type == "service":
# #         services = Service.objects.filter(name__icontains=query)

# #     elif search_type == "supplier":
# #         suppliers = Supplier.objects.filter(name__icontains=query)

# #     elif search_type == "lpo":
# #         lpos = LPO.objects.filter(number__icontains=query)


# #     elif search_type == "receipt":
# #         receipts = PaymentReceipt.objects.filter(
# #             receipt_number__icontains=query
# #         )
# #     else:  # default = all
# #         customers = Customer.objects.filter(name__icontains=query)
# #         quotations = Quotation.objects.filter(number__icontains=query)
# #         invoices = Invoice.objects.filter(number__icontains=query)
# #         services = Service.objects.filter(name__icontains=query)
# #         suppliers = Supplier.objects.filter(name__icontains=query)
# #         lpos = LPO.objects.filter(number__icontains=query)
# #         receipts = PaymentReceipt.objects.filter(
# #     receipt_number__icontains=query
# # )

#     # CUSTOMER
#     if search_type == "customer":
#         customers = Customer.objects.filter(name__icontains=query) if query else Customer.objects.all()

#     # QUOTATION
#     elif search_type == "quotation":
#         quotations = Quotation.objects.filter(number__icontains=query) if query else Quotation.objects.all()

#     # INVOICE
#     elif search_type == "invoice":
#         invoices = Invoice.objects.filter(number__icontains=query) if query else Invoice.objects.all()

#     # SERVICE
#     elif search_type == "service":
#         services = Service.objects.filter(name__icontains=query) if query else Service.objects.all()

#     # SUPPLIER
#     elif search_type == "supplier":
#         suppliers = Supplier.objects.filter(name__icontains=query) if query else Supplier.objects.all()

#     # LPO
#     elif search_type == "lpo":
#         lpos = LPO.objects.filter(number__icontains=query) if query else LPO.objects.all()

#     # RECEIPTS
#     elif search_type == "receipt":
#         receipts = (
#             PaymentReceipt.objects.filter(receipt_number__icontains=query)
#             if query else PaymentReceipt.objects.all()
#         )

#     # ALL
#     else:
#         customers = Customer.objects.filter(name__icontains=query) if query else Customer.objects.all()
#         quotations = Quotation.objects.filter(number__icontains=query) if query else Quotation.objects.all()
#         invoices = Invoice.objects.filter(number__icontains=query) if query else Invoice.objects.all()
#         services = Service.objects.filter(name__icontains=query) if query else Service.objects.all()
#         suppliers = Supplier.objects.filter(name__icontains=query) if query else Supplier.objects.all()
#         lpos = LPO.objects.filter(number__icontains=query) if query else LPO.objects.all()
#         receipts = (
#             PaymentReceipt.objects.filter(receipt_number__icontains=query)
#             if query else PaymentReceipt.objects.all()
#         )

#     return render(request, "sales/search_results.html", {
#         "customers": customers,
#         "quotations": quotations,
#         "invoices": invoices,
#         "query": query,
#         "services": services,
#         "search_type": search_type ,  # 🔥 PASS THIS
#         "suppliers": suppliers,
#         "lpos": lpos,
#         "receipts": receipts,
#     })


from django.shortcuts import render

def search_results(request):

    query = request.GET.get("q", "").strip()
    search_type = request.GET.get("type")

    customers = Customer.objects.none()
    quotations = Quotation.objects.none()
    invoices = Invoice.objects.none()
    services = Service.objects.none()
    suppliers = Supplier.objects.none()
    lpos = LPO.objects.none()
    receipts = PaymentReceipt.objects.none()

    # -----------------------------
    # CUSTOMER
    # -----------------------------
    if search_type == "customer":
        customers = (
            Customer.objects.filter(name__icontains=query)
            if query else Customer.objects.all()
        )

    # -----------------------------
    # QUOTATION
    # -----------------------------
    elif search_type == "quotation":
        quotations = (
            Quotation.objects.filter(number__icontains=query)
            if query else Quotation.objects.all()
        )

    # -----------------------------
    # INVOICE
    # -----------------------------
    elif search_type == "invoice":
        invoices = (
            Invoice.objects.filter(number__icontains=query)
            if query else Invoice.objects.all()
        )

    # -----------------------------
    # SERVICE
    # -----------------------------
    elif search_type == "service":
        services = (
            Service.objects.filter(name__icontains=query)
            if query else Service.objects.all()
        )

    # -----------------------------
    # SUPPLIER
    # -----------------------------
    elif search_type == "supplier":
        suppliers = (
            Supplier.objects.filter(name__icontains=query)
            if query else Supplier.objects.all()
        )

    # -----------------------------
    # LPO
    # -----------------------------
    elif search_type == "lpo":
        lpos = (
            LPO.objects.filter(number__icontains=query)
            if query else LPO.objects.all()
        )

    # -----------------------------
    # RECEIPT
    # -----------------------------
    elif search_type == "receipt":
        receipts = (
            PaymentReceipt.objects.filter(receipt_number__icontains=query)
            if query else PaymentReceipt.objects.all()
        )

    # -----------------------------
    # ALL
    # -----------------------------
    else:
        customers = (
            Customer.objects.filter(name__icontains=query)
            if query else Customer.objects.all()
        )

        quotations = (
            Quotation.objects.filter(number__icontains=query)
            if query else Quotation.objects.all()
        )

        invoices = (
            Invoice.objects.filter(number__icontains=query)
            if query else Invoice.objects.all()
        )

        services = (
            Service.objects.filter(name__icontains=query)
            if query else Service.objects.all()
        )

        suppliers = (
            Supplier.objects.filter(name__icontains=query)
            if query else Supplier.objects.all()
        )

        lpos = (
            LPO.objects.filter(number__icontains=query)
            if query else LPO.objects.all()
        )

        receipts = (
            PaymentReceipt.objects.filter(receipt_number__icontains=query)
            if query else PaymentReceipt.objects.all()
        )

    # -----------------------------
    # SORTING
    # -----------------------------
    customers = customers.order_by("name")
    quotations = quotations.order_by("id")
    invoices = invoices.order_by("id")
    services = services.order_by("name")
    suppliers = suppliers.order_by("name")
    lpos = lpos.order_by("id")
    receipts = receipts.order_by("id")

    return render(request, "sales/search_results.html", {
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices,
        "services": services,
        "suppliers": suppliers,
        "lpos": lpos,
        "receipts": receipts,
        "query": query,
        "search_type": search_type,
    })


# ---------------- RECEIPT PREVIEW ----------------
# def receipt_preview(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     if request.method == "POST":
#         base_url = reverse("receipt_pdf", args=[invoice.id])

#         query_string = urlencode({
#             "desc": request.POST.get("description"),
#             "received_by": request.POST.get("received_by"),
#             "payment_method": request.POST.get("payment_method")
#         })

#         return redirect(f"{base_url}?{query_string}")

#     return render(request, "sales/receipt_preview.html", {
#         "invoice": invoice
#     })

# def receipt_preview(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     if request.method == "POST":
#         description = request.POST.get("description")
#         received_by = request.POST.get("received_by")
#         payment_method = request.POST.get("payment_method")

#         # ✅ CREATE RECEIPT HERE
#         receipt = PaymentReceipt.objects.create(
#             invoice=invoice,
#             receipt_number=generate_receipt_number(),
#             amount_paid=invoice.paid_amount,
#             payment_method=payment_method,
#             received_by=received_by
#         )

#         base_url = reverse("receipt_pdf", args=[invoice.id])

#         query_string = urlencode({
#             "desc": description,
#             "received_by": received_by,
#             "payment_method": payment_method
#         })

#         return redirect(f"{base_url}?{query_string}")

#     return render(request, "sales/receipt_preview.html", {
#         "invoice": invoice
#     })


def receipt_preview(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)

    if request.method == "POST":
        description = request.POST.get("description")
        received_by = request.POST.get("received_by")
        payment_method = request.POST.get("payment_method")

        # ✅ SAVE TO DB
        receipt = PaymentReceipt.objects.create(
            invoice=invoice,
            receipt_number=generate_receipt_number(),
            amount_paid=invoice.paid_amount,
            # payment_method=payment_method,
            payment_method=payment_method or "bank",   # ✅ DEFAULT FIX
            received_by=received_by,
            short_description=description   # 🔥 HERE
            
        )

        return redirect("receipt_pdf", pk=receipt.id)

    return render(request, "sales/receipt_preview.html", {
        "invoice": invoice
    })

def edit_quotation(request, pk):
    quotation = get_object_or_404(Quotation, id=pk)
    customers = Customer.objects.all()

    if request.method == "POST":
        quotation.customer_id = request.POST.get("customer")
        quotation.attention = request.POST.get("attention")
        quotation.sales_person = request.POST.get("sales_person")
        quotation.note= request.POST.get("note")

        quotation.save()

        # 🔥 DELETE OLD ITEMS
        quotation.items.all().delete()

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = 0

        for i in range(len(quantities)):
            qty = int(quantities[i])
            price = float(prices[i])
            total = qty * price

            QuotationItem.objects.create(
                quotation=quotation,
                description=descriptions[i],
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        quotation.subtotal = subtotal
        quotation.vat = subtotal * 0.05
        quotation.total = quotation.subtotal + quotation.vat
        quotation.save()

        return redirect("quotation_detail", pk=quotation.id)

    return render(request, "sales/edit_quotation.html", {
        "quotation": quotation,
        "customers": customers,
        "services": Service.objects.all()
    })

def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    customers = Customer.objects.all()

    if request.method == "POST":
        invoice.customer_id = request.POST.get("customer")
        invoice.attention = request.POST.get("attention")
        invoice.sales_person = request.POST.get("sales_person")
        invoice.note = request.POST.get("note")

        invoice.save()

        # 🔥 DELETE OLD ITEMS
        invoice.items.all().delete()

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = 0

        for i in range(len(quantities)):
            qty = int(quantities[i])
            price = float(prices[i])
            total = qty * price

            InvoiceItem.objects.create(
                invoice=invoice,
                description=descriptions[i],
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        invoice.subtotal = subtotal
        invoice.vat = subtotal * 0.05
        invoice.total = invoice.subtotal + invoice.vat
        invoice.save()

        return redirect("invoice_detail", pk=invoice.id)

    return render(request, "sales/edit_invoice.html", {
        "invoice": invoice,
        "customers": customers
    })

def delete_quotation(request, pk):
    q = get_object_or_404(Quotation, id=pk)
    q.delete()
    return redirect('dashboard')


def delete_invoice(request, pk):
    i = get_object_or_404(Invoice, id=pk)
    i.delete()
    return redirect('dashboard')

def delete_customer(request, pk):
    c = get_object_or_404(Customer, id=pk)
    c.delete()
    return redirect('dashboard')


def delete_service(request, pk):
    s = get_object_or_404(Service, id=pk)
    s.delete()
    return redirect('dashboard')

# def create_lpo(request):
#     customers = Customer.objects.all()

#     if request.method == "POST":
#         supplier = Customer.objects.get(id=request.POST.get("supplier"))

#         lpo = LPO.objects.create(
#             number=generate_lpo_number(),
#             supplier=supplier,
#             note=request.POST.get("note")
#         )

#         descriptions = request.POST.getlist("description")
#         quantities = request.POST.getlist("quantity")
#         prices = request.POST.getlist("price")

#         subtotal = 0

#         for i in range(len(quantities)):
#             qty = int(quantities[i])
#             price = float(prices[i])
#             total = qty * price

#             LPOItem.objects.create(
#                 lpo=lpo,
#                 description=descriptions[i],
#                 quantity=qty,
#                 price=price,
#                 total=total
#             )

#             subtotal += total

#         lpo.subtotal = subtotal
#         lpo.vat = subtotal * 0.05
#         lpo.total = lpo.subtotal + lpo.vat
#         lpo.save()

#         return redirect("lpo_detail", pk=lpo.id)

#     return render(request, "sales/create_lpo.html", {
#         "customers": customers
#     })


from .models import Supplier   # ✅ make sure this is imported

# def create_lpo(request):
#     suppliers = Supplier.objects.all()   # ✅ CHANGE

#     if request.method == "POST":
#         supplier = Supplier.objects.get(id=request.POST.get("supplier"))  # ✅ CHANGE

#         lpo = LPO.objects.create(
#             number=generate_lpo_number(),
#             supplier=supplier,
#             note=request.POST.get("note"),
#             delivery_date=request.POST.get("delivery_date") or None  # ✅ optional
#         )

#         descriptions = request.POST.getlist("description")
#         quantities = request.POST.getlist("quantity")
#         prices = request.POST.getlist("price")

#         subtotal = 0

#         for i in range(len(quantities)):
#             qty = int(quantities[i])
#             price = float(prices[i])
#             total = qty * price

#             LPOItem.objects.create(
#                 lpo=lpo,
#                 description=descriptions[i],
#                 quantity=qty,
#                 price=price,
#                 total=total
#             )

#             subtotal += total

#         lpo.subtotal = subtotal
#         lpo.vat = subtotal * 0.05
#         lpo.total = subtotal + lpo.vat
#         lpo.save()

#         return redirect("lpo_detail", pk=lpo.id)

#     return render(request, "sales/create_lpo.html", {
#         "suppliers": suppliers   # ✅ CHANGE
#     })


from decimal import Decimal

# def create_lpo(request):
#     suppliers = Supplier.objects.all()

#     if request.method == "POST":
#         supplier = Supplier.objects.get(id=request.POST.get("supplier"))

#         lpo = LPO.objects.create(
#             number=generate_lpo_number(),
#             supplier=supplier,
#             note=request.POST.get("note"),
#             delivery_date=request.POST.get("delivery_date") or None
#         )

#         descriptions = request.POST.getlist("description")
#         quantities = request.POST.getlist("quantity")
#         prices = request.POST.getlist("price")

#         subtotal = Decimal("0")
#         total_vat = Decimal("0")
#         grand_total = Decimal("0")

#         # for i in range(len(quantities)):
#         #     qty = Decimal(quantities[i])
#         #     price = Decimal(prices[i])

#         #     item_total = qty * price
#         #     item_vat = item_total * Decimal("0.05")
#         #     item_grand = item_total + item_vat

#         #     LPOItem.objects.create(
#         #         lpo=lpo,
#         #         description=descriptions[i],
#         #         quantity=qty,
#         #         price=price,
#         #         total=item_grand   # ✅ STORE FINAL (WITH VAT)
#         #     )

#         #     subtotal += item_total
#         #     total_vat += item_vat
#         #     grand_total += item_grand


#         from decimal import Decimal

#     for i in range(len(quantities)):
#         if not descriptions[i].strip():
#             continue   # skip empty rows

#         qty = Decimal(quantities[i])
#         price = Decimal(prices[i])

#         item_total = qty * price
#         item_vat = item_total * Decimal("0.05")
#         item_grand = item_total + item_vat

#         LPOItem.objects.create(
#             lpo=lpo,
#             description=descriptions[i],
#             quantity=qty,
#             price=price,
#             vat=item_vat,        # ✅ MUST ADD THIS
#             total=item_grand     # ✅ FINAL WITH VAT
#         )

#         subtotal += item_total
#         total_vat += item_vat
#         grand_total += item_grand

#         lpo.subtotal = subtotal
#         lpo.vat = total_vat
#         lpo.total = grand_total
#         lpo.save()

#         return redirect("lpo_detail", pk=lpo.id)

#     return render(request, "sales/create_lpo.html", {
#         "suppliers": suppliers
#     })

from decimal import Decimal

def create_lpo(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        supplier = Supplier.objects.get(id=request.POST.get("supplier"))

        lpo = LPO.objects.create(
            number=generate_lpo_number(),
            quote_ref=request.POST.get("quote_ref"),   # ✅ ADD THIS LINE
            supplier=supplier,
            note=request.POST.get("note"),
            delivery_date=request.POST.get("delivery_date") or None
        )

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = Decimal("0")
        total_vat = Decimal("0")
        grand_total = Decimal("0")

        # ✅ LOOP MUST BE INSIDE POST
        for i in range(len(quantities)):
            if not descriptions[i].strip():
                continue

            qty = Decimal(quantities[i])
            price = Decimal(prices[i])

            item_total = qty * price
            item_vat = item_total * Decimal("0.05")
            item_grand = item_total + item_vat

            LPOItem.objects.create(
                lpo=lpo,
                description=descriptions[i],
                quantity=qty,
                price=price,
                vat=item_vat,
                total=item_grand
            )

            subtotal += item_total
            total_vat += item_vat
            grand_total += item_grand

        # ✅ SAVE AFTER LOOP
        lpo.subtotal = subtotal
        lpo.vat = total_vat
        lpo.total = grand_total
        lpo.save()

        # ✅ RETURN AFTER LOOP
        return redirect("lpo_detail", pk=lpo.id)

    # ✅ GET REQUEST
    return render(request, "sales/create_lpo.html", {
        "suppliers": suppliers
    })

# def lpo_pdf(request, pk):
#     lpo = get_object_or_404(LPO, id=pk)

#     html = render_to_string(
#         "sales/lpo_pdf.html",
#         {
#             "lpo": lpo,
#             "static_path": settings.STATIC_ROOT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     return HttpResponse(pdf, content_type='application/pdf')

# def lpo_pdf(request, pk):
#     lpo = get_object_or_404(LPO, id=pk)

#     html = render_to_string(
#         "sales/lpo_pdf.html",
#         {
#             "lpo": lpo,
#             "static_path": settings.STATIC_ROOT
#         }
#     )

#     pdf = HTML(
#         string=html,
#         base_url=settings.STATIC_ROOT
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = (
#         f'inline; filename="lpo_{lpo.number}.pdf"'
#     )

#     return response


def lpo_pdf(request, pk):
    """
    Generate LPO PDF, upload it to Google Drive,
    and return the PDF to the browser.
    """

    lpo = get_object_or_404(LPO, id=pk)

    html = render_to_string(
        "sales/lpo_pdf.html",
        {
            "lpo": lpo,
            "static_path": settings.STATIC_ROOT,
        }
    )

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # -------------------------------------------------------
    # Backup PDF to Google Drive
    # -------------------------------------------------------
    try:
        drive_result = GoogleDriveService().upload_document(
            customer_name=lpo.supplier.name,
            document_type=DOCUMENT_TYPES["lpo"],
            file_name=f"{lpo.number}.pdf",
            pdf_bytes=pdf,
        )

        # Save Google Drive URL
        lpo.google_drive_url = drive_result["url"]
        lpo.save(update_fields=["google_drive_url"])

        logger.info(
            "LPO '%s' uploaded successfully to Google Drive.",
            lpo.number,
        )

    except Exception:
        logger.exception(
            "Failed to upload LPO '%s' to Google Drive.",
            lpo.number,
        )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{lpo.number}.pdf"'
    )

    return response

def lpo_detail(request, pk):
    lpo = get_object_or_404(LPO, id=pk)

    return render(request, "sales/lpo_detail.html", {
        "lpo": lpo
    })


def add_supplier(request):
    if request.method == "POST":
        Supplier.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            trn_number=request.POST.get("trn_number"),
            website=request.POST.get("website")
        )
        return redirect('dashboard')   # or redirect to create_lpo

    return render(request, "sales/add_supplier.html")


def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)

    if request.method == "POST":
        supplier.name = request.POST.get("name")
        supplier.phone = request.POST.get("phone")
        supplier.email = request.POST.get("email")
        supplier.address = request.POST.get("address")
        supplier.trn_number = request.POST.get("trn_number")
        supplier.website = request.POST.get("website")

        supplier.save()

        return redirect("dashboard")

    return render(request, "sales/edit_supplier.html", {
        "supplier": supplier
    })

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)
    supplier.delete()
    return redirect("dashboard")

# def supplier_detail(request, pk):
#     supplier = get_object_or_404(Supplier, id=pk)

#     return render(request, "sales/supplier_detail.html", {
#         "supplier": supplier
#     })

from django.shortcuts import render, get_object_or_404
from .models import Supplier, LPO

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)

    lpos = LPO.objects.filter(supplier=supplier)

    return render(request, "sales/supplier_detail.html", {
        "supplier": supplier,
        "lpos": lpos
    })

def edit_lpo(request, pk):
    lpo = get_object_or_404(LPO, id=pk)
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        lpo.supplier_id = request.POST.get("supplier")
        lpo.quote_ref = request.POST.get("quote_ref")
        lpo.note = request.POST.get("note")
        lpo.delivery_date = request.POST.get("delivery_date") or None
        lpo.save()

        # delete old items
        lpo.items.all().delete()

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        # subtotal = 0

        # for i in range(len(quantities)):
        #     qty = int(quantities[i])
        #     price = float(prices[i])
        #     total = qty * price

        #     LPOItem.objects.create(
        #         lpo=lpo,
        #         description=descriptions[i],
        #         quantity=qty,
        #         price=price,
        #         total=total
        #     )

        #     subtotal += total

        # lpo.subtotal = subtotal
        # lpo.vat = subtotal * 0.05
        # lpo.total = subtotal + lpo.vat


        from decimal import Decimal

        subtotal = Decimal("0")
        total_vat = Decimal("0")
        grand_total = Decimal("0")

        for i in range(len(quantities)):
            if not descriptions[i].strip():
                continue

            qty = Decimal(quantities[i])
            price = Decimal(prices[i])

            item_total = qty * price
            item_vat = item_total * Decimal("0.05")
            item_grand = item_total + item_vat

            LPOItem.objects.create(
                lpo=lpo,
                description=descriptions[i],
                quantity=qty,
                price=price,
                vat=item_vat,          # ✅ FIX
                total=item_grand       # ✅ FIX
            )

            subtotal += item_total
            total_vat += item_vat
            grand_total += item_grand

        lpo.subtotal = subtotal
        lpo.vat = total_vat
        lpo.total = grand_total
        lpo.save()

        return redirect("lpo_detail", pk=lpo.id)

    return render(request, "sales/edit_lpo.html", {
        "lpo": lpo,
        "suppliers": suppliers
    })

# def delete_lpo(request, pk):
#     lpo = get_object_or_404(LPO, id=pk)
#     lpo.delete()
#     return redirect('dashboard')

# def delete_lpo(request, pk):
#     lpo = get_object_or_404(LPO, id=pk)

#     if request.method == "POST":
#         lpo.delete()
#         return redirect('dashboard')

#     return redirect('dashboard')


def delete_lpo(request, pk):
    lpo = get_object_or_404(LPO, id=pk)
    lpo.delete()
    return redirect('dashboard')


def delete_receipt(request, pk):

    receipt = get_object_or_404(PaymentReceipt, id=pk)

    receipt.delete()

    return redirect("dashboard")


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login

# def login_view(request):

#     if request.method == 'POST':

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user:

#             login(request, user)

#             if user.is_superuser:
#                 return redirect('dashboard')

#             # Later we will add employee/freelancer role check

#             return redirect('dashboard')

#     return render(request, 'login.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin
            if user.is_superuser:
                return redirect('dashboard')

            # Employee / Freelancer
            try:
                profile = user.userprofile

                if profile.role in ['employee', 'freelancer']:
                    # return redirect('/tasks/freelancer_dashboard/')
                    return redirect('freelancer_dashboard')
            except:
                pass

            return redirect('dashboard')

    return render(request, 'login.html')


@login_required
def create_quotation_from_request(request, request_id):

    work_request = get_object_or_404(
        WorkRequest,
        id=request_id,
        status="approved"
    )

    customer, created = Customer.objects.get_or_create(
        name=work_request.customer_name
    )

    if request.method == "POST":

        quotation = Quotation.objects.create(
            number=generate_quotation_number(),
            customer=customer,
            attention=request.POST.get("attention"),
            sales_person=request.POST.get("sales_person"),
            note=request.POST.get("note"),
        )

        subtotal = 0

        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        for description, quantity, price in zip(
            descriptions,
            quantities,
            prices
        ):

            if not description.strip():
                continue

            qty = int(quantity)
            price = float(price)
            total = qty * price

            QuotationItem.objects.create(
                quotation=quotation,
                description=description,
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        quotation.subtotal = subtotal
        quotation.vat = subtotal * 0.05
        quotation.total = quotation.subtotal + quotation.vat
        quotation.save()

        work_request.status = "quotation_created"
        work_request.quotation = quotation
        work_request.save()

        messages.success(
            request,
            "Quotation created successfully."
        )

        return redirect("quotation_detail", pk=quotation.id)

    return render(
        request,
        "sales/create_quotation_from_request.html",
        {
            "work_request": work_request,
            "customer": customer,
            "services": Service.objects.all(),
        },
    )