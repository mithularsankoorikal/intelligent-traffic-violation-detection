from django.db import models

# Create your models here.


class UserData(models.Model):
    name = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.vehicle_no} - {self.name}"
