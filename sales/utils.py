from .models import Quotation,PaymentReceipt

# def generate_quotation_number():
#     last = Quotation.objects.order_by('-id').first()
#     if not last:
#         return "CRD-QT-2561"
    
#     num = int(last.number.split('-')[-1]) + 1
#     return f"CRD-QT-{num:04d}"

# def generate_quotation_number():
#     last = Quotation.objects.order_by('-id').first()

#     if not last:
#         return "CRD2573"   # starting number

#     try:
#         last_num = int(last.number.split('-')[-1])
#     except:
#         last_num = 2572   # fallback safety

#     new_num = last_num + 1

#     return f"CRD{new_num}"
PREFIX = "CRD"

def generate_quotation_number():
    last = Quotation.objects.order_by('-id').first()

    if not last:
        return f"{PREFIX}2573"

    try:
        last_num = int(last.number.replace(PREFIX, ""))
    except:
        last_num = 2572

    return f"{PREFIX}{last_num + 1}"

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

# def generate_invoice_number():
#     last = Invoice.objects.order_by('-id').first()

#     if not last:
#         return "INVCRD2567"

#     try:
#         last_num = int(last.number.split('-')[-1])
#     except:
#         last_num = 2566

#     new_num = last_num + 1

#     return f"INVCRD{new_num}"

# def generate_invoice_number():
#     last = Invoice.objects.order_by('-id').first()

#     if not last:
#         return "INVCRD2567"

#     try:
#         # remove prefix and extract number
#         last_num = int(last.number.replace("INVCRD", ""))
#     except:
#         last_num = 2566

#     new_num = last_num + 1

#     return f"INVCRD{new_num}"

from django.db import transaction

def generate_invoice_number():
    with transaction.atomic():
        last = Invoice.objects.select_for_update().order_by('-id').first()

        if not last:
            return "INVCRD2567"

        try:
            last_num = int(last.number.replace("INVCRD", ""))
        except:
            last_num = 2566

        return f"INVCRD{last_num + 1}"


def generate_receipt_number():
    last = PaymentReceipt.objects.order_by('-id').first()

    if not last:
        return "CRD-RCPT-2567"

    try:
        last_num = int(last.receipt_number.split('-')[-1])
    except:
        last_num = 2566

    return f"CRD-RCPT-{last_num + 1}"


# def generate_lpo_number():
#     import datetime
#     from .models import LPO

#     year = datetime.datetime.now().year

#     last = LPO.objects.filter(number__startswith=f"LPO-{year}")\
#                       .order_by('-id').first()

#     if last:
#         last_num = int(last.number.split('-')[-1])
#         new_num = last_num + 1
#     else:
#         new_num = 1

#     return f"LPO-{year}-{new_num:04d}"


def generate_lpo_number():
    from .models import LPO

    last = LPO.objects.filter(number__startswith="LPO-CRD")\
                      .order_by('-id').first()

    if last:
        try:
            last_num = int(last.number.replace("LPO-CRD", ""))
            new_num = last_num + 1
        except:
            new_num = 1001   # fallback if format broken
    else:
        new_num = 1001   # starting number

    return f"LPO-CRD{new_num}"