import uuid
from decimal import Decimal
from .models import Wallet, RewardTransaction

def reward_user_for_score(user, score):
    if score < 80:
        return False, "Score too low"

    wallet, created = Wallet.objects.get_or_create(
        user=user,
        defaults={
            "address": f"0xDEMO{uuid.uuid4().hex[:36]}",
            "balance": Decimal("0.00")
        }
    )

    already_paid = RewardTransaction.objects.filter(
        user=user,
        is_paid=True
    ).exists()

    if already_paid:
        return False, "Reward already claimed"

    RewardTransaction.objects.create(
        user=user,
        score=score,
        wallet_address=wallet.address,
        is_paid=True
    )

    wallet.balance += Decimal("0.01")
    wallet.save()

    return True, "🎉 Reward credited to demo wallet"
