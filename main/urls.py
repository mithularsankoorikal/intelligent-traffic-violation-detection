from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('process_video/', process_video, name='process_video')
]
