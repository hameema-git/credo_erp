from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from .forms import FreelancerForm,SignupForm,ProfileForm
from .forms import FreelancerForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')   # redirect to login page

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             if user.role == 'manager':
#                 return redirect('manager_dashboard')
#             else:
#                 return redirect('freelancer_dashboard')

#     return render(request, 'login.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile


# def login_view(request):

#     if request.method == "POST":

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is None:
#             messages.error(
#                 request,
#                 "Invalid username or password"
#             )
#             return redirect('login')

#         # SUPER ADMIN → ERP
#         if user.is_superuser:
#             login(request, user)
#             return redirect('dashboard')

#         try:
#             profile = UserProfile.objects.get(user=user)

#             # NOT APPROVED
#             if not profile.is_approved:
#                 messages.warning(
#                     request,
#                     "Your account is waiting for admin approval"
#                 )
#                 return redirect('login')

#             login(request, user)

#             # ADMIN
#             if profile.role == 'admin':
#                 return redirect('dashboard')

#             # EMPLOYEE / FREELANCER
#             if profile.role in ['employee', 'freelancer']:
#                 return redirect('freelancer_dashboard')

#         except UserProfile.DoesNotExist:

#             messages.error(
#                 request,
#                 "User profile not found"
#             )
#             return redirect('login')

#     return render(request, 'login.html')


# def login_view(request):

#     if request.method == "POST":

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is None:
#             messages.error(
#                 request,
#                 "Invalid username or password"
#             )
#             return redirect('login')

#         # ERP Admin
#         if user.is_superuser:
#             login(request, user)
#             return redirect('dashboard')

#         try:
#             profile = UserProfile.objects.get(user=user)

#             if not profile.is_approved:
#                 messages.warning(
#                     request,
#                     "Your account is waiting for admin approval"
#                 )
#                 return redirect('login')

#             login(request, user)

#             return redirect('freelancer_dashboard')

#         except UserProfile.DoesNotExist:
#             messages.error(
#                 request,
#                 "User profile not found"
#             )
#             return redirect('login')

#     return render(request, 'login.html')

# def login_view(request):

#     if request.method == "POST":

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is None:
#             messages.error(
#                 request,
#                 "Invalid username or password"
#             )
#             return redirect('login')

#         # ERP Super Admin
#         if user.is_superuser:
#             login(request, user)
#             return redirect('dashboard')

#         try:
#             profile = UserProfile.objects.get(user=user)

#             # Only employee/freelancer require approval
#             if profile.role in ['employee', 'freelancer']:

#                 if not profile.is_approved:
#                     messages.warning(
#                         request,
#                         "Your account is waiting for admin approval"
#                     )
#                     return redirect('login')

#             login(request, user)

#             # Manager
#             if profile.role == 'manager':
#                 return redirect('manager_dashboard')

#             # Employee/Freelancer
#             return redirect('freelancer_dashboard')

#         except UserProfile.DoesNotExist:

#             messages.error(
#                 request,
#                 "User profile not found"
#             )

#             return redirect('login')

#     return render(request, 'login.html')


def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            messages.error(
                request,
                "Invalid username or password"
            )
            return redirect('login')

        # ERP Super Admin
        if user.is_superuser:
            login(request, user)
            return redirect('dashboard')

        try:
            profile = user.userprofile

        except UserProfile.DoesNotExist:

            messages.error(
                request,
                "User profile not found"
            )
            return redirect('login')

        # Approval required only for employee/freelancer
        if profile.role in ['employee', 'freelancer']:

            if not profile.is_approved:
                messages.warning(
                    request,
                    "Your account is waiting for admin approval"
                )
                return redirect('login')

        login(request, user)

        if profile.role == 'manager':
            return redirect('manager_dashboard')

        return redirect('freelancer_dashboard')

    return render(request, 'login.html')

# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def login_view(request):

#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         # ❌ INVALID LOGIN
#         if user is None:
#             messages.error(request, "Invalid username or password")
#             return redirect('login')

#         # 🔒 NOT APPROVED (VERY IMPORTANT)
#         if user.role == 'freelancer' and not user.is_approved:
#             messages.warning(request, "Your account is waiting for manager approval")
#             return redirect('login')

#         # ✅ LOGIN SUCCESS
#         login(request, user)

#         if user.role == 'manager':
#             return redirect('manager_dashboard')

#         return redirect('freelancer_dashboard')

#     return render(request, 'login.html')

from django.contrib.auth.decorators import login_required
from .models import Task

# @login_required
# def manager_dashboard(request):
#     tasks = Task.objects.all()
#     return render(request, 'manager_dashboard.html', {'tasks': tasks})

# from datetime import date
# @login_required
# def manager_dashboard(request):
#     tasks = Task.objects.all()
#     return render(request, 'manager_dashboard.html', {
#         'tasks': tasks,
#         'today': date.today()
#     })


from datetime import date
from django.contrib.auth.decorators import login_required
from .models import Task, User

# @login_required
# def manager_dashboard(request):
#     tasks = Task.objects.all()

#     # Stats
#     pending_count = tasks.filter(status='pending').count()
#     completed_count = tasks.filter(status='completed').count()
#     overdue_count = tasks.filter(
#         deadline__lt=date.today()
#     ).exclude(status='completed').count()

#     # 👇 FREELANCER DATA WITH COUNTS
#     freelancers = User.objects.filter(role='freelancer')

#     freelancer_data = []
#     for user in freelancers:
#         user_tasks = Task.objects.filter(assigned_to=user)

#         freelancer_data.append({
#             'user': user,
#             'total': user_tasks.count(),
#             'pending': user_tasks.filter(status='pending').count(),
#             'in_progress': user_tasks.filter(status='in_progress').count(),
#             'completed': user_tasks.filter(status='completed').count(),
#         })

#     return render(request, 'manager_dashboard.html', {
#         'tasks': tasks,
#         'today': date.today(),

#         'pending_count': pending_count,
#         'completed_count': completed_count,
#         'overdue_count': overdue_count,

#         'freelancer_data': freelancer_data
#     })


from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task, User

# @login_required
# def manager_dashboard(request):
#     tasks = Task.objects.all()

#     # Stats
#     pending_count = tasks.filter(status='pending').count()
#     completed_count = tasks.filter(status='completed').count()
#     overdue_count = tasks.filter(
#         deadline__lt=date.today()
#     ).exclude(status='completed').count()

#     freelancers = User.objects.filter(role='freelancer')

#     freelancer_data = []

#     for user in freelancers:
#         user_tasks = Task.objects.filter(assigned_to=user)

#         total = user_tasks.count()
#         pending = user_tasks.filter(status='pending').count()
#         in_progress = user_tasks.filter(status='in_progress').count()
#         completed = user_tasks.filter(status='completed').count()

#         # 🔥 CALCULATE PERCENTAGES
#         if total > 0:
#             pending_percent = (pending / total) * 100
#             in_progress_percent = (in_progress / total) * 100
#             completed_percent = (completed / total) * 100
#         else:
#             pending_percent = 0
#             in_progress_percent = 0
#             completed_percent = 0

#         freelancer_data.append({
#             'user': user,
#             'total': total,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,

#             # 🔥 ADD THIS
#             'pending_percent': pending_percent,
#             'in_progress_percent': in_progress_percent,
#             'completed_percent': completed_percent,
#         })

#     return render(request, 'manager_dashboard.html', {
#         'tasks': tasks,
#         'today': date.today(),

#         'pending_count': pending_count,
#         'completed_count': completed_count,
#         'overdue_count': overdue_count,

#         'freelancer_data': freelancer_data
#     })



# @login_required
# def manager_dashboard(request):
#     query = request.GET.get('q', '').strip()

#     # 🔥 BASE QUERY
#     tasks = Task.objects.select_related('assigned_to')

#     # 🔍 SEARCH FILTER
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#     # 📊 STATS (filtered)
#     pending_count = tasks.filter(status='pending').count()
#     completed_count = tasks.filter(status='completed').count()
#     overdue_count = tasks.filter(
#         deadline__lt=date.today()
#     ).exclude(status='completed').count()

#     freelancers = User.objects.filter(role='freelancer')

#     freelancer_data = []

#     for user in freelancers:
#         # 🔥 USE RELATED NAME (FASTER)
#         user_tasks = user.tasks.all()

#         if query:
#             user_tasks = user_tasks.filter(
#                 Q(title__icontains=query) |
#                 Q(description__icontains=query) |
#                 Q(assigned_to__username__icontains=query)
#             )

#         total = user_tasks.count()
#         pending = user_tasks.filter(status='pending').count()
#         in_progress = user_tasks.filter(status='in_progress').count()
#         completed = user_tasks.filter(status='completed').count()

#         # 🔥 SAFE % CALCULATION
#         pending_percent = (pending / total * 100) if total else 0
#         in_progress_percent = (in_progress / total * 100) if total else 0
#         completed_percent = (completed / total * 100) if total else 0

#         freelancer_data.append({
#             'user': user,
#             'total': total,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,

#             'pending_percent': pending_percent,
#             'in_progress_percent': in_progress_percent,
#             'completed_percent': completed_percent,

#             # 🔥 LATEST TASKS
#             'recent_tasks': user_tasks.order_by('-id')[:3]
#         })

#     return render(request, 'manager_dashboard.html', {
#         'tasks': tasks,
#         'today': date.today(),

#         'pending_count': pending_count,
#         'completed_count': completed_count,
#         'overdue_count': overdue_count,

#         'freelancer_data': freelancer_data,
#         'query': query
#     })



from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task, User


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date

from .models import Task, User


