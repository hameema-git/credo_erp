from django.shortcuts import render, redirect
from .models import *
from .utils import generate_quotation_number
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Customer
from num2words import num2words

from .utils import generate_invoice_number

# def convert_to_invoice(request, pk):
#     quotation = Quotation.objects.get(id=pk)

#     # 🚫 Prevent duplicate invoice
#     if Invoice.objects.filter(quotation=quotation).exists():
#         invoice = Invoice.objects.get(quotation=quotation)
#         return redirect('invoice_detail', pk=invoice.id)

#     # ✅ Create Invoice
#     invoice = Invoice.objects.create(
#         number=generate_invoice_number(),
#         customer=quotation.customer,
#         quotation=quotation,
#         subtotal=quotation.subtotal,
#         vat=quotation.vat,
#         total=quotation.total
#     )

#     # ✅ Copy Items
#     for item in quotation.items.all():
#         InvoiceItem.objects.create(
#             invoice=invoice,
#             service=item.service,
#              description=item.description,  # ✅ ADD THIS
#             quantity=item.quantity,
#             price=item.price,
#             total=item.total
#         )

#     # ✅ Update quotation status
#     quotation.status = 'approved'
#     quotation.save()

#     return redirect('invoice_detail', pk=invoice.id)


# def invoice_detail(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     return render(request, "sales/invoice_detail.html", {
#         "invoice": invoice
#     })


from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib import messages

from .models import Invoice, InvoiceItem, Quotation


# 🔢 Generate Invoice Number
# def generate_invoice_number():
#     last = Invoice.objects.order_by('-id').first()
#     if last:
#         num = int(last.number.split('-')[-1]) + 1
#     else:
#         num = 1
#     return f"INV-2026-{num:04d}"


# 🔄 Convert Quotation → Invoice
def convert_to_invoice(request, pk):
    quotation = get_object_or_404(Quotation, id=pk)

    # 🚫 Prevent duplicate invoice
    existing_invoice = Invoice.objects.filter(quotation=quotation).first()
    if existing_invoice:
        messages.info(request, "Invoice already exists for this quotation.")
        return redirect('invoice_detail', pk=existing_invoice.id)

    # ✅ Create Invoice
    invoice = Invoice.objects.create(
        number=generate_invoice_number(),
        customer=quotation.customer,
        quotation=quotation,
        subtotal=quotation.subtotal,
        vat=quotation.vat,
        total=quotation.total
    )

    # ✅ Copy Items
    for item in quotation.items.all():
        InvoiceItem.objects.create(
            invoice=invoice,
            service=item.service,
            description=item.description,  # 🔥 important
            quantity=item.quantity,
            price=item.price,
            total=item.total
        )

    # ✅ Update quotation status
    quotation.status = 'approved'
    quotation.save()

    messages.success(request, "Invoice created successfully!")

    return redirect('invoice_detail', pk=invoice.id)




def invoice_detail(request, pk):
    invoice = Invoice.objects.get(id=pk)

    receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

    return render(request, "sales/invoice_detail.html", {
        "invoice": invoice,
        "receipt": receipt
    })

# # 📥 Invoice PDF
# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     template = get_template("sales/invoice_pdf.html")
#     html = template.render({
#         "invoice": invoice
#     })

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename="invoice_{invoice.number}.pdf"'

#     pisa.CreatePDF(html, dest=response)

#     return response

from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# def invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)

#     template = get_template("sales/invoice_pdf.html")
#     html = template.render({
#         "invoice": invoice,
#         "request": request   # 🔥 MUST ADD THIS
#     })

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename="invoice_{invoice.number}.pdf"'

#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF")

#     return response

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.shortcuts import get_object_or_404
from .models import Invoice

def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)

    # Render HTML
    html = render_to_string("sales/invoice_pdf.html", {
        "invoice": invoice
    })

    # Generate PDF
    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')   # 🔥 IMPORTANT for static files
    ).write_pdf()

    # Return response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{invoice.number}.pdf"'

    return response


