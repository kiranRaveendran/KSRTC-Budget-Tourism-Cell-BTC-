from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile,RateReview,Booking,Package_Details,BusDetails
from admin_panel.serializers import PackageSerializer
from depot_management.serializers import BusDetailsSerializer

class SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number")

        # Use Django's built-in create_user
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        # Create profile
        Profile.objects.create(user=user, phone_number=phone_number)

        return user


class BookingSerializer(serializers.ModelSerializer):
    user = SignupSerializer(read_only=True)
    package = PackageSerializer(read_only=True)
    bus = BusDetailsSerializer(read_only=True)

    user_id = serializers.IntegerField(write_only=True)
    package_id = serializers.IntegerField(write_only=True)
    bus_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'package', 'bus',
            'adults', 'children', 'boarding_point',
            'phone_number', 'total_price', 'booking_date',
            'user_id', 'package_id', 'bus_id',
        ]
        read_only_fields = ['total_price', 'booking_date']

    def validate(self, data):
        adults = data.get("adults")
        children = data.get("children")
        total_passengers = adults + children

        # Validate bus seats only on POST
        bus_id = data.get("bus_id")
        if bus_id:
            try:
                bus = BusDetails.objects.get(id=bus_id)
            except BusDetails.DoesNotExist:
                raise serializers.ValidationError({"bus_id": "Bus does not exist."})

            if bus.total_seats < total_passengers:
                raise serializers.ValidationError(
                    {"error": "Not enough available seats for this bus!"}
                )

        return data

    def create(self, validated_data):
        # Extract IDs
        user_id = validated_data.pop("user_id")
        package_id = validated_data.pop("package_id")
        bus_id = validated_data.pop("bus_id")

        # Fetch objects
        try:
            user = User.objects.get(id=user_id)
            package = Package_Details.objects.get(id=package_id)
            bus = BusDetails.objects.get(id=bus_id)
        except Exception:
            raise serializers.ValidationError({"error": "Invalid user/package/bus ID"})

        adults = validated_data.get("adults", 0)
        children = validated_data.get("children", 0)
        total_passengers = adults + children

        # Calculate price with 50% discount for children
        total_price = (adults * package.price) + (children * package.price * 0.5)

        validated_data["total_price"] = total_price

        # Reduce seats
        bus.total_seats -= total_passengers
        bus.save()

        # Create booking
        booking = Booking.objects.create(
            user=user,
            package=package,
            bus=bus,
            **validated_data
        )

        return booking

    

class RateReviewSerializer(serializers.ModelSerializer):
    user = SignupSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True) 

    class Meta:
        model = RateReview
        fields = ['user', 'rating', 'review', 'user_id']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User does not exist."})
        review = RateReview.objects.create(user=user, **validated_data)
        return review