@login_required
def manager_dashboard(request):

    # =====================================================
    # 🔍 GET FILTER VALUES
    # =====================================================

    query = request.GET.get('q', '').strip()

    status = request.GET.get('status')

    priority = request.GET.get('priority')

    # =====================================================
    # 📋 TASK QUERY
    # =====================================================

    tasks = Task.objects.select_related('assigned_to')

    # 🔍 SEARCH
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(assigned_to__username__icontains=query)
        )

    # 🎯 STATUS FILTER
    if status:
        tasks = tasks.filter(status=status)

    # 🎯 PRIORITY FILTER
    if priority:
        tasks = tasks.filter(priority=priority)

    # =====================================================
    # 📊 DASHBOARD STATS
    # =====================================================

    total_tasks = tasks.count()

    pending_count = tasks.filter(status='pending').count()

    completed_count = tasks.filter(status='completed').count()

    overdue_count = tasks.filter(
        deadline__lt=date.today()
    ).exclude(status='completed').count()

    # =====================================================
    # 🔥 PAGINATION
    # =====================================================

    paginator = Paginator(
        tasks.order_by('-id'),
        5
    )

    page_number = request.GET.get('page')

    tasks = paginator.get_page(page_number)

    # =====================================================
    # 👨‍💻 FREELANCERS
    # =====================================================

    # freelancers = User.objects.filter(role='freelancer')

    freelancers = User.objects.filter(
    userprofile__role='freelancer'
)

    freelancer_data = []

    for user in freelancers:

        user_tasks = user.tasks.all()

        # 🔍 SEARCH INSIDE USER TASKS
        if query:
            user_tasks = user_tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        total = user_tasks.count()

        pending = user_tasks.filter(
            status='pending'
        ).count()

        in_progress = user_tasks.filter(
            status='in_progress'
        ).count()

        completed = user_tasks.filter(
            status='completed'
        ).count()

        # 📊 PERCENTAGES
        pending_percent = (
            pending / total * 100
        ) if total else 0

        in_progress_percent = (
            in_progress / total * 100
        ) if total else 0

        completed_percent = (
            completed / total * 100
        ) if total else 0

        freelancer_data.append({

            'user': user,

            'total': total,

            'pending': pending,

            'in_progress': in_progress,

            'completed': completed,

            'pending_percent': pending_percent,

            'in_progress_percent': in_progress_percent,

            'completed_percent': completed_percent,

            'recent_tasks': user_tasks.order_by('-id')[:3]

        })

    # =====================================================
    # 👨‍💼 EMPLOYEES
    # =====================================================

    # employees = User.objects.filter(role='employee')

    employees = User.objects.filter(
    userprofile__role='employee'
)

    employee_data = []

    for user in employees:

        user_tasks = user.tasks.all()

        # 🔍 SEARCH INSIDE USER TASKS
        if query:
            user_tasks = user_tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        total = user_tasks.count()

        pending = user_tasks.filter(
            status='pending'
        ).count()

        in_progress = user_tasks.filter(
            status='in_progress'
        ).count()

        completed = user_tasks.filter(
            status='completed'
        ).count()

        # 📊 PERCENTAGES
        pending_percent = (
            pending / total * 100
        ) if total else 0

        in_progress_percent = (
            in_progress / total * 100
        ) if total else 0

        completed_percent = (
            completed / total * 100
        ) if total else 0

        employee_data.append({

            'user': user,

            'total': total,

            'pending': pending,

            'in_progress': in_progress,

            'completed': completed,

            'pending_percent': pending_percent,

            'in_progress_percent': in_progress_percent,

            'completed_percent': completed_percent,

            'recent_tasks': user_tasks.order_by('-id')[:3]

        })

    # =====================================================
    # 🚀 RENDER
    # =====================================================

    return render(request, 'manager_dashboard.html', {

        'tasks': tasks,

        'today': date.today(),

        # 📊 STATS
        'total_tasks': total_tasks,

        'pending_count': pending_count,

        'completed_count': completed_count,

        'overdue_count': overdue_count,

        # 👨‍💻 FREELANCERS
        'freelancer_data': freelancer_data,

        # 👨‍💼 EMPLOYEES
        'employee_data': employee_data,

        # 🔍 FILTER VALUES
        'query': query,

        'status': status,

        'priority': priority
    })


# @login_required
# def manager_dashboard(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     tasks = Task.objects.select_related('assigned_to')

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#     # 🎯 FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 📊 STATS (before pagination)
#     pending_count = tasks.filter(status='pending').count()
#     completed_count = tasks.filter(status='completed').count()
#     overdue_count = tasks.filter(
#         deadline__lt=date.today()
#     ).exclude(status='completed').count()

#     # 🔥 PAGINATION
#     paginator = Paginator(tasks.order_by('-id'), 5)
#     page_number = request.GET.get('page')
#     tasks = paginator.get_page(page_number)

#     freelancers = User.objects.filter(role='freelancer')

#     freelancer_data = []

#     for user in freelancers:
#         user_tasks = user.tasks.all()

#         if query:
#             user_tasks = user_tasks.filter(
#                 Q(title__icontains=query) |
#                 Q(description__icontains=query)
#             )

#         total = user_tasks.count()
#         pending = user_tasks.filter(status='pending').count()
#         in_progress = user_tasks.filter(status='in_progress').count()
#         completed = user_tasks.filter(status='completed').count()

#         pending_percent = (pending / total * 100) if total else 0
#         in_progress_percent = (in_progress / total * 100) if total else 0
#         completed_percent = (completed / total * 100) if total else 0

#         freelancer_data.append({
#             'user': user,
#             'total': total,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,
#             'pending_percent': pending_percent,
#             'in_progress_percent': in_progress_percent,
#             'completed_percent': completed_percent,
#             'recent_tasks': user_tasks.order_by('-id')[:3]
#         })

#     return render(request, 'manager_dashboard.html', {
#         'tasks': tasks,
#         'today': date.today(),

#         'pending_count': pending_count,
#         'completed_count': completed_count,
#         'overdue_count': overdue_count,

#         'freelancer_data': freelancer_data,

#         'query': query,
#         'status': status,
#         'priority': priority
#     })


# from django.http import JsonResponse

# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     tasks = Task.objects.select_related('assigned_to')

#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     data = []

#     for task in tasks:
#         data.append({
#             'title': task.title,
#             'description': task.description,
#             'assigned_to': task.assigned_to.username,
#             'deadline': str(task.deadline),
#             'status': task.status,
#         })

#     return JsonResponse({'tasks': data})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task, User


# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')

#     tasks = Task.objects.select_related('assigned_to')

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#     # 🎯 FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 WORKLOAD FILTER (based on freelancer pending tasks)
#     if workload:
#         filtered_users = []

#         freelancers = User.objects.filter(role='freelancer')

#         for user in freelancers:
#             pending_count = Task.objects.filter(
#                 assigned_to=user,
#                 status='pending'
#             ).count()

#             if workload == 'free' and pending_count == 0:
#                 filtered_users.append(user.id)

#             elif workload == 'busy' and 1 <= pending_count <= 5:
#                 filtered_users.append(user.id)

#             elif workload == 'overloaded' and pending_count > 5:
#                 filtered_users.append(user.id)

#         tasks = tasks.filter(assigned_to__id__in=filtered_users)

#     # 📦 RESPONSE DATA
#     data = []

#     for task in tasks:
#         data.append({
#             'id': task.id,   # 🔥 REQUIRED
#             'user_id': task.assigned_to.id,   # 🔥 REQUIRED
#             'title': task.title,
#             'description': task.description,
#             'assigned_to': task.assigned_to.username,
#             'deadline': str(task.deadline),
#             'status': task.status,
#             'priority': task.priority,
#         })

#     return JsonResponse({'tasks': data})

from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Task, User

# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')

#     tasks = Task.objects.select_related('assigned_to')
#     freelancers = User.objects.filter(role='freelancer')

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             username__icontains=query
#         )

#     # 🎯 FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 WORKLOAD FILTER
#     if workload:
#         filtered_users = []

#         for user in freelancers:
#             pending_count = Task.objects.filter(
#                 assigned_to=user,
#                 status='pending'
#             ).count()

#             if workload == 'free' and pending_count == 0:
#                 filtered_users.append(user.id)

#             elif workload == 'busy' and 1 <= pending_count <= 5:
#                 filtered_users.append(user.id)

#             elif workload == 'overloaded' and pending_count > 5:
#                 filtered_users.append(user.id)

#         tasks = tasks.filter(assigned_to__id__in=filtered_users)
#         freelancers = freelancers.filter(id__in=filtered_users)

#     return JsonResponse({
#         'tasks': [
#             {
#                 'id': t.id,
#                 'user_id': t.assigned_to.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#                 'priority': t.priority,
#             } for t in tasks
#         ],
#         'freelancers': [
#             {
#                 'id': f.id,
#                 'username': f.username,
#                 'phone': f.phone,
#             } for f in freelancers
#         ]
#     })

from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from .models import Task, User


# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')

#     # 🔥 OPTIMIZED QUERYSETS
#     tasks = Task.objects.select_related('assigned_to')
#     freelancers = User.objects.filter(role='freelancer').annotate(
#         pending_count=Count('tasks', filter=Q(tasks__status='pending'))
#     )

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             Q(username__icontains=query) |
#             Q(phone__icontains=query)
#         )

#     # 🎯 FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 FILTER FREELANCERS BASED ON TASK FILTERS

#     if status or priority:
#         freelancers = freelancers.filter(tasks__in=tasks).distinct()

#     # 🔥 WORKLOAD FILTER (NO LOOPS 🔥)
#     if workload == 'free':
#         freelancers = freelancers.filter(pending_count=0)

#     elif workload == 'busy':
#         freelancers = freelancers.filter(pending_count__gte=1, pending_count__lte=5)

#     elif workload == 'overloaded':
#         freelancers = freelancers.filter(pending_count__gt=5)

#     # filter tasks based on filtered freelancers
#     if workload:
#         tasks = tasks.filter(assigned_to__in=freelancers)

