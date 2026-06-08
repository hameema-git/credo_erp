from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Task, UserProfile


# class TaskForm(forms.ModelForm):

#     class Meta:
#         model = Task
#         fields = [
#             'title',
#             'description',
#             'assigned_to',
#             'task_type',
#             'deadline',
#             'priority',
#             'status'
#         ]

#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'assigned_to': forms.Select(attrs={'class': 'form-control'}),
#             'task_type': forms.Select(attrs={'class': 'form-control'}),
#             'deadline': forms.DateInput(
#                 attrs={
#                     'type': 'date',
#                     'class': 'form-control'
#                 }
#             ),
#             'priority': forms.Select(attrs={'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].queryset = User.objects.all()

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            'title',
            'description',
            'assigned_to',
            'task_type',
            'deadline',
            'priority',
            'status',

            'payment_amount',
            'paid_amount',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={'class': 'form-control'}
            ),

            'assigned_to': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'task_type': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'priority': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'payment_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Task Amount'
                }
            ),

            'paid_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Paid Amount'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.all()

    def save(self, commit=True):

        task = super().save(commit=False)

        if not task.payment_amount:

            task.payment_status = 'pending'

        elif task.paid_amount <= 0:

            task.payment_status = 'pending'

        elif task.paid_amount < task.payment_amount:

            task.payment_status = 'partial'

        else:

            task.payment_status = 'paid'

        if commit:
            task.save()

        return task


class SignupForm(UserCreationForm):

    email = forms.EmailField()

    phone = forms.CharField(required=False)

    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female')
        ],
        required=False
    )

    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class FreelancerForm(SignupForm):
    pass


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'gender',
            'profile_image'
        ]