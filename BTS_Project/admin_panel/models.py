from django.db import models
from django.contrib.auth.models import User


class DepotProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    depot_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, default='Depot Manager', editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.depot_name} ({self.role})"


class Package_Details(models.Model):
    package_name = models.CharField(max_length=200)
    package_overview = models.TextField()
    duration = models.CharField(max_length=100)
    places = models.JSONField(default=list)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.PositiveIntegerField()

    
    image1 = models.ImageField(upload_to='tourist_places/', null=True, blank=True)
    image2 = models.ImageField(upload_to='tourist_places/', null=True, blank=True)
    image3 = models.ImageField(upload_to='tourist_places/', null=True, blank=True)
    image4 = models.ImageField(upload_to='tourist_places/', null=True, blank=True)

    assigned_depot_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_packages"
    )

    def __str__(self):
        return self.package_name


class DayWiseItinerary(models.Model):
    package = models.ForeignKey(
        Package_Details,
        related_name='itineraries',
        null=True,
        on_delete=models.CASCADE
    )
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.package.package_name} - Day {self.day_number}: {self.title}"
