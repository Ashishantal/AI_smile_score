from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from web3 import Web3
from django.conf import settings
from .models import Wallet, RewardTransaction
from decimal import Decimal
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))


@login_required
def wallet_page(request):
    user = request.user
    wallet = Wallet.objects.filter(user=user).first()

    # Wallet NOT created yet
    if not wallet:
        return render(request, "wallet/wallet.html", {
            "wallet": None
        })

    w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))

    balance_wei = w3.eth.get_balance(wallet.address)
    balance_eth = Decimal(w3.from_wei(balance_wei, 'ether'))

    wallet.balance = balance_eth
    wallet.save(update_fields=["balance"])

    transactions = RewardTransaction.objects.filter(user=user).order_by("-created_at")

    return render(request, "wallet/wallet.html", {
        "wallet": wallet,
        "transactions": transactions,
        "balance": balance_eth
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

