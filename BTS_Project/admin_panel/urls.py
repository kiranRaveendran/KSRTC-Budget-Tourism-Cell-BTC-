from django.urls import path
from .views import PackageAPI, DayWiseItineraryAPI,DepotSignup,Navbar,DepotManagerList

app_name='admin_site'
urlpatterns = [
    path('packages/', PackageAPI.as_view()),          # GET all / POST
    path('packages/<int:pk>/', PackageAPI.as_view()), # GET one / PUT / DELETE

    path('itineraries/', DayWiseItineraryAPI.as_view()),          
    path('itineraries/<int:pk>/', DayWiseItineraryAPI.as_view()),

    path('depotsignup/', DepotSignup.as_view(), name='depotsignup'),
    path('navbar/', Navbar.as_view(), name='navbar'),
    path('managerlist/', DepotManagerList.as_view(), name='managerlist'),

    
    
]

