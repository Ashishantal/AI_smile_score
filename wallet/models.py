from django.db import models
from django.conf import settings


class RewardTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    wallet_address = models.CharField(max_length=255)
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.score} - Paid: {self.is_paid}"

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=42)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    def __str__(self):
        return f"{self.user} - {self.balance} ETH"