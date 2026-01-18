from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/<int:image_id>/', views.upload_to_leaderboard, name='upload_leaderboard'),
]