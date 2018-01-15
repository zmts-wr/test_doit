from django.urls import path
from django.contrib.auth import views as auth_views

from polls import views

urlpatterns = [
    path('login', views.login_signup, name='login'),
    path('signup', views.login_signup, { 'signup': True, }, name='signup'),
    path('gr/<int:qg_id>/result/', views.result, name='result'),
    path('gr/<int:qg_id>/', views.qgroup, name='question_group'),
    path('', views.home, name='home'),
]
