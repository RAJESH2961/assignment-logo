from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_form, name='show_form'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]
