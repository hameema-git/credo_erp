from django.db import models

# ---------- Customer ----------
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    trn_number = models.CharField(max_length=50, blank=True, null=True)  # ✅ ADD THIS

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
    note = models.TextField(blank=True, null=True)

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
class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
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

    # 🔥 OPTIONAL (for future use only)
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    # 🔥 ADD THIS (same as quotation)
    attention = models.CharField(max_length=100, blank=True, null=True)
    sales_person = models.CharField(max_length=100, blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    notes = models.TextField(blank=True, null=True)

    @property
    def balance(self):
        return self.total - self.paid_amount

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

    def __str__(self):
        return self.description[:50]


# ---------- Payment Receipt ----------
class PaymentReceipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="receipts")

    receipt_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20, choices=Invoice.PAYMENT_METHODS)
    short_description = models.TextField(blank=True, null=True)

    received_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.receipt_number
    
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    trn_number = models.CharField(max_length=50, blank=True, null=True)
    # website = models.URLField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# ---------- LPO ----------
# class LPO(models.Model):
#     number = models.CharField(max_length=50, unique=True)

#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

#     order_date = models.DateField(auto_now_add=True)
#     delivery_date = models.DateField(null=True, blank=True)

#     note = models.TextField(blank=True, null=True)

#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return self.number


# # ---------- LPO ITEMS ----------
# # class LPOItem(models.Model):
# #     lpo = models.ForeignKey(LPO, on_delete=models.CASCADE, related_name="items")

# #     description = models.TextField()
# #     quantity = models.IntegerField(default=1)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
# #     total = models.DecimalField(max_digits=10, decimal_places=2)

# #     def save(self, *args, **kwargs):
# #         self.total = self.quantity * self.price
# #         super().save(*args, **kwargs)


# from decimal import Decimal

# # class LPOItem(models.Model):
# #     lpo = models.ForeignKey(LPO, on_delete=models.CASCADE, related_name="items")

# #     description = models.TextField()
# #     quantity = models.IntegerField(default=1)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)

# #     total = models.DecimalField(max_digits=10, decimal_places=2)   # base total
# #     vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # ✅ NEW

#     # def save(self, *args, **kwargs):
#     #     base_total = Decimal(self.quantity) * self.price
#     #     self.vat = base_total * Decimal("0.05")   # ✅ VAT per item
#     #     self.total = base_total + self.vat        # ✅ final total WITH VAT
#     #     super().save(*args, **kwargs)



# class LPOItem(models.Model):
#     lpo = models.ForeignKey(LPO, on_delete=models.CASCADE, related_name="items")

#     description = models.TextField()
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     total = models.DecimalField(max_digits=10, decimal_places=2)


from decimal import Decimal

# ---------- LPO ----------
class LPO(models.Model):
    number = models.CharField(max_length=50, unique=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)

    note = models.TextField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.number


# ---------- LPO ITEMS ----------
class LPOItem(models.Model):
    lpo = models.ForeignKey(LPO, on_delete=models.CASCADE, related_name="items")

    description = models.TextField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # ✅ VAT PER ITEM
    total = models.DecimalField(max_digits=10, decimal_places=2)            # ✅ FINAL (WITH VAT)