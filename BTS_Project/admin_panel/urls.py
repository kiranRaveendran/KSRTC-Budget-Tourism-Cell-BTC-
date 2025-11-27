from django.urls import path
from .views import PackageAPI, DayWiseItineraryAPI,Signup

urlpatterns = [
    path('packages/', PackageAPI.as_view()),          # GET all / POST
    path('packages/<int:pk>/', PackageAPI.as_view()), # GET one / PUT / DELETE

    path('itineraries/', DayWiseItineraryAPI.as_view()),          
    path('itineraries/<int:pk>/', DayWiseItineraryAPI.as_view()),

    path('signup/', Signup.as_view(), name='signup'),

    
    
]

