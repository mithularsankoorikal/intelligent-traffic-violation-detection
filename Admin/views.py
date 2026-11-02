from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from datetime import datetime, timedelta
from user.models import *
from .models import *
from main.models import *
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login
# Create your views here.


def admin_reg(request):
    # Allow only ONE super admin
    if User.objects.filter(is_superuser=True).exists():
        messages.warning(request, "Admin already exists. Please login.")
        return redirect(admin_log)

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("con_password")

        if password != re_password:
            messages.warning(request, "Password mismatch")
            return redirect(admin_reg)

        if User.objects.filter(username=email).exists():
            messages.warning(request, "Email already exists")
            return redirect(admin_reg)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True
        )
        user.save()

        messages.success(request, "Admin registered successfully")
        return redirect(admin_log)

    return render(request, "admin_reg.html")




def admin_log(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect(admin_dashboard)
            else:
                messages.warning(request, "You are not an admin")
        else:
            messages.warning(request, "Invalid credentials")

    return render(request, "admin_log.html")



def admin_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(username=email).exists():
            def generate_otp():
                return random.randint(1000, 9999)
            otp = generate_otp()
            send_mail("OTP for Password Reset", f"Your OTP for forgot password verification is {otp}",
                      settings.EMAIL_HOST_USER, [email])
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['time'] = str(datetime.now())
            return redirect(admin_reset)
        else:
            messages.warning(request, "Account not Found")
    return render(request, "admin_otp.html")


def admin_reset(request):
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
        re_password = request.POST.get("re_password")
        if new_password == re_password:
            if otp == otp1 and duration <= timedelta(minutes=5):
                user = User.objects.get(username=email)
                user.set_password(new_password)
                user.save()
                return redirect(admin_log)
            elif otp == otp1 and duration > timedelta(minutes=5):
                messages.warning(request, "Time exceeded !!")
                return redirect(admin_otp)
            else:
                messages.warning(request, "Invalid otp")
        else:
            messages.warning(request, "Password Mismatch")
    return render(request, "admin_reset.html")


def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


def admin_logout(request):
    logout(request)
    return redirect(reverse('home'))


def user_details(request):
    users = UserData.objects.all()
    return render(request, "user_details.html", {'users': users})


def give_fine(request, image_id=None):
    users = UserData.objects.all()  # Fetch registered vehicle owners
    selected_image = None
    print("Users:", users)
    for user in users:  # Iterate through QuerySet
        print("Vehicle No:", user.vehicle_no, "| Name:", user.name)  # Print each user's details
    if image_id:
        violation = ViolationImage.objects.get(id=image_id)
        selected_image = violation.image_path

    if request.method == "POST":
        vehicle_no = request.POST.get("vehicle_no")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        fine_amount = request.POST.get("fine_amount")
        image_path = request.POST.get("image_path")  # Get the violation image

        if not vehicle_no or not fine_amount:
            messages.error(request, "All fields are required!")
            return redirect("give_fine")

        # Save fine details along with the image path
        Fine.objects.create(
            user_name=user_name,
            email=email,
            vehicle_no=vehicle_no,
            fine_amount=fine_amount,
            image_path=image_path  # Save violation image path
        )

        # Send fine notification via email
        subject = "Fine Notification"
        message = f"Dear {user_name},\n\nYou have been fined an amount of ₹{fine_amount} for your vehicle {vehicle_no}.\n\nPlease pay the fine at the earliest.\n\nCheck the dashboard for more details.\n\nThank you."
        email_msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])

        # Attach the violation image

        if image_path:
            image_path = default_storage.path(image_path)
            with open(image_path, 'rb') as img:
                email_msg.attach(image_path.split('/')[-1], img.read(), 'image/jpeg')

        email_msg.send()  # Send email
        messages.success(request, "Fine issued successfully and email notification sent!")
        return redirect("view_violation_images")

    return render(request, "give_fine.html", {"users": users, "selected_image": selected_image, "MEDIA_URL": settings.MEDIA_URL})


def view_fine_details(request):
    fines = Fine.objects.all()
    return render(request, 'view_fine_details.html', {'fines': fines})


def view_predictions(request):
    videos = ProcessedVideo.objects.all().order_by("-uploaded_at")  # Show latest videos first
    return render(request, 'view_predictions.html', {"videos": videos})


def view_violation_images(request):
    violations = ViolationImage.objects.all().order_by("-timestamp")
    print(violations)
    return render(request, 'view_violation_images.html', {"violations": violations, "MEDIA_URL": settings.MEDIA_URL})
