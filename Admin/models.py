from django.db import models

# Create your models here.


class Fine(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    vehicle_no = models.CharField(max_length=50)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=255, null=True, blank=True)  # Store violation image path
    date_issued = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.user_name} - {self.vehicle_no} - ₹{self.fine_amount}"


