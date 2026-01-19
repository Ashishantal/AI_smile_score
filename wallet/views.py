from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from web3 import Web3
from django.conf import settings
from .models import Wallet, RewardTransaction
from decimal import Decimal
from web3 import Web3
DEMO_REWARD_ETH = Decimal("0.01")



@login_required
def wallet_page(request):
    wallet = Wallet.objects.filter(user=request.user).first()

    if not wallet:
        return render(request, "wallet/wallet.html", {
            "wallet": None
        })

    transactions = RewardTransaction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_earned = transactions.count() * DEMO_REWARD_ETH

    return render(request, "wallet/wallet.html", {
        "wallet": wallet,
        "transactions": transactions,
        "balance": wallet.balance or Decimal("0"),
        "total_earned": total_earned
    })



@login_required
def create_wallet(request):
    if Wallet.objects.filter(user=request.user).exists():
        return redirect("wallet")

    w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
    account = w3.eth.account.create()

    Wallet.objects.create(
        user=request.user,
        address=account.address
    )

    return redirect("wallet")