#     # 📦 LIMIT RESULTS (IMPORTANT FOR PERFORMANCE)
#     tasks = tasks[:10]
#     freelancers = freelancers[:10]

    

#     # 📤 RESPONSE
#     return JsonResponse({
#         'tasks': [
#             {
#                 'id': t.id,
#                 'user_id': t.assigned_to.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#                 'priority': t.priority,
#             } for t in tasks
#         ],

#         'freelancers': [
#             {
#                 'id': f.id,
#                 'username': f.username,
#                 'phone': f.phone,
#                 'pending': f.pending_count,  # 🔥 useful
#             } for f in freelancers
#         ]
#     })

from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from .models import Task, User


# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')
#     search_type = request.GET.get('type', 'all')   # 🔥 IMPORTANT

#     # 🔥 BASE QUERYSETS
#     tasks = Task.objects.select_related('assigned_to')
#     freelancers = User.objects.filter(role='freelancer').annotate(
#         pending_count=Count('tasks', filter=Q(tasks__status='pending'))
#     )

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             Q(username__icontains=query) |
#             Q(phone__icontains=query) |
#             Q(tasks__title__icontains=query)   # 🔥 IMPORTANT ADD
#         ).distinct()

#     # 🎯 TASK FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 FILTER FREELANCERS BASED ON FILTERED TASKS
#     if status or priority:
#         freelancers = freelancers.filter(tasks__in=tasks).distinct()

#     # 🔥 WORKLOAD FILTER
#     if workload == 'free':
#         freelancers = freelancers.filter(pending_count=0)

#     elif workload == 'busy':
#         freelancers = freelancers.filter(pending_count__gte=1, pending_count__lte=5)

#     elif workload == 'overloaded':
#         freelancers = freelancers.filter(pending_count__gt=5)

#     # 🔥 FILTER TASKS BASED ON FILTERED FREELANCERS
#     if workload:
#         tasks = tasks.filter(assigned_to__in=freelancers)

#     # 🔥 TYPE FILTER (VERY IMPORTANT)
#     if search_type == 'task':
#         freelancers = freelancers.none()

#     elif search_type == 'freelancer':
#         tasks = tasks.none()

#     # 📦 LIMIT RESULTS
#     tasks = tasks[:10]
#     freelancers = freelancers[:10]

#     # 📤 RESPONSE
#     return JsonResponse({
#         'tasks': [
#             {
#                 'id': t.id,
#                 'user_id': t.assigned_to.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#                 'priority': t.priority,
#             } for t in tasks
#         ],

#         # 'freelancers': [
#         #     {
#         #         'id': f.id,
#         #         'username': f.username,
#         #         'phone': f.phone,
#         #         'pending': f.pending_count,
#         #     } for f in freelancers
#         # ]

#         'freelancers': [
#     {
#         'id': f.id,
#         'username': f.username,
#         'phone': f.phone,
#         'gender': f.gender,
#         'is_approved': f.is_approved,

#         # 🔥 IMAGE FIX (VERY IMPORTANT)
#         'image': f.profile_image.url if f.profile_image else None,

#         # 🔥 FULL STATS
#         'total': f.tasks.count(),
#         'pending': f.tasks.filter(status='pending').count(),
#         'in_progress': f.tasks.filter(status='in_progress').count(),
#         'completed': f.tasks.filter(status='completed').count(),
#     } for f in freelancers
# ]
#     })


from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

# @login_required
# def search_tasks(request):

#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')
#     search_type = request.GET.get('type', 'all')

#     # =====================================================
#     # TASKS
#     # =====================================================

#     tasks = Task.objects.select_related('assigned_to')

#     # =====================================================
#     # FREELANCERS
#     # =====================================================

#     freelancers = User.objects.filter(
#         role='freelancer'
#     ).annotate(
#         pending_count=Count(
#             'tasks',
#             filter=Q(tasks__status='pending')
#         )
#     )

#     # =====================================================
#     # EMPLOYEES
#     # =====================================================

#     employees = User.objects.filter(
#         role='employee'
#     ).annotate(
#         pending_count=Count(
#             'tasks',
#             filter=Q(tasks__status='pending')
#         )
#     )

#     # =====================================================
#     # SEARCH
#     # =====================================================

#     if query:

#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             Q(username__icontains=query) |
#             Q(phone__icontains=query) |
#             Q(tasks__title__icontains=query)
#         ).distinct()

#         employees = employees.filter(
#             Q(username__icontains=query) |
#             Q(phone__icontains=query) |
#             Q(tasks__title__icontains=query)
#         ).distinct()

#     # =====================================================
#     # TASK FILTERS
#     # =====================================================

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # =====================================================
#     # FILTER USERS BASED ON TASKS
#     # =====================================================

#     if status or priority:

#         freelancers = freelancers.filter(
#             tasks__in=tasks
#         ).distinct()

#         employees = employees.filter(
#             tasks__in=tasks
#         ).distinct()

#     # =====================================================
#     # WORKLOAD FILTER
#     # =====================================================

#     if workload == 'free':

#         freelancers = freelancers.filter(
#             pending_count=0
#         )

#         employees = employees.filter(
#             pending_count=0
#         )

#     elif workload == 'busy':

#         freelancers = freelancers.filter(
#             pending_count__gte=1,
#             pending_count__lte=5
#         )

#         employees = employees.filter(
#             pending_count__gte=1,
#             pending_count__lte=5
#         )

#     elif workload == 'overloaded':

#         freelancers = freelancers.filter(
#             pending_count__gt=5
#         )

#         employees = employees.filter(
#             pending_count__gt=5
#         )

#     # =====================================================
#     # FILTER TASKS BASED ON USERS
#     # =====================================================

#     if workload:

#         users = list(freelancers) + list(employees)

#         tasks = tasks.filter(
#             assigned_to__in=users
#         )

#     # =====================================================
#     # TYPE FILTER
#     # =====================================================

#     if search_type == 'task':

#         freelancers = freelancers.none()
#         employees = employees.none()

#     elif search_type == 'freelancer':

#         tasks = tasks.none()
#         employees = employees.none()

#     elif search_type == 'employee':

#         tasks = tasks.none()
#         freelancers = freelancers.none()

#     # =====================================================
#     # LIMIT RESULTS
#     # =====================================================

#     tasks = tasks[:10]
#     freelancers = freelancers[:10]
#     employees = employees[:10]

#     # =====================================================
#     # RESPONSE
#     # =====================================================

#     return JsonResponse({

#         # =================================================
#         # TASKS
#         # =================================================

#         'tasks': [

#             {
#                 'id': t.id,
#                 'user_id': t.assigned_to.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#                 'priority': t.priority,

#             } for t in tasks
#         ],

#         # =================================================
#         # FREELANCERS
#         # =================================================

#         'freelancers': [

#             {
#                 'id': f.id,
#                 'username': f.username,
#                 'phone': f.phone,
#                 'gender': f.gender,
#                 'is_approved': f.is_approved,

#                 'image': (
#                     f.profile_image.url
#                     if f.profile_image
#                     else None
#                 ),

#                 'total': f.tasks.count(),

#                 'pending': f.tasks.filter(
#                     status='pending'
#                 ).count(),

#                 'in_progress': f.tasks.filter(
#                     status='in_progress'
#                 ).count(),

#                 'completed': f.tasks.filter(
#                     status='completed'
#                 ).count(),

#             } for f in freelancers
#         ],

#         # =================================================
#         # EMPLOYEES
#         # =================================================

#         'employees': [

#             {
#                 'id': e.id,
#                 'username': e.username,
#                 'phone': e.phone,
#                 'gender': e.gender,
#                 'is_approved': e.is_approved,

#                 'image': (
#                     e.profile_image.url
#                     if e.profile_image
#                     else None
#                 ),

#                 'total': e.tasks.count(),

#                 'pending': e.tasks.filter(
#                     status='pending'
#                 ).count(),

#                 'in_progress': e.tasks.filter(
#                     status='in_progress'
#                 ).count(),

#                 'completed': e.tasks.filter(
#                     status='completed'
#                 ).count(),

#             } for e in employees
#         ]

#     })


