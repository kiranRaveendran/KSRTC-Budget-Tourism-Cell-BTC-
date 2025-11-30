from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Package_Details, DayWiseItinerary, DepotProfile
from .serializers import (
    PackageSerializer,
    DayWiseItinerarySerializer,
    DepotSignupSerializer,
    DepotProfileSerializer
)

# --------------------------- SIGNUP API ---------------------------
class Signup(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DepotSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User and DepotProfile created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profiles = DepotProfile.objects.all()
        serializer = DepotProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------- PACKAGE API ---------------------------
class PackageAPI(APIView):
    permission_classes = [permissions.AllowAny]

    
    def get(self, request, pk=None):
        if pk:
            try:
                package = Package_Details.objects.get(id=pk)
            except Package_Details.DoesNotExist:
                return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PackageSerializer(package)
            return Response(serializer.data)

        # Filters
        destination = request.GET.get('destination', '')
        date = request.GET.get('date', '')
        price = request.GET.get('price', '')

        packages = Package_Details.objects.all()

        if destination:
            packages = packages.filter(places__icontains=destination)

        if date:
            packages = packages.filter(start_date__lte=date, end_date__gte=date)

        if price:
            try:
                price = int(price)
                if price > 50000:
                    packages = packages.filter(price__gt=50000)
                else:
                    packages = packages.filter(price__lte=price)
            except ValueError:
                pass  

        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            package = Package_Details.objects.get(id=pk)
        except Package_Details.DoesNotExist:
            return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageSerializer(package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            package = Package_Details.objects.get(id=pk)
            package.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Package_Details.DoesNotExist:
            return Response({"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND)


# --------------------------- DAY WISE ITINERARY API ---------------------------
class DayWiseItineraryAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        if pk:
            try:
                itinerary = DayWiseItinerary.objects.get(id=pk)
            except DayWiseItinerary.DoesNotExist:
                return Response({"message": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = DayWiseItinerarySerializer(itinerary)
            return Response(serializer.data)

        itineraries = DayWiseItinerary.objects.all()
        serializer = DayWiseItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DayWiseItinerarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            itinerary = DayWiseItinerary.objects.get(id=pk)
        except DayWiseItinerary.DoesNotExist:
            return Response({"message": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DayWiseItinerarySerializer(itinerary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            itinerary = DayWiseItinerary.objects.get(id=pk)
            itinerary.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except DayWiseItinerary.DoesNotExist:
            return Response({"message": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)
