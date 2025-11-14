from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Register, name="reg"),
    path('login/', views.login, name='login'),
    path("Index.html", views.Index, name="index"),
    path("Service.html", views.Service, name="ser"),
    path("service-details.html", views.Service_details, name="ser-details"),
    path("Blog.html", views.Blog, name="blog"),
    path("blog-details.html", views.Blog_details, name="blog-details"),
    path("Contact.html", views.Contact, name="con"),
    path('logout', views.logout_view, name='logout')
]