from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def search_tasks(request):

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    workload = request.GET.get('workload')
    search_type = request.GET.get('type', 'all')

    # ==========================================
    # TASKS
    # ==========================================

    tasks = Task.objects.select_related('assigned_to')

    # ==========================================
    # FREELANCERS
    # ==========================================

    freelancers = User.objects.filter(
        userprofile__role='freelancer'
    ).select_related(
        'userprofile'
    ).annotate(
        pending_count=Count(
            'tasks',
            filter=Q(tasks__status='pending')
        )
    )

    # ==========================================
    # EMPLOYEES
    # ==========================================

    employees = User.objects.filter(
        userprofile__role='employee'
    ).select_related(
        'userprofile'
    ).annotate(
        pending_count=Count(
            'tasks',
            filter=Q(tasks__status='pending')
        )
    )

    # ==========================================
    # SEARCH
    # ==========================================

    if query:

        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(assigned_to__username__icontains=query)
        )

        freelancers = freelancers.filter(
            Q(username__icontains=query) |
            Q(userprofile__phone__icontains=query) |
            Q(tasks__title__icontains=query)
        ).distinct()

        employees = employees.filter(
            Q(username__icontains=query) |
            Q(userprofile__phone__icontains=query) |
            Q(tasks__title__icontains=query)
        ).distinct()

    # ==========================================
    # TASK FILTERS
    # ==========================================

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    # ==========================================
    # FILTER USERS BY TASKS
    # ==========================================

    if status or priority:

        freelancers = freelancers.filter(
            tasks__in=tasks
        ).distinct()

        employees = employees.filter(
            tasks__in=tasks
        ).distinct()

    # ==========================================
    # WORKLOAD
    # ==========================================

    if workload == 'free':

        freelancers = freelancers.filter(
            pending_count=0
        )

        employees = employees.filter(
            pending_count=0
        )

    elif workload == 'busy':

        freelancers = freelancers.filter(
            pending_count__gte=1,
            pending_count__lte=5
        )

        employees = employees.filter(
            pending_count__gte=1,
            pending_count__lte=5
        )

    elif workload == 'overloaded':

        freelancers = freelancers.filter(
            pending_count__gt=5
        )

        employees = employees.filter(
            pending_count__gt=5
        )

    # ==========================================
    # FILTER TASKS BY USERS
    # ==========================================

    if workload:

        users = list(freelancers) + list(employees)

        tasks = tasks.filter(
            assigned_to__in=users
        )

    # ==========================================
    # TYPE FILTER
    # ==========================================

    if search_type == 'task':

        freelancers = freelancers.none()
        employees = employees.none()

    elif search_type == 'freelancer':

        tasks = tasks.none()
        employees = employees.none()

    elif search_type == 'employee':

        tasks = tasks.none()
        freelancers = freelancers.none()

    # ==========================================
    # LIMIT
    # ==========================================

    tasks = tasks[:10]
    freelancers = freelancers[:10]
    employees = employees[:10]

    # ==========================================
    # RESPONSE
    # ==========================================
    today = timezone.now().date()
    return JsonResponse({

        # 'tasks': [

        #     {
        #         'id': t.id,
        #         'user_id': t.assigned_to.id,
        #         'title': t.title,
        #         'description': t.description,
        #         'assigned_to': t.assigned_to.username,
        #         'deadline': str(t.deadline),
        #         'status': t.status,
        #         'priority': t.priority,

        #     } for t in tasks
        # ],

        'tasks': [

        {
            'id': t.id,
            'user_id': t.assigned_to.id,
            'title': t.title,
            'description': t.description,
            'assigned_to': t.assigned_to.username,
            'deadline': str(t.deadline),
            'status': t.status,
            'priority': t.priority,

            'is_overdue': (
                t.deadline
                and t.deadline < today
                and t.status != "completed"
            ),

        } for t in tasks
    ],

        'freelancers': [

            {
                'id': f.id,
                'username': f.username,
                'phone': f.userprofile.phone,
                'gender': f.userprofile.gender,
                'is_approved': f.userprofile.is_approved,

                'image': (
                    f.userprofile.profile_image.url
                    if f.userprofile.profile_image
                    else None
                ),

                'total': f.tasks.count(),

                'pending': f.tasks.filter(
                    status='pending'
                ).count(),

                'in_progress': f.tasks.filter(
                    status='in_progress'
                ).count(),

                'completed': f.tasks.filter(
                    status='completed'
                ).count(),
            }

            for f in freelancers
        ],

        'employees': [

            {
                'id': e.id,
                'username': e.username,
                'phone': e.userprofile.phone,
                'gender': e.userprofile.gender,
                'is_approved': e.userprofile.is_approved,

                'image': (
                    e.userprofile.profile_image.url
                    if e.userprofile.profile_image
                    else None
                ),

                'total': e.tasks.count(),

                'pending': e.tasks.filter(
                    status='pending'
                ).count(),

                'in_progress': e.tasks.filter(
                    status='in_progress'
                ).count(),

                'completed': e.tasks.filter(
                    status='completed'
                ).count(),
            }

            for e in employees
        ]

    })

from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Task, User


# @login_required
# def search_tasks(request):
#     query = request.GET.get('q', '').strip()
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')
#     workload = request.GET.get('workload')

#     tasks = Task.objects.select_related('assigned_to')
#     freelancers = User.objects.filter(role='freelancer')

#     # 🔍 SEARCH
#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             username__icontains=query
#         )

#     # 🎯 TASK FILTERS
#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 WORKLOAD FILTER
#     if workload:
#         filtered_users = []

#         for user in freelancers:
#             pending_count = Task.objects.filter(
#                 assigned_to=user,
#                 status='pending'
#             ).count()

#             if workload == 'free' and pending_count == 0:
#                 filtered_users.append(user.id)

#             elif workload == 'busy' and 1 <= pending_count <= 5:
#                 filtered_users.append(user.id)

#             elif workload == 'overloaded' and pending_count > 5:
#                 filtered_users.append(user.id)

#         tasks = tasks.filter(assigned_to__id__in=filtered_users)
#         freelancers = freelancers.filter(id__in=filtered_users)

#     # 📦 RESPONSE
#     return JsonResponse({
#         'tasks': [
#             {
#                 'id': t.id,
#                 'user_id': t.assigned_to.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#                 'priority': t.priority,
#             } for t in tasks
#         ],

#         'freelancers': [
#             {
#                 'id': f.id,
#                 'username': f.username,
#                 'phone': f.phone,
#             } for f in freelancers
#         ]
#     })



from django.http import JsonResponse
from django.db.models import Q

# def search_tasks(request):
#     query = request.GET.get('q', '')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     tasks = Task.objects.select_related('assigned_to')
#     freelancers = User.objects.filter(role='freelancer')

#     if query:
#         tasks = tasks.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(assigned_to__username__icontains=query)
#         )

#         freelancers = freelancers.filter(
#             username__icontains=query
#         )

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     return JsonResponse({
#         'tasks': [
#             {
#                 'id': t.id,
#                 'title': t.title,
#                 'description': t.description,
#                 'assigned_to': t.assigned_to.username,
#                 'deadline': str(t.deadline),
#                 'status': t.status,
#             } for t in tasks
#         ],
#         'freelancers': [
#             {
#                 'id': f.id,
#                 'username': f.username
#             } for f in freelancers
#         ]
#     })

# @login_required
# def freelancer_detail(request, user_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     freelancer = User.objects.get(id=user_id, role='freelancer')

#     tasks = Task.objects.filter(assigned_to=freelancer)

#     return render(request, 'freelancer_detail.html', {
#         'freelancer': freelancer,
#         'tasks': tasks
#     })

from django.shortcuts import get_object_or_404

# @login_required
# def freelancer_detail(request, user_id):

#     if not request.user.is_superuser:
#         return redirect('login')

#     freelancer = get_object_or_404(
#         User,
#         id=user_id,
#         userprofile__role='freelancer'
#     )

#     tasks = Task.objects.filter(
#         assigned_to=freelancer
#     )

#     return render(
#         request,
#         'freelancer_detail.html',
#         {
#             'freelancer': freelancer,
#             'tasks': tasks
#         }
#     )

@login_required
def freelancer_detail(request, user_id):

    if not request.user.is_superuser:
        return redirect('login')

    freelancer = get_object_or_404(
        User,
        id=user_id,
    )

    profile = get_object_or_404(
        UserProfile,
        user=freelancer
    )

    tasks = Task.objects.filter(
        assigned_to=freelancer
    )

    return render(
        request,
        'freelancer_detail.html',
        {
            'freelancer': freelancer,
            'profile': profile,
            'tasks': tasks
        }
    )

# @login_required
# def task_detail(request, task_id):
#     task = Task.objects.select_related('assigned_to').get(id=task_id)

#     return render(request, 'task_detail.html', {
#         'task': task
#     })


# @login_required
# def task_detail(request, task_id):

#     task = Task.objects.select_related(
#         'assigned_to'
#     ).get(id=task_id)

#     profile = UserProfile.objects.get(
#         user=request.user
#     )

#     return render(
#         request,
#         'task_detail.html',
#         {
#             'task': task,
#             'profile': profile
#         }
#     )

@login_required
def task_detail(request, task_id):

    task = Task.objects.select_related(
        "assigned_to",
        "assigned_to__userprofile"
    ).get(id=task_id)

    profile = UserProfile.objects.get(user=request.user)

    assigned_role = task.assigned_to.userprofile.role

    return render(
        request,
        "task_detail.html",
        {
            "task": task,
            "profile": profile,
            "assigned_role": assigned_role,
        },
    )
from django.http import JsonResponse

# @login_required
# def freelancer_detail(request, user_id):
#     user = User.objects.get(id=user_id, role='freelancer')
#     tasks = Task.objects.filter(assigned_to=user)

#     return JsonResponse({
#         'username': user.username,
#         'email': user.email,
#         'phone': user.phone,
#         'tasks': [
#             {
#                 'title': t.title,
#                 'status': t.status,
#                 'deadline': str(t.deadline)
#             } for t in tasks
#         ]
#     })


# @login_required
# def freelancer_detail(request, user_id):

#     user = User.objects.get(id=user_id, role='freelancer')
#     tasks = Task.objects.filter(assigned_to=user)

#     return JsonResponse({

#         # BASIC INFO
#         'username': user.username,
#         'email': user.email,
#         'phone': user.phone,

#         # 🔥 ADD THESE (VERY IMPORTANT)
#         'image': user.profile_image.url if user.profile_image else None,
#         'gender': user.gender,
#         'is_approved': user.is_approved,

#         # TASKS
#         'tasks': [
#             {
#                 'title': t.title,
#                 'status': t.status,
#                 'deadline': str(t.deadline),
#                 'priority': t.priority
#             } for t in tasks
#         ]
#     })
# @login_required
# def freelancer_dashboard(request):
#     tasks = Task.objects.filter(assigned_to=request.user)
#     return render(request, 'freelancer_dashboard.html', {'tasks': tasks})


from .forms import TaskForm

# @login_required
# def create_task(request):
#     if request.user.role != 'manager':
#         return redirect('login')

#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard')
#     else:
#         form = TaskForm()

#     return render(request, 'create_task.html', {'form': form})


@login_required
def update_status(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.user != task.assigned_to:
        return redirect('login')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
        return redirect('freelancer_dashboard')

    return render(request, 'update_status.html', {'task': task})
# @login_required
# def create_freelancer(request):
#     if request.user.role != 'manager':
#         return redirect('login')

#     if request.method == 'POST':
#         form = FreelancerForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'freelancer'   # 👈 automatically set role
#             user.save()
#             return redirect('manager_dashboard')
#     else:
#         form = FreelancerForm()

#     return render(request, 'create_freelancer.html', {'form': form})

# @login_required
# def create_freelancer(request):
#     if request.user.role != 'manager':
#         return redirect('login')

#     if request.method == 'POST':
#         form = FreelancerForm(request.POST, request.FILES)  # 🔥 FIX HERE

#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'freelancer'
#             user.save()
#             return redirect('manager_dashboard')
#         else:
#             print(form.errors)  # optional debug

#     else:
#         form = FreelancerForm()

#     return render(request, 'create_freelancer.html', {'form': form})


from .models import UserProfile

@login_required
def create_freelancer(request):

    if not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':

        form = FreelancerForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role='freelancer',
                phone=form.cleaned_data.get('phone'),
                gender=form.cleaned_data.get('gender'),
                profile_image=form.cleaned_data.get('profile_image'),
                is_approved=True
            )

            return redirect('manager_dashboard')

    else:
        form = FreelancerForm()

    return render(
        request,
        'create_freelancer.html',
        {'form': form}
    )


from django.shortcuts import get_object_or_404

# @login_required
# def edit_freelancer(request, user_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     freelancer = get_object_or_404(User, id=user_id, role='freelancer')

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=freelancer)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard')
#     else:
#         form = ProfileForm(instance=freelancer)

#     return render(request, 'edit_freelancer.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfileForm


# @login_required
# def edit_freelancer(request, user_id):

#     # Manager/Admin check
#     if not request.user.is_superuser:
#         return redirect('login')

#     user = get_object_or_404(User, id=user_id)

#     profile = get_object_or_404(
#         UserProfile,
#         user=user,
#         role='freelancer'
#     )

#     if request.method == 'POST':
#         form = ProfileForm(
#             request.POST,
#             request.FILES,
#             instance=profile
#         )

#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard')

#     else:
#         form = ProfileForm(instance=profile)

#     return render(
#         request,
#         'edit_freelancer.html',
#         {
#             'form': form,
#             'profile': profile,
#             'user_obj': user
#         }
#     )

@login_required
def edit_freelancer(request, user_id):

    if request.user.userprofile.role != 'manager':
        return redirect('login')

    freelancer = get_object_or_404(
        User,
        id=user_id,
        userprofile__role='freelancer'
    )

    profile = freelancer.userprofile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        'edit_freelancer.html',
        {
            'form': form,
            'freelancer': freelancer,
            'profile': profile
        }
    )

