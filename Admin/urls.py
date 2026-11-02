from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_reg, name='admin_reg'),
    path('admin_log/', admin_log, name='admin_log'),
    path('admin_otp/', admin_otp, name='admin_otp'),
    path('admin_reset/', admin_reset, name='admin_reset'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    path('user_details/', user_details, name='user_details'),
    path('give_fine/<int:image_id>/', give_fine, name='give_fine'),
    path('view_fine_details/', view_fine_details, name='view_fine_details'),
    path('view_predictions/', view_predictions, name='view_predictions'),
    path('view_violation_images/', view_violation_images, name='view_violation_images'),
]
