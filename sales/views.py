from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q
from weasyprint import HTML
from num2words import num2words

from .models import *
from .utils import generate_quotation_number, generate_invoice_number, generate_receipt_number


# ---------------- DASHBOARD ----------------
def dashboard(request):
    query = request.GET.get('q')

    customers = Customer.objects.all()
    quotations = Quotation.objects.all()
    invoices = Invoice.objects.all()

    search_type = request.GET.get('type', 'all')

    if query:
        if search_type in ['all', 'customer']:
            customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))

        if search_type in ['all', 'quotation']:
            quotations = quotations.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

        if search_type in ['all', 'invoice']:
            invoices = invoices.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))

    return render(request, "sales/dashboard.html", {
        "customers_count": customers.count(),
        "quotations_count": quotations.count(),
        "invoices_count": invoices.count(),
        "recent_quotations": quotations.order_by('-id')[:5],
        "recent_invoices": invoices.order_by('-id')[:5],
        "query": query
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

        quotation = Quotation.objects.create(
            number=generate_quotation_number(),
            customer=customer,
            attention=request.POST.get("attention") or "",
            sales_person=request.POST.get("sales_person") or "",
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

def quotation_pdf(request, pk):
    quotation = get_object_or_404(Quotation, id=pk)

    html = render_to_string(
        "sales/quotation_pdf.html",
        {
            "quotation": quotation,
            "static_path": settings.STATIC_ROOT  # ✅ IMPORTANT
        },
        request=request
    )

    pdf = HTML(string=html).write_pdf()

    return HttpResponse(pdf, content_type='application/pdf')

# ---------------- INVOICE (NEW FLOW) ----------------
def create_invoice(request):
    customers = Customer.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        customer = Customer.objects.get(id=request.POST.get("customer"))

        invoice = Invoice.objects.create(
            number=generate_invoice_number(),
            customer=customer,
            attention=request.POST.get("attention") or "",
            sales_person=request.POST.get("sales_person") or "",
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

def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)

    html = render_to_string(
        "sales/invoice_pdf.html",
        {
            "invoice": invoice,
            "static_path": settings.STATIC_ROOT   # ✅ IMPORTANT
        }
    )

    pdf = HTML(
        string=html,
        base_url=settings.STATIC_ROOT   # ✅ CRITICAL FIX
    ).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{invoice.number}.pdf"'

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

def payment_receipt_pdf(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

    if not receipt:
        return HttpResponse("No payment receipt found for this invoice")

    amount_words = num2words(receipt.amount_paid, lang='en').title() + " AED Only"

    html = render_to_string(
        "sales/payment_receipt_pdf.html",
        {
            "receipt": receipt,
            "amount_words": amount_words,
            "static_path": settings.STATIC_ROOT
        }
    )

    pdf = HTML(
        string=html,
        base_url=settings.STATIC_ROOT
    ).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

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

    if search_type == "customer" or not search_type:
        customers = list(Customer.objects.filter(name__icontains=query).values('id','name')[:5])

    if search_type == "quotation" or not search_type:
        quotations = list(Quotation.objects.filter(number__icontains=query).values('id','number')[:5])

    if search_type == "invoice" or not search_type:
        invoices = list(Invoice.objects.filter(number__icontains=query).values('id','number')[:5])
    if search_type == "service" or not search_type:
        services = list(Service.objects.filter(name__icontains=query).values('id','name')[:5])

    return JsonResponse({
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices,
        "services":services
    })


# def search_results(request):
#     query = request.GET.get('q')

#     return render(request, "sales/search_results.html", {
#         "customers": Customer.objects.filter(name__icontains=query),
#         "quotations": Quotation.objects.filter(number__icontains=query),
#         "invoices": Invoice.objects.filter(number__icontains=query),
#         "query": query
#     })


def search_results(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')  # 🔥 ADD THIS

    customers = Customer.objects.none()
    quotations = Quotation.objects.none()
    invoices = Invoice.objects.none()
    services = Service.objects.none()

    # 🔥 APPLY FILTER
    if search_type == "customer":
        customers = Customer.objects.filter(name__icontains=query)

    elif search_type == "quotation":
        quotations = Quotation.objects.filter(number__icontains=query)

    elif search_type == "invoice":
        invoices = Invoice.objects.filter(number__icontains=query)
    elif search_type == "service":
        services = Service.objects.filter(name__icontains=query)

    else:  # default = all
        customers = Customer.objects.filter(name__icontains=query)
        quotations = Quotation.objects.filter(number__icontains=query)
        invoices = Invoice.objects.filter(number__icontains=query)
        services = Service.objects.filter(name__icontains=query)

    return render(request, "sales/search_results.html", {
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices,
        "query": query,
        "services": services,
        "search_type": search_type   # 🔥 PASS THIS
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

        return redirect("receipt_pdf", pk=invoice.id)

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
        quotation.notes = request.POST.get("notes")

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
        invoice.notes = request.POST.get("notes")

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