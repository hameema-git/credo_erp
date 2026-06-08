from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


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