from django.contrib.auth.models import User
from django.db import models
from admin_panel.models import Package_Details

class BusDetails(models.Model):

    BUS_TYPE_CHOICES = [
        ('AC', 'AC Bus'),
        ('NON-AC', 'Non-AC Bus'),
        ('SLEEPER', 'Sleeper Bus'),
        ('SEMI-SLEEPER', 'Semi Sleeper Bus'),
        ('VOLVO', 'Volvo Bus'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buses", null=True)
    package = models.ForeignKey(Package_Details, on_delete=models.CASCADE, related_name="buses", null=True)

    bus_name = models.CharField(max_length=100, default="KSRTC BUS", editable=False)
    bus_number = models.CharField(max_length=50)
    route_name = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    bus_type = models.CharField(max_length=50, choices=BUS_TYPE_CHOICES)

    def __str__(self):
        return f"{self.bus_name} - {self.bus_number}"


class BusRoute(models.Model):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE, related_name="routes", null=True)
    location = models.CharField(max_length=100)
    arrival_time = models.TimeField()
    departure_time = models.TimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.bus.bus_number} → {self.location}"
