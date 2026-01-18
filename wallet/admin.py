from django.contrib import admin
from .models import Wallet, RewardTransaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "balance")

@admin.register(RewardTransaction)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "tx_hash", "created_at")