# 📋 Invoice List (OPTIONAL but useful)
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-id')

    return render(request, "sales/invoice_list.html", {
        "invoices": invoices
    })

def add_customer(request):
    if request.method == "POST":
        Customer.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address")
        )
        return redirect('/quotation/create/')

    return render(request, "customers/add_customer.html")


def add_service(request):
    if request.method == "POST":
        Service.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description")
        )
        return redirect('/quotation/create/')

    return render(request, "services/add_service.html")


def create_quotation(request):
    customers = Customer.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        customer = Customer.objects.get(id=request.POST.get("customer"))

        attention = request.POST.get("attention") or ""
        sales_person = request.POST.get("sales_person") or ""

        quotation = Quotation.objects.create(
            number=generate_quotation_number(),
            customer=customer,
            attention=attention,
            sales_person=sales_person
        )

        # ✅ NEW DATA FROM FORM
        service_ids = request.POST.getlist("service")
        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("price")

        subtotal = 0

        for i in range(len(quantities)):
            # Handle optional service
            service = None
            if service_ids[i]:
                service = Service.objects.get(id=service_ids[i])

            description = descriptions[i]
            qty = int(quantities[i])
            price = float(prices[i])
            total = qty * price

            QuotationItem.objects.create(
                quotation=quotation,
                service=service,
                description=description,
                quantity=qty,
                price=price,
                total=total
            )

            subtotal += total

        vat = subtotal * 0.05
        grand_total = subtotal + vat

        quotation.subtotal = subtotal
        quotation.vat = vat
        quotation.total = grand_total
        quotation.save()

        return redirect("quotation_detail", pk=quotation.id)

    return render(request, "sales/create_quotation.html", {
        "customers": customers,
        "services": services
    })

# def create_quotation(request):
#     customers = Customer.objects.all()
#     services = Service.objects.all()

#     if request.method == "POST":
#         customer = Customer.objects.get(id=request.POST.get("customer"))


       

#         attention = request.POST.get("attention") or ""
#         sales_person = request.POST.get("sales_person") or ""
#         quotation = Quotation.objects.create(
#             number=generate_quotation_number(),
#             customer=customer,
#             attention=attention,
#             sales_person=sales_person
#         )

#         service_ids = request.POST.getlist("service")
#         quantities = request.POST.getlist("quantity")

#         subtotal = 0

#         for i in range(len(service_ids)):
#             service = Service.objects.get(id=service_ids[i])
#             qty = int(quantities[i])
#             price = service.price
#             total = price * qty

#             QuotationItem.objects.create(
#                 quotation=quotation,
#                 service=service,
#                 quantity=qty,
#                 price=price,
#                 total=total
#             )

#             subtotal += total

#         vat = 0  # keep 0 for demo
#         grand_total = subtotal + vat

#         quotation.subtotal = subtotal
#         quotation.vat = vat
#         quotation.total = grand_total
#         quotation.save()

#         return redirect("quotation_detail", pk=quotation.id)

#     return render(request, "sales/create_quotation.html", {
#         "customers": customers,
#         "services": services
#     })


def quotation_detail(request, pk):
    quotation = Quotation.objects.get(id=pk)

    return render(request, "sales/quotation_detail.html", {
        "quotation": quotation
    })


# def quotation_pdf(request, pk):
#     quotation = Quotation.objects.get(id=pk)

#     html = render_to_string("sales/quotation_pdf.html", {
#         "quotation": quotation
#     })

#     pdf = HTML(string=html).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'filename="quotation_{quotation.number}.pdf"'

#     return response

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Quotation


def quotation_pdf(request, pk):
    # Get quotation
    quotation = Quotation.objects.get(id=pk)

    # Render HTML template
    html = render_to_string("sales/quotation_pdf.html", {
        "quotation": quotation
    })

    # Generate PDF
    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')   # IMPORTANT for static files
    ).write_pdf()

    # Return response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="quotation_{quotation.number}.pdf"'

    return response

