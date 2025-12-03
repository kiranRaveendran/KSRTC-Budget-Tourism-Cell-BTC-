from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import HotelProfile

class HotelSignupSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(write_only=True, required=True)
    city = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'hotel_name', 'city']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        hotel_name = validated_data.pop('hotel_name')
        city = validated_data.pop('city')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )

        HotelProfile.objects.create(
            user=user,
            hotel_name=hotel_name,
            city=city
        )

        return user
