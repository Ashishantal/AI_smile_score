from django.urls import path
from .views import wallet_page, create_wallet
from . import views


urlpatterns = [
    path('', wallet_page, name='wallet'),
     path("create/", views.create_wallet, name="create_wallet"),
]
