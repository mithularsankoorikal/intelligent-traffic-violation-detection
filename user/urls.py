from django.urls import path
from .views import *

urlpatterns = [
    path('', user_reg, name='user_reg'),
    path('user_log/', user_log, name='user_log'),
    path('user_otp/', user_otp, name='user_otp'),
    path('user_reset/', user_reset, name='user_reset'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('user_logout/', user_logout, name='user_logout'),

    path('user_fine_details/', user_fine_details, name='user_fine_details'),
    path('pending_bills/', pending_bills, name='pending_bills'),
    path('pay_fine/<int:fine_id>/', pay_fine, name='pay_fine'),
    path("download_receipt/<int:fine_id>/", generate_receipt, name="download_receipt"),
]
