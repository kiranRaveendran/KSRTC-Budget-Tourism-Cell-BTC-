from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Package_Details, DayWiseItinerary, DepotProfile
from depot_management.serializers import BusDetailsSerializer


# --------------------------- SIGNUP SERIALIZER (POST) ---------------------------
class DepotSignupSerializer(serializers.ModelSerializer):
    depot_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'depot_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        depot_name = validated_data.pop('depot_name')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )

        DepotProfile.objects.create(
            user=user,
            depot_name=depot_name
        )

        return user


# --------------------------- DEPOT PROFILE SERIALIZER (GET) ---------------------------
class DepotProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = DepotProfile
        fields = ['username', 'email', 'depot_name']


# --------------------------- ITINERARY & PACKAGE SERIALIZERS ---------------------------
class DayWiseItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayWiseItinerary
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    itineraries = DayWiseItinerarySerializer(many=True, read_only=True)
    buses = BusDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Package_Details
        fields = '__all__'
