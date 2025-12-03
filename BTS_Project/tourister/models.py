from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Package_Details
from depot_management.models import BusDetails

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    role = models.CharField(max_length=20, default="Tourister")

class RateReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


class Package_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package_Details, on_delete=models.CASCADE)
    bus = models.ForeignKey(BusDetails, on_delete=models.SET_NULL, null=True, blank=True)

    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    boarding_point = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    total_price = models.PositiveIntegerField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"

