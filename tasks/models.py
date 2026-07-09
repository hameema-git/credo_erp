from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from sales.models import Quotation


# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('manager', 'Manager'),
#         ('freelancer', 'Freelancer'),
#     )
#     # role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     role = models.CharField(
#     max_length=20,
#     choices=ROLE_CHOICES,
#     default='freelancer'
# )

#     # 🔥 NEW FIELDS (Professional)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
#     is_approved = models.BooleanField(default=False)
#     gender = models.CharField(
#     max_length=10,
#     choices=[('male', 'Male'), ('female', 'Female')],
#     blank=True,
#     null=True
# )

#     def __str__(self):
#         return self.username

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):

#     ROLE_CHOICES = (
#         ('manager', 'Manager'),
#         ('freelancer', 'Freelancer'),
#         ('employee', 'Employee'), 
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default='freelancer'   # 🔥 IMPORTANT
#     )

#     phone = models.CharField(max_length=15, blank=True, null=True)

#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         blank=True,
#         null=True
#     )

#     gender = models.CharField(
#         max_length=10,
#         choices=[('male', 'Male'), ('female', 'Female')],
#         blank=True,
#         null=True
#     )

#     # 🔥 APPROVAL SYSTEM
#     is_approved = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.role == 'manager':
#             self.is_approved = True
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.username

# class Task(models.Model):
#     PRIORITY_CHOICES = (
#         ('low', 'Low'),
#         ('medium', 'Medium'),
#         ('high', 'High'),
#     )

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed')
#     )

#     title = models.CharField(max_length=200)
#     description = models.TextField()

#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

#     # 🔥 NEW FIELDS
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     deadline = models.DateField()

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def __str__(self):
#         return self.title


class Task(models.Model):

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )

    TASK_TYPE_CHOICES = (
        ('one_time', 'One Time'),
        ('ongoing', 'Ongoing'),
        ('monthly', 'Monthly'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        default='one_time'
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    # PAYMENT SECTION

    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def balance_amount(self):
        if self.payment_amount:
            return self.payment_amount - self.paid_amount
        return 0

    def __str__(self):
        return self.title
    

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     role = models.CharField(
#         max_length=20,
#         choices=[
#             ('admin', 'Admin'),
#             ('employee', 'Employee'),
#             ('freelancer', 'Freelancer')
#         ]
#     )

#     phone = models.CharField(max_length=15, blank=True)
#     gender = models.CharField(max_length=10, blank=True)

#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         blank=True,
#         null=True
#     )

from django.contrib.auth.models import User

# class UserProfile(models.Model):

#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('employee', 'Employee'),
#         ('freelancer', 'Freelancer'),
#     )

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default='employee'
#     )

#     phone = models.CharField(
#         max_length=15,
#         blank=True,
#         null=True
#     )

#     gender = models.CharField(
#         max_length=10,
#         blank=True,
#         null=True
#     )

#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         blank=True,
#         null=True
#     )

#     def __str__(self):
#         return self.user.username

from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):

#     ROLE_CHOICES = (
#         ('employee', 'Employee'),
#         ('freelancer', 'Freelancer'),
#     )

#     GENDER_CHOICES = (
#         ('male', 'Male'),
#         ('female', 'Female'),
#     )

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=ROLE_CHOICES
#     )

#     phone = models.CharField(
#         max_length=15,
#         blank=True,
#         null=True
#     )

#     gender = models.CharField(
#         max_length=10,
#         choices=GENDER_CHOICES,
#         blank=True,
#         null=True
#     )

#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         blank=True,
#         null=True
#     )

#     is_approved = models.BooleanField(
#         default=False
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.role}"

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('freelancer', 'Freelancer'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

# ==============================================================
# WORK REQUEST MODULE — Phase 1
# Append this block to the bottom of tasks/models.py
# ==============================================================

class WorkRequest(models.Model):
    """
    A request submitted by an employee or freelancer for a piece of work.

    Lifecycle:
        pending → under_review → approved / rejected
        approved → quotation_created  (Phase 3, when linked to Quotation)
    """

    PRIORITY_CHOICES = (
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    )

    STATUS_CHOICES = (
        ('pending',            'Pending'),
        ('under_review',       'Under Review'),
        ('approved',           'Approved'),
        ('rejected',           'Rejected'),
        ('quotation_created',  'Quotation Created'),
    )

    # Auto-generated reference number e.g. WR00025
    request_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    # Who submitted this request
    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='work_requests',
    )

    # Customer this work is for (free-text for Phase 1; link to
    # sales.Customer via FK in a later phase if needed)
    customer_name = models.CharField(max_length=200)

    title = models.CharField(max_length=200)

    description = models.TextField()

    quotation = models.ForeignKey(
    Quotation,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="work_requests"
)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )

    required_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    # Manager notes visible to employee after review
    admin_notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Request'
        verbose_name_plural = 'Work Requests'

    # ------------------------------------------------------------------
    # Auto-number: WR00001, WR00002, …
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        if not self.request_no:
            # Use MAX(id)+1 as a safe sequential number before first save
            # last = WorkRequest.objects.order_by('id').last()
            # next_number = (last.id + 1) if last else 1

            last = WorkRequest.objects.order_by("-created_at").first()

            if last:
                last_no = int(last.request_no.replace("WR", ""))
            else:
                last_no = 0

            self.request_no = f"WR{last_no+1:05d}"
            # self.request_no = f"WR{next_number:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_no} — {self.title}"

    # ------------------------------------------------------------------
    # Convenience status helpers
    # ------------------------------------------------------------------

    @property
    def is_pending(self) -> bool:
        return self.status == 'pending'

    @property
    def is_approved(self) -> bool:
        return self.status == 'approved'

    @property
    def is_rejected(self) -> bool:
        return self.status == 'rejected'

    @property
    def can_be_reviewed(self) -> bool:
        """True when the manager can still approve or reject."""
        return self.status in ('pending', 'under_review')