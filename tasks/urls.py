from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('create-task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('create-freelancer/', views.create_freelancer, name='create_freelancer'),
    path('employees/', views.employee_list, name='employee_list'),



    path('signup/freelancer/', views.signup_view, {'role': 'freelancer'}, name='signup_freelancer'),
    path('signup/employee/', views.signup_view, {'role': 'employee'}, name='signup_employee'),

    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    # path('freelancer/<int:user_id>/', views.freelancer_detail, name='freelancer_detail'),
    path('freelancer-data/<int:user_id>/', views.freelancer_detail, name='freelancer_data'),
    
    path('edit-freelancer/<int:user_id>/', views.edit_freelancer, name='edit_freelancer'),
    path('delete-freelancer/<int:user_id>/', views.delete_freelancer, name='delete_freelancer'),
    path('freelancer-tasks/<int:user_id>/', views.freelancer_tasks, name='freelancer_tasks'),
    path('search-tasks/', views.search_tasks, name='search_tasks'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path(
    'edit-employee/<int:user_id>/',
    views.edit_employee,
    name='edit_employee'
),

path(
    'delete-employee/<int:user_id>/',
    views.delete_employee,
    name='delete_employee'
),


# ==============================================================
# WORK REQUEST URLs — Phase 1
# Append these path() entries to the urlpatterns list in tasks/urls.py
# ==============================================================

    # ── Employee / Freelancer ──────────────────────────────────
    path('requests/',                  views.my_requests,           name='my_requests'),
    path('requests/new/',              views.create_work_request,   name='create_work_request'),
    path('requests/<int:request_id>/edit/', views.edit_work_request, name='edit_work_request'),

    # ── Manager ───────────────────────────────────────────────
    path('work-requests/',                         views.work_request_list,   name='work_request_list'),
    path('work-requests/<int:request_id>/',        views.work_request_detail, name='work_request_detail'),
    path('work-requests/<int:request_id>/approve/', views.approve_work_request, name='approve_work_request'),
    path('work-requests/<int:request_id>/reject/',  views.reject_work_request,  name='reject_work_request'),
    path('work-requests/<int:request_id>/review/',  views.mark_under_review,    name='mark_under_review'),
        path('work-requests/<int:request_id>/edit/',    views.admin_edit_work_request,  name='admin_edit_work_request'),
    path('work-requests/<int:request_id>/delete/',  views.delete_work_request,      name='delete_work_request'),

 path('employee-data/<int:user_id>/', views.employee_detail, name='employee_data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
