from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from Admin.models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.timezone import localtime

# Create your views here.


def user_reg(request):
    if request.method == "POST":
        name = request.POST.get("name")
        vehicle_no = request.POST.get("vehicle_no")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        print(name, vehicle_no, email, mobile, password, re_password)
        if password == re_password:
            if UserData.objects.filter(email=email).exists():
                messages.warning(request, "Email exist")
            else:
                password = make_password(password)
                print(password)
                user = UserData.objects.create(name=name, vehicle_no=vehicle_no,
                                               email=email, mobile=mobile, password=password)
                user.save()
                print("Data Inserted")
                return redirect(user_log)
        else:
            messages.warning(request, "Password mismatch")

    return render(request, "user_reg.html")


def user_log(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        user = UserData.objects.filter(email=email).first()
        print(user)
        if user and check_password(password, user.password):
            # Log in using Django's auth system
            user, created = User.objects.get_or_create(
                username=email,
                defaults={"password": make_password(password)}
            )
            print(user)
            login(request, user)
            print("logged successfully")
            return redirect(user_dashboard)
        else:
            messages.warning(request, "Account not found")
    return render(request, "user_log.html")


def user_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if UserData.objects.filter(email=email).exists():
            def generate_otp():
                return random.randint(100, 999)

            otp = generate_otp()
            send_mail("OTP for Password Reset", f"Your OTP for forgot password verification is {otp}",
                      settings.EMAIL_HOST_USER, [email])
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['time'] = str(datetime.now())
            return redirect(user_reset)
        else:
            messages.warning(request, "Account not Found")
    return render(request, "user_otp.html")


def user_reset(request):
    otp = request.session.get('otp')
    print(otp)
    email = request.session.get('email')
    send_time = request.session.get('time')
    send_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    duration = current_time - send_time
    print(duration)
    if request.method == "POST":
        otp1 = int(request.POST.get("otp"))
        # print(type(otp1))
        new_password = request.POST.get("password")
        re_new_password = request.POST.get("re_password")
        print(new_password, re_new_password)
        if new_password == re_new_password:
            if otp == otp1 and duration <= timedelta(minutes=5):
                user= UserData.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return redirect(user_log)
            elif otp == otp1 and duration > timedelta(minutes=5):
                messages.warning(request, "Time exceeded !!")
            else:
                messages.warning(request, "Invalid otp")
        else:
            messages.warning(request, "Password Mismatch")
    return render(request, "user_reset.html")


def user_dashboard(request):
    return render(request, "user_dashboard.html")


def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


@login_required
def user_fine_details(request):
    user_email = request.user.username
    user_fines = Fine.objects.filter(email=user_email)
    return render(request, 'fine_details.html', {'user_fines': user_fines})


@login_required
def pending_bills(request):
    user_email = request.user.username
    pending_fines = Fine.objects.filter(email=user_email, status='Pending')
    return render(request, 'bills.html', {'pending_fines': pending_fines, "MEDIA_URL": settings.MEDIA_URL})


@login_required
def pay_fine(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    print(fine)
    print("Before Update:", fine.status)

    if request.method == "POST" and fine.status == "Pending":
        print("Received POST Request")
        fine.status = "Paid"
        fine.save()
        print("Updated Fine Status:", fine.status)
    # messages.success(request, "Payment completed successfully!")
    return redirect("pending_bills")



def generate_receipt(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    local_time = localtime(fine.date_issued)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{fine.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # ===== HEADER =====
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 50, "Traffic Monitoring Department")

    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 80, "PAYMENT RECEIPT")

    # top line
    p.line(40, height - 95, width - 40, height - 95)

    # ===== RECEIPT INFO =====
    p.setFont("Helvetica", 12)
    y = height - 130

    p.drawString(60, y, f"Receipt No : {fine.id}")
    y -= 25
    p.drawString(60, y, f"Date : {local_time.strftime('%Y-%m-%d')}")
    y -= 25
    p.drawString(60, y, f"Time : {local_time.strftime('%H:%M:%S')}")

    # middle line
    p.line(40, y - 10, width - 40, y - 10)

    # ===== USER DETAILS =====
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(60, y, "User Details")
    y -= 25

    p.setFont("Helvetica", 12)
    p.drawString(60, y, f"Name : {fine.user_name}")
    y -= 25
    p.drawString(60, y, f"Vehicle Number : {fine.vehicle_no}")
    y -= 25
    p.drawString(60, y, f"Fine Amount : ₹{fine.fine_amount}")
    y -= 25
    p.drawString(60, y, "Payment Status : PAID")

    # ===== FOOTER =====
    y -= 40
    p.line(40, y, width - 40, y)

    y -= 40
    p.drawRightString(width - 60, y, "Authorized Signature")

    # bottom thank you
    y -= 40
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, y, "Thank you for your payment. Drive safely!")

    p.showPage()
    p.save()
    return response

