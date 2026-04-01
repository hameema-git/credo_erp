from .models import Quotation,PaymentReceipt

# def generate_quotation_number():
#     last = Quotation.objects.order_by('-id').first()
#     if not last:
#         return "CRD-QT-2561"
    
#     num = int(last.number.split('-')[-1]) + 1
#     return f"CRD-QT-{num:04d}"

def generate_quotation_number():
    last = Quotation.objects.order_by('-id').first()

    if not last:
        return "CRD-QT-2561"   # starting number

    try:
        last_num = int(last.number.split('-')[-1])
    except:
        last_num = 2560   # fallback safety

    new_num = last_num + 1

    return f"CRD-QT-{new_num}"

from .models import Quotation, Invoice


from datetime import datetime

# def generate_quotation_number():
#     year = datetime.now().year
#     count = Quotation.objects.filter(date__year=year).count() + 1
#     return f"QTN-{year}-{count:04d}"


# def generate_invoice_number():
#     year = datetime.now().year
#     count = Invoice.objects.filter(date__year=year).count() + 1
#     return f"INV-{year}-{count:04d}"
# def generate_invoice_number():
#     last = Invoice.objects.order_by('-id').first()
#     if not last:
#         return "CRD-IN-2561"
    
#     num = int(last.number.split('-')[-1]) + 1
#     return f"CRD-IN-{num:04d}"

def generate_invoice_number():
    last = Invoice.objects.order_by('-id').first()

    if not last:
        return "CRD-IN-2561"

    try:
        last_num = int(last.number.split('-')[-1])
    except:
        last_num = 2560

    new_num = last_num + 1

    return f"CRD-IN-{new_num}"


def generate_receipt_number():
    last = PaymentReceipt.objects.order_by('-id').first()

    if not last:
        return "CRD-RCPT-2561"

    try:
        last_num = int(last.receipt_number.split('-')[-1])
    except:
        last_num = 2560

    return f"CRD-RCPT-{last_num + 1}"