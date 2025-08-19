from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_company, name='create_company'),
    path('leave/', views.leave_company, name='leave_company'),
    path('delete/', views.delete_company, name='delete_company'),
    path('invite/', views.invite_user, name='invite_user'),
    path('accept/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
]