from .models import Customer, Quotation, Invoice

# def dashboard(request):
#     customers_count = Customer.objects.count()
#     quotations_count = Quotation.objects.count()
#     invoices_count = Invoice.objects.count()

#     recent_quotations = Quotation.objects.order_by('-id')[:5]
#     recent_invoices = Invoice.objects.order_by('-id')[:5]

#     return render(request, "sales/dashboard.html", {
#         "customers_count": customers_count,
#         "quotations_count": quotations_count,
#         "invoices_count": invoices_count,
#         "recent_quotations": recent_quotations,
#         "recent_invoices": recent_invoices,
#     })

from django.db.models import Q

def dashboard(request):
    query = request.GET.get('q')

    customers = Customer.objects.all()
    quotations = Quotation.objects.all()
    invoices = Invoice.objects.all()

    query = request.GET.get('q')
    search_type = request.GET.get('type', 'all')

    if query:
        if search_type in ['all', 'customer']:
            customers = customers.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query)
            )

        if search_type in ['all', 'quotation']:
            quotations = quotations.filter(
                Q(number__icontains=query) |
                Q(customer__name__icontains=query)
            )

        if search_type in ['all', 'invoice']:
            invoices = invoices.filter(
                Q(number__icontains=query) |
                Q(customer__name__icontains=query)
            )
    return render(request, "sales/dashboard.html", {
        "customers_count": customers.count(),
        "quotations_count": quotations.count(),
        "invoices_count": invoices.count(),
        "recent_quotations": quotations.order_by('-id')[:5],
        "recent_invoices": invoices.order_by('-id')[:5],
        "query": query
    })


# def update_payment(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     if request.method == "POST":
#         paid = request.POST.get("paid_amount")

#         if paid:
#             invoice.paid_amount = float(paid)
#             invoice.save()  # 🔥 triggers status logic

#     return redirect('invoice_detail', pk=pk)


from .models import PaymentReceipt

# def update_payment(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     if request.method == "POST":
#         paid = request.POST.get("paid_amount")

#         if paid:
#             invoice.paid_amount = float(paid)
#             invoice.save()

#             # ✅ CREATE RECEIPT
#             PaymentReceipt.objects.create(
#                 invoice=invoice,
#                 receipt_number=f"RCPT-{invoice.id}-{invoice.paid_amount}",
#                 amount_paid=invoice.paid_amount,
#                 payment_method='bank',  # or from form
#                 received_by="Admin"
#             )

#     return redirect('invoice_detail', pk=pk)


from .models import PaymentReceipt

def update_payment(request, pk):
    invoice = Invoice.objects.get(id=pk)

    if request.method == "POST":
        paid = request.POST.get("paid_amount")

        if paid:
            invoice.paid_amount = float(paid)
            invoice.save()

            # ✅ GENERATE UNIQUE RECEIPT NUMBER
            last_receipt = PaymentReceipt.objects.order_by('-id').first()

            if last_receipt:
                last_id = last_receipt.id + 1
            else:
                last_id = 1

            receipt_number = f"RCPT-{last_id:04d}"

            # ✅ CREATE RECEIPT
            PaymentReceipt.objects.create(
                invoice=invoice,
                receipt_number=receipt_number,
                amount_paid=invoice.paid_amount,
                payment_method=invoice.payment_method or 'bank',
                received_by="Admin"
            )

    return redirect('invoice_detail', pk=pk)

# def payment_receipt_pdf(request, pk):
#     receipt = PaymentReceipt.objects.get(id=pk)

#     return render(request, "sales/payment_receipt_pdf.html", {
#         "receipt": receipt
#     })

# def payment_receipt_pdf(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     return render(request, "sales/payment_receipt_pdf.html", {
#         "invoice": invoice
#     })

# def payment_receipt_pdf(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     return render(request, "sales/payment_receipt_pdf.html", {
#         "receipt": receipt,
#          "base_url": request.build_absolute_uri('/')  # 👈 ADD THIS
#     })