# @login_required
# def delete_freelancer(request, user_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     freelancer = get_object_or_404(User, id=user_id, role='freelancer')
#     freelancer.delete()

#     return redirect('manager_dashboard')


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete_freelancer(request, user_id):

    if not request.user.is_superuser:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    user.delete()

    return redirect('manager_dashboard')

# @login_required
# def create_task(request):
#     if request.user.role != 'manager':
#         return redirect('login')

#     if request.method == 'POST':
#         form = TaskForm(request.POST)

#         if form.is_valid():
#             form.save()
#             print("✅ Task saved")   # debug
#             return redirect('manager_dashboard')
#         else:
#             print("❌ Form errors:", form.errors)   # 👈 VERY IMPORTANT

#     else:
#         form = TaskForm()

#     return render(request, 'create_task.html', {'form': form})

from .models import UserProfile

@login_required
def create_task(request):

    # Allow only superuser/admin
    if not request.user.is_superuser:
        return redirect('freelancer_dashboard')

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')

        else:
            print(form.errors)

    else:
        form = TaskForm()

    return render(
        request,
        'create_task.html',
        {'form': form}
    )

@login_required
def employee_list(request):
    if request.user.role != 'manager':
        return redirect('login')

    freelancers = User.objects.filter(role='freelancer')

    return render(request, 'employee_list.html', {'freelancers': freelancers})


# @login_required
# def create_employee(request):

#     if request.user.role != 'manager':
#         return redirect('login')

#     if request.method == 'POST':

#         form = FreelancerForm(request.POST, request.FILES)

#         if form.is_valid():

#             user = form.save(commit=False)

#             # 👨‍💼 EMPLOYEE ROLE
#             user.role = 'employee'

#             user.save()

#             return redirect('manager_dashboard')

#         else:
#             print(form.errors)

#     else:
#         form = FreelancerForm()

#     return render(request, 'create_employee.html', {
#         'form': form
#     })


from .models import UserProfile

@login_required
def create_employee(request):

    if not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':

        form = FreelancerForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role='employee',
                phone=form.cleaned_data.get('phone'),
                gender=form.cleaned_data.get('gender'),
                profile_image=form.cleaned_data.get('profile_image'),
                is_approved=True
            )

            return redirect('manager_dashboard')

    else:
        form = FreelancerForm()

    return render(
        request,
        'create_employee.html',
        {'form': form}
    )
from django.shortcuts import get_object_or_404

# =====================================================
# 👨‍💼 EDIT EMPLOYEE
# =====================================================

# @login_required
# def edit_employee(request, user_id):

#     if request.user.role != 'manager':
#         return redirect('login')

#     employee = get_object_or_404(
#         User,
#         id=user_id,
#         role='employee'
#     )

#     if request.method == 'POST':

#         form = ProfileForm(
#             request.POST,
#             request.FILES,
#             instance=employee
#         )

#         if form.is_valid():

#             form.save()

#             return redirect('manager_dashboard')

#     else:

#         form = ProfileForm(instance=employee)

#     return render(request, 'edit_employee.html', {
#         'form': form
#     })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def edit_employee(request, user_id):

    # Manager check
    if request.user.userprofile.role != 'manager':
        return redirect('login')

    employee = get_object_or_404(
        User,
        id=user_id,
        userprofile__role='employee'
    )

    profile = employee.userprofile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        'edit_employee.html',
        {
            'form': form,
            'employee': employee,
            'profile': profile
        }
    )


# =====================================================
# 🗑 DELETE EMPLOYEE
# =====================================================

# @login_required
# def delete_employee(request, user_id):

#     if request.user.role != 'manager':
#         return redirect('login')

#     employee = get_object_or_404(
#         User,
#         id=user_id,
#         role='employee'
#     )

#     employee.delete()

#     return redirect('manager_dashboard')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User


@login_required
def delete_employee(request, user_id):

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'manager':
        return redirect('login')

    employee = get_object_or_404(
        User,
        id=user_id
    )

    employee.delete()

    return redirect('manager_dashboard')

@login_required
def employee_list(request):

    if request.user.role != 'manager':
        return redirect('login')

    # 👨‍💻 FREELANCERS
    freelancers = User.objects.filter(
        role='freelancer'
    )

    # 👨‍💼 EMPLOYEES
    employees = User.objects.filter(
        role='employee'
    )

    return render(request, 'employee_list.html', {

        'freelancers': freelancers,

        'employees': employees

    })

# =====================================================
# 👨‍💼 EMPLOYEE DETAIL PAGE
# =====================================================

# @login_required
# def employee_detail(request, user_id):

#     # 🔒 ONLY MANAGER
#     if request.user.role != 'manager':
#         return redirect('login')

#     # 👨‍💼 GET EMPLOYEE
#     employee = User.objects.get(
#         id=user_id,
#         role='employee'
#     )

#     # 📋 EMPLOYEE TASKS
#     tasks = Task.objects.filter(
#         assigned_to=employee
#     )

#     return render(request, 'employee_detail.html', {

#         'employee': employee,

#         'tasks': tasks

#     })

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def employee_detail(request, user_id):

    # Only manager can access
    if request.user.userprofile.role != 'manager':
        return redirect('login')

    # Get employee user
    employee = get_object_or_404(
        User,
        id=user_id,
        userprofile__role='employee'
    )

    # Employee tasks
    tasks = Task.objects.filter(
        assigned_to=employee
    )

    return render(
        request,
        'employee_detail.html',
        {
            'employee': employee,
            'profile': employee.userprofile,
            'tasks': tasks
        }
    )


# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'freelancer'   # 👈 auto assign role
#             user.is_approved = False  
#             user.save()
#             return redirect('login')
#     else:
#         form = SignupForm()

#     return render(request, 'signup.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import SignupForm

# def signup_view(request, role):
#     if request.method == 'POST':
#         form = SignupForm(request.POST, request.FILES)  # 🔥 include FILES

#         if form.is_valid():
#             user = form.save(commit=False)

#             # 🔥 SET ROLE BASED ON URL
#             user.role = role

#             # 🔥 approval system
#             user.is_approved = False  

#             user.save()
#             return redirect('login')
#     else:
#         form = SignupForm()

#     return render(request, 'signup.html', {
#         'form': form,
#         'role': role
#     })


# def signup_view(request, role):
#     if request.method == 'POST':
#         form = SignupForm(request.POST, request.FILES)

#         if form.is_valid():
#             user = form.save(commit=False)

#             user.role = role
#             user.is_approved = False  

#             user.save()

#             return redirect('login')

#     else:
#         form = SignupForm()

#     return render(request, 'signup.html', {
#         'form': form,
#         'role': role
#     })


from .models import UserProfile

def signup_view(request, role):

    if request.method == 'POST':

        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=role,
                phone=form.cleaned_data.get('phone'),
                gender=form.cleaned_data.get('gender'),
                profile_image=form.cleaned_data.get('profile_image'),
                is_approved=False
            )

            return redirect('login')

    else:
        form = SignupForm()

    return render(
        request,
        'signup.html',
        {
            'form': form,
            'role': role
        }
    )

# @login_required
# def profile(request):
#     return render(request, 'profile.html', {'user': request.user})

from .models import UserProfile

