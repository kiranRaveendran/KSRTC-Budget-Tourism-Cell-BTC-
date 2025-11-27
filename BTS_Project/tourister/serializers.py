from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile,RateReview,Booking
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
    package = PackageSerializer(read_only=True)  
    bus = BusDetailsSerializer(read_only=True)           
    user =SignupSerializer(read_only=True)         

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_price', 'booking_date']

    def validate(self, data):
        bus = data.get("bus")
        adults = data.get("adults")
        children = data.get("children")

        total_passengers = adults + children

       
        if bus:
            if bus.total_seats < total_passengers:
                raise serializers.ValidationError(
                    {"error": "Not enough available seats for this bus!"}
                )

        return data

    def create(self, validated_data):
        bus = validated_data.get("bus")
        package = validated_data.get("package")

        adults = validated_data.get("adults")
        children = validated_data.get("children")

        total_passengers = adults + children

        # ------- PRICE CALCULATION -------
        total_price = package.price* total_passengers
        validated_data["total_price"] = total_price

        # ------- REDUCE SEATS -------
        if bus:
            bus.total_seats -= total_passengers
            bus.save()

        return super().create(validated_data)
    




class RateReviewSerializer(serializers.ModelSerializer):
    user = SignupSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)  # Client sends user ID

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