# def payment_receipt_pdf(request, pk):
#     invoice = Invoice.objects.get(id=pk)
#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     html = render_to_string("sales/payment_receipt_pdf.html", {
#         "receipt": receipt
#     })
#     pdf = HTML(
#         string=html,
#         base_url=request.build_absolute_uri('/')
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')

#     # 🔥 CHANGE THIS LINE
#     response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

#     return response


# def payment_receipt_pdf(request, pk):
#     invoice = Invoice.objects.get(id=pk)
#     receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

#     # ✅ Get custom description from request
#     custom_description = request.GET.get("desc", "")

#     html = render_to_string("sales/payment_receipt_pdf.html", {
#         "receipt": receipt,
#         "custom_description": custom_description
#     })

#     pdf = HTML(
#         string=html,
#         base_url=request.build_absolute_uri('/')
#     ).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')

#     response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

#     return response

def payment_receipt_pdf(request, pk):
    invoice = Invoice.objects.get(id=pk)
    receipt = PaymentReceipt.objects.filter(invoice=invoice).last()

    custom_description = request.GET.get("desc", "")
    received_by = request.GET.get("received_by", "")
    payment_method = request.GET.get("payment_method", "")
    amount = receipt.amount_paid

    amount_words = num2words(amount, lang='en').title() + " AED Only"

    html = render_to_string("sales/payment_receipt_pdf.html", {
        "receipt": receipt,
        "custom_description": custom_description,
        "received_by": received_by,
        "payment_method": payment_method,
        "amount_words": amount_words   # ✅ PASS TO TEMPLATE
    })

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_number}.pdf"'

    return response


from django.http import JsonResponse

def search_ajax(request):
    query = request.GET.get('q')

    customers = list(Customer.objects.filter(name__icontains=query).values('id','name')[:5])
    quotations = list(Quotation.objects.filter(number__icontains=query).values('id','number')[:5])
    invoices = list(Invoice.objects.filter(number__icontains=query).values('id','number')[:5])

    return JsonResponse({
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices
    })

def search_results(request):
    query = request.GET.get('q')

    customers = Customer.objects.filter(name__icontains=query)
    quotations = Quotation.objects.filter(number__icontains=query)
    invoices = Invoice.objects.filter(number__icontains=query)

    return render(request, "sales/search_results.html", {
        "query": query,
        "customers": customers,
        "quotations": quotations,
        "invoices": invoices
    })


# def receipt_preview(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     if request.method == "POST":
#         description = request.POST.get("description")

#         return redirect(f"/receipt/{invoice.id}/?desc={description}")

#     return render(request, "sales/receipt_preview.html", {
#         "invoice": invoice
#     })


# from django.shortcuts import redirect
# from django.urls import reverse
# from urllib.parse import urlencode

# def receipt_preview(request, pk):
#     invoice = Invoice.objects.get(id=pk)

#     if request.method == "POST":
#         description = request.POST.get("description")

#         # ✅ Build URL safely
#         base_url = reverse("receipt_pdf", args=[invoice.id])
#         query_string = urlencode({"desc": description})

#         url = f"{base_url}?{query_string}"

#         return redirect(url)

#     return render(request, "sales/receipt_preview.html", {
#         "invoice": invoice
#     })

from django.urls import reverse
from urllib.parse import urlencode

def receipt_preview(request, pk):
    invoice = Invoice.objects.get(id=pk)

    if request.method == "POST":
        description = request.POST.get("description")
        received_by = request.POST.get("received_by")
        payment_method = request.POST.get("payment_method")

        base_url = reverse("receipt_pdf", args=[invoice.id])

        query_string = urlencode({
            "desc": description,
            "received_by": received_by,
            "payment_method": payment_method
        })

        return redirect(f"{base_url}?{query_string}")

    return render(request, "sales/receipt_preview.html", {
        "invoice": invoice
    })