# @login_required
# def profile(request):
#     profile = UserProfile.objects.get(user=request.user)

#     return render(request, 'profile.html', {
#         'profile': profile
#     })

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'manager'
        }
    )

    return render(
        request,
        'profile.html',
        {
            'profile': profile
        }
    )

# @login_required
# def freelancer_dashboard(request):
#     tasks = Task.objects.filter(assigned_to=request.user)

#     pending = tasks.filter(status='pending')
#     in_progress = tasks.filter(status='in_progress')
#     completed = tasks.filter(status='completed')

#     return render(request, 'freelancer_dashboard.html', {
#         'tasks': tasks,
#         'pending': pending,
#         'in_progress': in_progress,
#         'completed': completed
#     })

from django.db.models import Q, Case, When, Value, IntegerField

# @login_required
# def freelancer_dashboard(request):

#     tasks = Task.objects.filter(
#         assigned_to=request.user
#     )

#     # 🔍 Search Filters
#     q = request.GET.get('q')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     if q:
#         tasks = tasks.filter(
#             Q(title__icontains=q) |
#             Q(description__icontains=q)
#         )

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # 🔥 High Priority First
#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     pending = tasks.filter(
#         status='pending'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     in_progress = tasks.filter(
#         status='in_progress'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     completed = tasks.filter(
#         status='completed'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         {
#             'tasks': tasks,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,
#         }
#     )

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, Value, IntegerField

# @login_required
# def freelancer_dashboard(request):

#     # Only tasks assigned to logged-in user
#     tasks = Task.objects.filter(
#         assigned_to=request.user
#     )

#     # Search
#     q = request.GET.get('q', '')
#     status = request.GET.get('status', '')
#     priority = request.GET.get('priority', '')

#     if q:
#         tasks = tasks.filter(
#             Q(title__icontains=q) |
#             Q(description__icontains=q)
#         )

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     pending = tasks.filter(
#         status='pending'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     in_progress = tasks.filter(
#         status='in_progress'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     completed = tasks.filter(
#         status='completed'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         {
#             'all_tasks': tasks,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,
#             'q': q,
#             'status': status,
#             'priority': priority,
#         }
#     )

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, Value, IntegerField

# @login_required
# def freelancer_dashboard(request):

#     # All tasks assigned to logged-in user
#     tasks = Task.objects.filter(
#         assigned_to=request.user
#     )

#     # For dropdown list
#     user_tasks = Task.objects.filter(
#         assigned_to=request.user
#     )

#     # Dropdown task filter
#     task_id = request.GET.get('task_id', '')

#     # Status filter
#     status = request.GET.get('status', '')

#     # Priority filter
#     priority = request.GET.get('priority', '')

#     # Apply filters
#     if task_id:
#         tasks = tasks.filter(id=task_id)

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     # High Priority First
#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     pending = tasks.filter(
#         status='pending'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     in_progress = tasks.filter(
#         status='in_progress'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     completed = tasks.filter(
#         status='completed'
#     ).annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-id'
#     )

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         {
#             'user_tasks': user_tasks,      # dropdown list
#             'all_tasks': tasks,
#             'pending': pending,
#             'in_progress': in_progress,
#             'completed': completed,
#             'task_id': task_id,
#             'status': status,
#             'priority': priority,
#         }
#     )

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, Value, IntegerField
from .models import Task


# @login_required
# def freelancer_dashboard(request):

#     user_tasks = Task.objects.filter(
#         assigned_to=request.user
#     ).order_by('-created_at')


#     tasks = user_tasks

#     task_id = request.GET.get('task_id')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     if task_id:
#         tasks = tasks.filter(id=task_id)

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     tasks = tasks.annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-deadline'
#     )

#     pending = tasks.filter(status='pending')
#     in_progress = tasks.filter(status='in_progress')
#     completed = tasks.filter(status='completed')

#     context = {
#         'user_tasks': user_tasks,

#         'pending': pending,
#         'in_progress': in_progress,
#         'completed': completed,

#         'pending_count': pending.count(),
#         'progress_count': in_progress.count(),
#         'completed_count': completed.count(),

#         'task_id': task_id,
#         'status': status,
#         'priority': priority,
#     }

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         context
#     )


from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from .models import Task


# def freelancer_dashboard(request):

#     user_tasks = Task.objects.filter(
#         assigned_to=request.user
#     ).order_by('-created_at')

#     tasks = user_tasks

#     task_id = request.GET.get('task_id')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     if task_id:
#         tasks = tasks.filter(id=task_id)

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     tasks = tasks.annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-deadline'
#     )

#     pending = tasks.filter(status='pending')
#     in_progress = tasks.filter(status='in_progress')
#     completed = tasks.filter(status='completed')

#     # PAYMENT SUMMARY

#     pending_payment = 0
#     partial_payment = 0
#     paid_payment = 0

#     for task in user_tasks:

#         if task.payment_status == 'pending':
#             pending_payment += task.balance_amount

#         elif task.payment_status == 'partial':
#             partial_payment += task.balance_amount

#         elif task.payment_status == 'paid':
#             paid_payment += task.paid_amount

#     context = {
#         'user_tasks': user_tasks,

#         'pending': pending,
#         'in_progress': in_progress,
#         'completed': completed,

#         'pending_count': pending.count(),
#         'progress_count': in_progress.count(),
#         'completed_count': completed.count(),

#         'pending_payment': pending_payment,
#         'partial_payment': partial_payment,
#         'paid_payment': paid_payment,

#         'task_id': task_id,
#         'status': status,
#         'priority': priority,
#     }

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         context
#     )

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from .models import Task


# @login_required
# def freelancer_dashboard(request):

#     user_tasks = Task.objects.filter(
#         assigned_to=request.user
#     ).order_by('-created_at')

#     tasks = user_tasks

#     task_id = request.GET.get('task_id')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     if task_id:
#         tasks = tasks.filter(id=task_id)

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     tasks = tasks.annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-deadline'
#     )

#     pending = tasks.filter(status='pending')
#     in_progress = tasks.filter(status='in_progress')
#     completed = tasks.filter(status='completed')

#     # PAYMENT SUMMARY

#     total_earnings = 0
#     received_payment = 0
#     balance_payment = 0

#     for task in user_tasks:

#         total_earnings += task.payment_amount or 0
#         received_payment += task.paid_amount or 0
#         balance_payment += task.balance_amount or 0

#     context = {

#         'user_tasks': user_tasks,

#         'pending': pending,
#         'in_progress': in_progress,
#         'completed': completed,

#         'pending_count': pending.count(),
#         'progress_count': in_progress.count(),
#         'completed_count': completed.count(),

#         'total_earnings': total_earnings,
#         'received_payment': received_payment,
#         'balance_payment': balance_payment,

#         'task_id': task_id,
#         'status': status,
#         'priority': priority,
#     }

#     return render(
#         request,
#         'freelancer_dashboard.html',
#         context
#     )



# @login_required
# def freelancer_dashboard(request):

#     profile = UserProfile.objects.get(user=request.user)

#     user_tasks = Task.objects.filter(
#         assigned_to=request.user
#     ).order_by('-created_at')

#     tasks = user_tasks

#     task_id = request.GET.get('task_id')
#     status = request.GET.get('status')
#     priority = request.GET.get('priority')

#     if task_id:
#         tasks = tasks.filter(id=task_id)

#     if status:
#         tasks = tasks.filter(status=status)

#     if priority:
#         tasks = tasks.filter(priority=priority)

#     priority_order = Case(
#         When(priority='high', then=Value(1)),
#         When(priority='medium', then=Value(2)),
#         When(priority='low', then=Value(3)),
#         output_field=IntegerField()
#     )

#     tasks = tasks.annotate(
#         priority_rank=priority_order
#     ).order_by(
#         'priority_rank',
#         '-deadline'
#     )

#     pending = tasks.filter(status='pending')
#     in_progress = tasks.filter(status='in_progress')
#     completed = tasks.filter(status='completed')

#     # PAYMENT SUMMARY
#     total_earnings = 0
#     received_payment = 0
#     balance_payment = 0

#     # Only calculate payments for freelancers
#     if profile.role == "freelancer":
#         for task in user_tasks:
#             total_earnings += task.payment_amount or 0
#             received_payment += task.paid_amount or 0
#             balance_payment += task.balance_amount or 0

#     context = {

#         "profile": profile,

#         "user_tasks": user_tasks,

#         "pending": pending,
#         "in_progress": in_progress,
#         "completed": completed,

#         "pending_count": pending.count(),
#         "progress_count": in_progress.count(),
#         "completed_count": completed.count(),

#         "total_earnings": total_earnings,
#         "received_payment": received_payment,
#         "balance_payment": balance_payment,

#         "task_id": task_id,
#         "status": status,
#         "priority": priority,
#     }

#     return render(
#         request,
#         "freelancer_dashboard.html",
#         context
#     )

from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

@login_required
def freelancer_dashboard(request):

    profile = UserProfile.objects.get(user=request.user)

    today = timezone.now().date()

    user_tasks = Task.objects.filter(
        assigned_to=request.user
    ).order_by('-created_at')

    tasks = user_tasks

    task_id = request.GET.get('task_id')
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if task_id:
        tasks = tasks.filter(id=task_id)

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    priority_order = Case(
        When(priority='high', then=Value(1)),
        When(priority='medium', then=Value(2)),
        When(priority='low', then=Value(3)),
        output_field=IntegerField()
    )

    tasks = tasks.annotate(
        priority_rank=priority_order
    ).order_by(
        'priority_rank',
        '-deadline'
    )

    pending = tasks.filter(status='pending')
    in_progress = tasks.filter(status='in_progress')
    completed = tasks.filter(status='completed')

    overdue_tasks = tasks.filter(
        deadline__lt=today
    ).exclude(
        status='completed'
    )

    # PAYMENT SUMMARY
    total_earnings = 0
    received_payment = 0
    balance_payment = 0

    # Only calculate payments for freelancers
    if profile.role == "freelancer":
        for task in user_tasks:
            total_earnings += task.payment_amount or 0
            received_payment += task.paid_amount or 0
            balance_payment += task.balance_amount or 0

    context = {

        "profile": profile,

        "today": today,

        "user_tasks": user_tasks,
        "tasks": tasks,

        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,

        "pending_count": pending.count(),
        "progress_count": in_progress.count(),
        "completed_count": completed.count(),
        "overdue_count": overdue_tasks.count(),

        "total_earnings": total_earnings,
        "received_payment": received_payment,
        "balance_payment": balance_payment,

        "task_id": task_id,
        "status": status,
        "priority": priority,
    }

    return render(
        request,
        "freelancer_dashboard.html",
        context
    )

from django.shortcuts import get_object_or_404

@login_required
# def edit_task(request, task_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     task = get_object_or_404(Task, id=task_id)

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard')
#     else:
#         form = TaskForm(instance=task)

#     return render(request, 'edit_task.html', {'form': form})

# def edit_task(request, task_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     task = get_object_or_404(Task, id=task_id)

#     if request.method == 'POST':

#         form = TaskForm(request.POST, instance=task)

#         print("POST DATA:", request.POST)

#         if form.is_valid():
#             print("FORM VALID")
#             form.save()
#             return redirect('manager_dashboard')

#         else:
#             print("FORM ERRORS:", form.errors)

#     else:
#         form = TaskForm(instance=task)

#     return render(request, 'edit_task.html', {'form': form})

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404

# @login_required
def edit_task(request, task_id):

    # Only admin/superuser can edit tasks
    if not request.user.is_superuser:
        return redirect('login')

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task
        )

        # if form.is_valid():
        #     form.save()
        #     return redirect('manager_dashboard')

        if form.is_valid():

            task = form.save(commit=False)

            if not task.payment_amount:

                task.payment_status = 'pending'

            elif task.paid_amount <= 0:

                task.payment_status = 'pending'

            elif task.paid_amount < task.payment_amount:

                task.payment_status = 'partial'

            else:

                task.payment_status = 'paid'

            if task.payment_amount and task.paid_amount > task.payment_amount:

                form.add_error(
                    'paid_amount',
                    'Paid amount cannot exceed task amount.'
                )

            task.save()

            return redirect('manager_dashboard')

        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'edit_task.html',
        {
            'form': form,
            'task': task
        }
    )

