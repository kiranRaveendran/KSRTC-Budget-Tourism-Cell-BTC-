from django.urls import path
from .views import Signup,Login,Package_details,RateReviewAPI,Index,Navbar,Footer,Payment,Payment_Success,front_end_signup,front_end_login,Package_list,My_Booking

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('package_details/', Package_details.as_view(), name='Package_details'),
    path('reviews/', RateReviewAPI.as_view(), name='reviews'),
    path('index/', Index.as_view(), name='index'),
    path('navbar/', Navbar.as_view(), name='navbar'),
    path('footer/', Footer.as_view(), name='footer'),
    path('payment/', Payment.as_view(), name='payment'),
    path('payment_success/', Payment_Success.as_view(), name='payment_sucess'),
    path('frontend_signup/', front_end_signup.as_view(), name='frontend_signup'),
    path('frontend_login/', front_end_login.as_view(), name='frontend_login'),
    path('package_list/', Package_list.as_view(), name='frontend_login'),
    path('my_booking/', My_Booking.as_view(), name='my_booking'),
]
