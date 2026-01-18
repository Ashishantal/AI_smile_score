from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.enter_email, name='enter_email'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
]