# @login_required
# def delete_task(request, task_id):
#     if request.user.role != 'manager':
#         return redirect('login')

#     task = get_object_or_404(Task, id=task_id)
#     task.delete()

#     return redirect('manager_dashboard')

@login_required
def delete_task(request, task_id):

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'manager':
        return redirect('login')

    task = get_object_or_404(Task, id=task_id)

    task.delete()

    return redirect('manager_dashboard')

# @login_required
# def edit_profile(request):
#     user = request.user

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=user)

#     return render(request, 'edit_profile.html', {'form': form})

@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'manager' if request.user.is_staff else 'employee'
        }
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {
            'form': form,
            'profile': profile,
            'user': request.user
        }
    )

from django.contrib.auth import logout

@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    return redirect('login')


@login_required
def freelancer_tasks(request, user_id):
    if request.user.role != 'manager':
        return redirect('login')

    freelancer = User.objects.get(id=user_id, role='freelancer')
    tasks = Task.objects.filter(assigned_to=freelancer)

    return render(request, 'freelancer_tasks.html', {
        'freelancer': freelancer,
        'tasks': tasks
    })

# from django.shortcuts import redirect, get_object_or_404

# @login_required
# def approve_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     user.is_approved = True
#     user.save()

#     return redirect('manager_dashboard')

from django.shortcuts import get_object_or_404

@login_required
def approve_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    profile = get_object_or_404(
        UserProfile,
        user=user
    )

    profile.is_approved = True
    profile.save()

    return redirect('manager_dashboard')


# ==============================================================
# WORK REQUEST VIEWS — Phase 1
# Append this block to the bottom of tasks/views.py
# ==============================================================

from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import WorkRequest


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def _get_profile_or_403(request):
    """Return the UserProfile for request.user or raise 403."""
    try:
        return request.user.userprofile
    except UserProfile.DoesNotExist:
        return None


def _is_manager(request):
    """True if the logged-in user is a superuser or has manager role."""
    if request.user.is_superuser:
        return True
    profile = _get_profile_or_403(request)
    return profile is not None and profile.role == 'manager'


def _is_staff_member(request):
    """True for employees, freelancers, and managers."""
    if request.user.is_superuser:
        return True
    profile = _get_profile_or_403(request)
    return profile is not None and profile.role in ('manager', 'employee', 'freelancer')


# ------------------------------------------------------------------
# Employee / Freelancer: My Requests
# ------------------------------------------------------------------

@login_required
def my_requests(request):
    """
    List all WorkRequests submitted by the currently logged-in user.
    Employees and freelancers land here.
    """
    requests_qs = WorkRequest.objects.filter(
        requested_by=request.user
    ).order_by('-created_at')

    # Simple status filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)

    status_choices = WorkRequest.STATUS_CHOICES

    return render(request, 'tasks/my_requests.html', {
        'work_requests':  requests_qs,
        'status_filter':  status_filter,
        'status_choices': status_choices,
    })


# ------------------------------------------------------------------
# Employee / Freelancer: Create Request
# ------------------------------------------------------------------

# @login_required
# def create_work_request(request):
#     print("===== CREATE WORK REQUEST VIEW CALLED =====")
#     """
#     Allow any logged-in employee or freelancer to submit a new WorkRequest.
#     """
#     if not _is_staff_member(request):
#         return redirect('login')

#     if request.method == 'POST':
#         customer_name = request.POST.get('customer_name', '').strip()
#         title         = request.POST.get('title', '').strip()
#         description   = request.POST.get('description', '').strip()
#         priority      = request.POST.get('priority', 'medium')
#         required_date = request.POST.get('required_date') or None

#         errors = []
#         if not customer_name:
#             errors.append('Customer name is required.')
#         if not title:
#             errors.append('Title is required.')
#         if not description:
#             errors.append('Description is required.')

#         if errors:
#             # return render(request, 'tasks/work_request_form.html', {
#             #     'errors':        errors,
#             #     'form_data':     request.POST,
#             #     'priority_choices': WorkRequest.PRIORITY_CHOICES,
#             #     'action':        'Create',
#             # })

#             return render(request, 'tasks/work_request_create.html', {
#             'errors': errors,
#             'form_data': request.POST,
#             'priority_choices': WorkRequest.PRIORITY_CHOICES,
#         })

#         WorkRequest.objects.create(
#             requested_by=request.user,
#             customer_name=customer_name,
#             title=title,
#             description=description,
#             priority=priority,
#             required_date=required_date,
#             status='pending',
#         )

#         messages.success(request, 'Work request submitted successfully.')
#         return redirect('my_requests')

#     # return render(request, 'tasks/work_request_form.html', {
#     #     'priority_choices': WorkRequest.PRIORITY_CHOICES,
#     #     'action': 'Create',
#     # })

#     return render(request, 'tasks/work_request_create.html', {
#     'priority_choices': WorkRequest.PRIORITY_CHOICES,
# })


@login_required
def create_work_request(request):

    if not _is_staff_member(request):
        return redirect('login')

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name', '').strip()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', 'medium')
        required_date = request.POST.get('required_date') or None

        errors = []

        if not customer_name:
            errors.append("Customer name is required.")

        if not title:
            errors.append("Title is required.")

        if not description:
            errors.append("Description is required.")

        if errors:
            return render(
                request,
                "tasks/work_request_create.html",
                {
                    "errors": errors,
                    "form_data": request.POST,
                    "priority_choices": WorkRequest.PRIORITY_CHOICES,
                },
            )

        WorkRequest.objects.create(
            requested_by=request.user,
            customer_name=customer_name,
            title=title,
            description=description,
            priority=priority,
            required_date=required_date,
            status="pending",
        )

        messages.success(request, "Work Request submitted successfully.")
        return redirect("my_requests")

    return render(
        request,
        "tasks/work_request_create.html",
        {
            "priority_choices": WorkRequest.PRIORITY_CHOICES,
        },
    )

# ------------------------------------------------------------------
# Employee / Freelancer: Edit own pending request
# ------------------------------------------------------------------

@login_required
def edit_work_request(request, request_id):
    """
    Allow the submitter to edit their own WorkRequest while it is still pending.
    """
    work_request = get_object_or_404(WorkRequest, id=request_id)

    # Only the submitter may edit, and only while pending
    if work_request.requested_by != request.user:
        messages.error(request, 'You can only edit your own requests.')
        return redirect('my_requests')

    if not work_request.is_pending:
        messages.warning(request, 'Only pending requests can be edited.')
        return redirect('my_requests')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        title         = request.POST.get('title', '').strip()
        description   = request.POST.get('description', '').strip()
        priority      = request.POST.get('priority', 'medium')
        required_date = request.POST.get('required_date') or None

        errors = []
        if not customer_name:
            errors.append('Customer name is required.')
        if not title:
            errors.append('Title is required.')
        if not description:
            errors.append('Description is required.')

        if errors:
            return render(request, 'tasks/work_request_form.html', {
                'errors':           errors,
                'form_data':        request.POST,
                'priority_choices': WorkRequest.PRIORITY_CHOICES,
                'work_request':     work_request,
                'action':           'Edit',
            })

        work_request.customer_name = customer_name
        work_request.title         = title
        work_request.description   = description
        work_request.priority      = priority
        work_request.required_date = required_date
        work_request.save()

        messages.success(request, 'Work request updated.')
        return redirect('my_requests')

    return render(request, 'tasks/work_request_form.html', {
        'priority_choices': WorkRequest.PRIORITY_CHOICES,
        'work_request':     work_request,
        'action':           'Edit',
    })


