from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .models import Package_Details, DayWiseItinerary,User
from .serializers import (
    PackageSerializer,
    DayWiseItinerarySerializer,
    DepotSignupSerializer,
)

# --------------------------- SIGNUP API ---------------------------
class DepotSignup(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "depotsignup.html"

    def post(self, request):
        serializer = DepotSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User and DepotProfile created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def get(self, request, pk=None):

        if request.accepted_renderer.format == 'html':
            return Response({"package_id": pk})


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




class Navbar(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "navbar.html"

    
    def get(self, request, pk=None):

        if request.accepted_renderer.format == 'html':
            return Response({})
        
        
        
class DepotManagerList(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "depotmanagers.html"

    def get(self, request):

        managers = User.objects.filter(
            depotprofile__role="Depot Manager"
        ).select_related("depotprofile")

        data = [
            {
                "id": manager.id,
                "username": manager.username,
                "email": manager.email,
                "depot_name": manager.depotprofile.depot_name,
                "role": manager.depotprofile.role,
                "date_joined": manager.date_joined,
            }
            for manager in managers
        ]

        if request.accepted_renderer.format == "html":
            return Response({"managers": data})

        return Response(data, status=status.HTTP_200_OK)

