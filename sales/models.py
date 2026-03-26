from django.db import models

# Create your models here.
from django.db import models

# ---------- Customer ----------
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ---------- Service ----------
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# ---------- Quotation ----------
# class Quotation(models.Model):
#     number = models.CharField(max_length=50, unique=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     STATUS_CHOICES = [
#     ('draft', 'Draft'),
#     ('sent', 'Sent'),
#     ('approved', 'Approved'),
#     ('rejected', 'Rejected'),
# ]

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

#     def __str__(self):
#         return self.number

# # ---------- Quotation ----------
# class Quotation(models.Model):
#     STATUS_CHOICES = [
#         ('draft', 'Draft'),
#         ('sent', 'Sent'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     number = models.CharField(max_length=50, unique=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)

#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
#     notes = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.number

# ---------- Quotation ----------
class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # ✅ NEW FIELDS
    attention = models.CharField(max_length=100, blank=True, null=True)
    sales_person = models.CharField(max_length=100, blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.number



# ---------- Quotation Items ----------
# class QuotationItem(models.Model):
#     quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.service.name} - {self.quotation.number}"


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")

    # OPTIONAL predefined service
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    # MAIN FIELD (used always)
    description = models.TextField()

    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description[:50]

# ---------- Invoice ----------
# class Invoice(models.Model):
#     number = models.CharField(max_length=50, unique=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True)
#     date = models.DateField(auto_now_add=True)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return self.number


# ---------- Invoice ----------
class Invoice(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
    ]

    number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True)

    date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    notes = models.TextField(blank=True, null=True)

     # ✅ ADD HERE
    @property
    def balance(self):
        return self.total - self.paid_amount
    
       # ✅ ADD SAVE METHOD HERE
    def save(self, *args, **kwargs):
        if self.paid_amount == 0:
            self.payment_status = 'pending'
        elif self.paid_amount >= self.total:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'partial'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.number


# ---------- Invoice Items ----------
# class InvoiceItem(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.service.name} - {self.invoice.number}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()

    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)


class PaymentReceipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    receipt_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20, choices=Invoice.PAYMENT_METHODS)

    received_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.receipt_number