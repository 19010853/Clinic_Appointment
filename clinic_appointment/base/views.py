from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import requests
import stripe

from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }
    return render(request, "base/index.html", context)

def services(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }
    return render(request, "base/services.html", context)

def about(request):
    return render(request, "base/about.html")

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    context = {
        "service": service
    }
    return render(request, "base/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.date_of_birth = date_of_birth
        patient.save()

        # Create appointment object
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )

        # Create a billing objects
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()

        return redirect("base:checkout", billing.billing_id)

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "base/book_appointment.html", context)

@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    context = {
        "billing": billing,
    }
    return render(request, "base/checkout.html", context)

@login_required
def mark_as_paid(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    if billing.status == "Unpaid":
        billing.status = "Paid"
        billing.save()
        billing.appointment.status = "Completed"
        billing.appointment.save()

        doctor_models.Notification.objects.create(
            doctor=billing.appointment.doctor,
            appointment=billing.appointment,
            type="New Appointment"
        )

        patient_models.Notification.objects.create(
            patient=billing.appointment.patient,
            appointment=billing.appointment,
            type="Appointment Scheduled"
        )

        merge_data = {"billing": billing}
        try:
            # Email cho doctor
            subject = "New Appointment"
            text_body = render_to_string("email/new_appointment.txt", merge_data)
            html_body = render_to_string("email/new_appointment.html", merge_data)
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[billing.appointment.doctor.user.email],
                body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            print(f"Doctor email sent successfully to {billing.appointment.doctor.user.email}")

            # Email cho patient
            subject = "Appointment Booked Successfully"
            text_body = render_to_string("email/appointment_booked.txt", merge_data)
            html_body = render_to_string("email/appointment_booked.html", merge_data)
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[billing.appointment.patient.email],
                body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            print(f"Patient email sent successfully to {billing.appointment.patient.email}")
        except Exception as e:
            print("Email sending failed!")
            print("Error details:", str(e))
            print("From email:", settings.FROM_EMAIL)
            print("Doctor email:", billing.appointment.doctor.user.email)
            print("Patient email:", billing.appointment.patient.email)
            print("Email backend:", settings.EMAIL_BACKEND)
            print("Brevo API Key configured:", bool(settings.ANYMAIL.get("SENDINBLUE_API_KEY")))

    return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")

@login_required
def payment_status(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status,
    }
    return render(request, "base/payment_status.html", context)
