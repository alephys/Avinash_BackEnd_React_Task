# myproject/urls.py
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='root'),  # Root URL for GET (login page)
    path('login/', views.login_view, name='login'),  # For POST from login.js
    path('submit/', views.submit_request, name='submit'),
    path('home/', views.home, name='home'),
    path('home/<str:topic_name>/', views.topic_detail, name='topic_detail'),
    path('create_topic/', views.create_topic, name='create_topic'),
]