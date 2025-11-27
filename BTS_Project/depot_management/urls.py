from django.urls import path
from .views import Login,BusAPI,RouteAPI

urlpatterns = [
    
    path('login/', Login.as_view(), name='login'),
    path('bus/', BusAPI.as_view()),          
    path('bus/<int:pk>/', BusAPI.as_view()),  
    path('route/', RouteAPI.as_view()),           
    path('route/<int:pk>/', RouteAPI.as_view()),
]
