
from django.contrib import admin
from django.urls import path
from .views import registrationView, loginAPIView, UserProfile

urlpatterns = [
    path('register/', registrationView.as_view(), name='register'),
    path('login/', loginAPIView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile')
]