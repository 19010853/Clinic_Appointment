from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('book_appointment/<int:service_id>/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('checkout/<str:billing_id>/', views.checkout, name='checkout'),
    path('mark_as_paid/<str:billing_id>/', views.mark_as_paid, name='mark_as_paid'),
    path('payment_status/<str:billing_id>/', views.payment_status, name='payment_status'),
]