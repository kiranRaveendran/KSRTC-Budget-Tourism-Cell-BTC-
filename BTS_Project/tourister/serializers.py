from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile,RateReview,Package_Booking
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
