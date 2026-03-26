from .models import Quotation

def generate_quotation_number():
    last = Quotation.objects.order_by('-id').first()
    if not last:
        return "CRD-QT-0001"
    
    num = int(last.number.split('-')[-1]) + 1
    return f"CRD-QT-{num:04d}"

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
def generate_invoice_number():
    last = Invoice.objects.order_by('-id').first()
    if not last:
        return "CRD-IN-0001"
    
    num = int(last.number.split('-')[-1]) + 1
    return f"CRD-IN-{num:04d}"