# ------------------------------------------------------------------
# Manager: All Requests List
# ------------------------------------------------------------------

# @login_required
# def work_request_list(request):
#     """
#     Manager view: list all WorkRequests with optional status filter.
#     """
#     if not _is_manager(request):
#         return redirect('login')

#     requests_qs = WorkRequest.objects.select_related(
#         'requested_by', 'requested_by__userprofile'
#     ).order_by('-created_at')

#     status_filter   = request.GET.get('status', '').strip()
#     priority_filter = request.GET.get('priority', '').strip()
#     query           = request.GET.get('q', '').strip()

#     if status_filter:
#         requests_qs = requests_qs.filter(status=status_filter)

#     if priority_filter:
#         requests_qs = requests_qs.filter(priority=priority_filter)

#     if query:
#         requests_qs = requests_qs.filter(
#             Q(title__icontains=query) |
#             Q(customer_name__icontains=query) |
#             Q(requested_by__username__icontains=query) |
#             Q(request_no__icontains=query)
#         )

#     # Counts for the summary bar
#     total_count    = WorkRequest.objects.count()
#     pending_count  = WorkRequest.objects.filter(status='pending').count()
#     approved_count = WorkRequest.objects.filter(status='approved').count()
#     rejected_count = WorkRequest.objects.filter(status='rejected').count()

#     return render(request, 'tasks/work_request_list.html', {
#         'work_requests':    requests_qs,
#         'status_filter':    status_filter,
#         'priority_filter':  priority_filter,
#         'query':            query,
#         'status_choices':   WorkRequest.STATUS_CHOICES,
#         'priority_choices': WorkRequest.PRIORITY_CHOICES,
#         'total_count':      total_count,
#         'pending_count':    pending_count,
#         'approved_count':   approved_count,
#         'rejected_count':   rejected_count,
#     })

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def work_request_list(request):
    """
    Manager View
    Displays all work requests with search, filters and pagination.
    """

    if not _is_manager(request):
        return redirect("login")

    requests_qs = (
        WorkRequest.objects
        .select_related(
            "requested_by",
            "requested_by__userprofile"
        )
        .order_by("-created_at")
    )

    # -----------------------------
    # Filters
    # -----------------------------
    status_filter = request.GET.get("status", "").strip()
    priority_filter = request.GET.get("priority", "").strip()
    query = request.GET.get("q", "").strip()

    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)

    if priority_filter:
        requests_qs = requests_qs.filter(priority=priority_filter)

    if query:
        requests_qs = requests_qs.filter(

            Q(request_no__icontains=query) |

            Q(title__icontains=query) |

            Q(customer_name__icontains=query) |

            Q(description__icontains=query) |

            Q(requested_by__username__icontains=query) |

            Q(requested_by__first_name__icontains=query) |

            Q(requested_by__last_name__icontains=query)

        )

    # -----------------------------
    # Pagination
    # -----------------------------
    paginator = Paginator(requests_qs, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    # -----------------------------
    # Dashboard Counts
    # -----------------------------
    total_count = WorkRequest.objects.count()

    pending_count = WorkRequest.objects.filter(
        status="pending"
    ).count()

    review_count = WorkRequest.objects.filter(
        status="under_review"
    ).count()

    approved_count = WorkRequest.objects.filter(
        status="approved"
    ).count()

    quotation_count = WorkRequest.objects.filter(
        status="quotation_created"
    ).count()

    rejected_count = WorkRequest.objects.filter(
        status="rejected"
    ).count()

    return render(
        request,
        "tasks/work_request_list.html",
        {
            "work_requests": page_obj,
            "page_obj": page_obj,

            "status_filter": status_filter,
            "priority_filter": priority_filter,
            "query": query,

            "status_choices": WorkRequest.STATUS_CHOICES,
            "priority_choices": WorkRequest.PRIORITY_CHOICES,

            "total_count": total_count,
            "pending_count": pending_count,
            "review_count": review_count,
            "approved_count": approved_count,
            "quotation_count": quotation_count,
            "rejected_count": rejected_count,
        },
    )

# ------------------------------------------------------------------
# Manager + Submitter: Request Detail
# ------------------------------------------------------------------

@login_required
def work_request_detail(request, request_id):

    print("===== WORK REQUEST DETAIL VIEW =====")
    """
    Detail page for a single WorkRequest.

    - Managers see Approve / Reject / Mark Under Review buttons.
    - Submitters see their own request in read-only mode.
    """
    work_request = get_object_or_404(
        WorkRequest.objects.select_related(
            'requested_by', 'requested_by__userprofile'
        ),
        id=request_id,
    )

    is_mgr = _is_manager(request)
    is_owner = work_request.requested_by == request.user

    if not is_mgr and not is_owner:
        return redirect('login')

    return render(request, 'tasks/work_request_detail.html', {
        'work_request': work_request,
        'is_manager':   is_mgr,
    })


# ------------------------------------------------------------------
# Manager: Approve
# ------------------------------------------------------------------

@login_required
def approve_work_request(request, request_id):
    """Set status → approved and save optional admin notes."""
    if not _is_manager(request):
        return redirect('login')

    work_request = get_object_or_404(WorkRequest, id=request_id)

    if not work_request.can_be_reviewed:
        messages.warning(request, f'Request {work_request.request_no} cannot be approved in its current state.')
        return redirect('work_request_detail', request_id=request_id)

    if request.method == 'POST':
        work_request.admin_notes = request.POST.get('admin_notes', '').strip() or work_request.admin_notes
        work_request.status      = 'approved'
        work_request.save()
        messages.success(request, f'Request {work_request.request_no} approved.')
        return redirect('work_request_detail', request_id=request_id)

    return redirect('work_request_detail', request_id=request_id)


# ------------------------------------------------------------------
# Manager: Reject
# ------------------------------------------------------------------

@login_required
def reject_work_request(request, request_id):
    """Set status → rejected and save mandatory admin notes."""
    if not _is_manager(request):
        return redirect('login')

    work_request = get_object_or_404(WorkRequest, id=request_id)

    if not work_request.can_be_reviewed:
        messages.warning(request, f'Request {work_request.request_no} cannot be rejected in its current state.')
        return redirect('work_request_detail', request_id=request_id)

    if request.method == 'POST':
        admin_notes = request.POST.get('admin_notes', '').strip()
        if not admin_notes:
            messages.error(request, 'Please provide a reason for rejection.')
            return redirect('work_request_detail', request_id=request_id)

        work_request.admin_notes = admin_notes
        work_request.status      = 'rejected'
        work_request.save()
        messages.success(request, f'Request {work_request.request_no} rejected.')
        return redirect('work_request_list')

    return redirect('work_request_detail', request_id=request_id)


# ------------------------------------------------------------------
# Manager: Mark Under Review
# ------------------------------------------------------------------

@login_required
def mark_under_review(request, request_id):
    """Set status → under_review (manager has seen it but not decided yet)."""
    if not _is_manager(request):
        return redirect('login')

    work_request = get_object_or_404(WorkRequest, id=request_id)

    if work_request.status == 'pending':
        work_request.status = 'under_review'
        work_request.save()
        messages.info(request, f'Request {work_request.request_no} marked as Under Review.')

    return redirect('work_request_detail', request_id=request_id)




@login_required
def admin_edit_work_request(request, request_id):
    """
    Manager view: edit any WorkRequest directly from the admin list,
    regardless of submitter or current status.
    """
    if not _is_manager(request):
        return redirect('login')
 
    work_request = get_object_or_404(WorkRequest, id=request_id)
 
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        title         = request.POST.get('title', '').strip()
        description   = request.POST.get('description', '').strip()
        priority      = request.POST.get('priority', 'medium')
        required_date = request.POST.get('required_date') or None
        status        = request.POST.get('status', work_request.status)
 
        errors = []
        if not customer_name:
            errors.append('Customer name is required.')
        if not title:
            errors.append('Title is required.')
        if not description:
            errors.append('Description is required.')
 
        if errors:
            return render(request, 'tasks/work_request_form.html', {
                'errors':           errors,
                'form_data':        request.POST,
                'priority_choices': WorkRequest.PRIORITY_CHOICES,
                'status_choices':   WorkRequest.STATUS_CHOICES,
                'work_request':     work_request,
                'action':           'Edit',
                'is_admin_edit':    True,
            })
 
        work_request.customer_name = customer_name
        work_request.title         = title
        work_request.description   = description
        work_request.priority      = priority
        work_request.required_date = required_date
        work_request.status        = status
        work_request.save()
 
        messages.success(request, f'Request {work_request.request_no} updated.')
        return redirect('work_request_list')
 
    return render(request, 'tasks/work_request_form.html', {
        'priority_choices': WorkRequest.PRIORITY_CHOICES,
        'status_choices':   WorkRequest.STATUS_CHOICES,
        'work_request':     work_request,
        'action':           'Edit',
        'is_admin_edit':    True,
    })
 
 
# ──────────────────────────────────────────────────────────────
# 4. ADD this new view — Delete (manager only)
# ──────────────────────────────────────────────────────────────
 
@login_required
def delete_work_request(request, request_id):
    """
    Manager view: permanently delete a WorkRequest.
    Requires POST for safety (confirmation handled in template).
    """
    if not _is_manager(request):
        return redirect('login')
 
    work_request = get_object_or_404(WorkRequest, id=request_id)
 
    if request.method == 'POST':
        ref = work_request.request_no
        work_request.delete()
        messages.success(request, f'Request {ref} deleted.')
        return redirect('work_request_list')
 
    return redirect('work_request_detail', request_id=request_id)
 
