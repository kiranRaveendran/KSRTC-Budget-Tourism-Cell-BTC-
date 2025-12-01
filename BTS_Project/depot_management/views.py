from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import BusDetailsSerializer, BusRouteSerializer
from .models import BusDetails, BusRoute


# ---------------------- LOGIN API ----------------------

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        depot_name = request.data.get('depot_name')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # if depot profile doesn't exist → handle safely
        if not hasattr(user, 'depotprofile'):
            return Response({'error': 'Depot profile not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check depot name
        if user.depotprofile.depot_name != depot_name:
            return Response({'error': 'Depot name mismatch'},
                            status=status.HTTP_403_FORBIDDEN)

        # JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
            'role': user.depotprofile.role,
            'depot_name': user.depotprofile.depot_name
        }, status=status.HTTP_200_OK)


class BusAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        if pk:
            try:
                bus = BusDetails.objects.get(id=pk)
            except BusDetails.DoesNotExist:
                return Response({"error": "Bus not found"}, status=404)
            serializer = BusDetailsSerializer(bus)
            return Response(serializer.data)

        buses = BusDetails.objects.all()
        serializer = BusDetailsSerializer(buses, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = BusDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def put(self, request, pk):
        try:
            bus = BusDetails.objects.get(id=pk)
        except BusDetails.DoesNotExist:
            return Response({"error": "Bus not found"}, status=404)

        serializer = BusDetailsSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        try:
            bus = BusDetails.objects.get(id=pk)
        except BusDetails.DoesNotExist:
            return Response({"error": "Bus not found"}, status=404)

        bus.delete()
        return Response({"message": "Deleted successfully"}, status=204)

class RouteAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        if pk:
            try:
                route = BusRoute.objects.get(id=pk)
            except BusRoute.DoesNotExist:
                return Response({"error": "Route not found"}, status=404)

            serializer = BusRouteSerializer(route)
            return Response(serializer.data)

        routes = BusRoute.objects.all()
        serializer = BusRouteSerializer(routes, many=True)
        return Response(serializer.data)


    def post(self, request):
        # Validate bus exists
        bus_id = request.data.get("bus")
        if not BusDetails.objects.filter(id=bus_id).exists():
            return Response({"error": "Invalid bus ID"}, status=400)

        serializer = BusRouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def put(self, request, pk):
        try:
            route = BusRoute.objects.get(id=pk)
        except BusRoute.DoesNotExist:
            return Response({"error": "Route not found"}, status=404)

        serializer = BusRouteSerializer(route, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        try:
            route = BusRoute.objects.get(id=pk)
        except BusRoute.DoesNotExist:
            return Response({"error": "Route not found"}, status=404)

        route.delete()
        return Response({"message": "Deleted successfully"}, status=204)
