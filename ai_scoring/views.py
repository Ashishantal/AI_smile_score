from django.shortcuts import render, redirect, get_object_or_404
from .models import ScoredImage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
import base64, random
from wallet.models import RewardTransaction, Wallet
from django.contrib import messages
from ai_scoring.model.model import predict_score
from wallet.blockchain import send_fake_eth


def home(request):
    # USER IMAGES (non-leaderboard)
    images = ScoredImage.objects.filter(
        user=request.user if request.user.is_authenticated else None,
        is_leaderboard=False
    )

    # LEADERBOARD
    leaderboard = ScoredImage.objects.filter(
        is_leaderboard=True
    ).order_by('-score')[:10]

    # CHECK IF USER ALREADY ON LEADERBOARD
    has_leaderboard = False
    if request.user.is_authenticated:
        has_leaderboard = ScoredImage.objects.filter(
            user=request.user,
            is_leaderboard=True
        ).exists()

    # DISPLAY NAME FIX
    for item in leaderboard:
        if item.user:
            item.display_name = item.user.username.split('@')[0]
        else:
            item.display_name = "Guest"

    # ===============================
    # SAVE CAPTURED IMAGE
    # ===============================
    if request.method == 'POST' and 'captured_image' in request.POST:
        img_data = request.POST['captured_image']
        format, imgstr = img_data.split(';base64,')
        ext = format.split('/')[-1]

        image_file = ContentFile(
            base64.b64decode(imgstr),
            name=f'image_{random.randint(1000,9999)}.{ext}'
        )

        img = ScoredImage.objects.create(
        image=image_file,
        score=0,
        user=request.user if request.user.is_authenticated else None
        )

        # ===============================
        # SCORE IMAGE
        # ===============================
        image_path = img.image.path
        score = predict_score(image_path)
        print("Predicted score:", score)
        if score >= 0:
            score = random.randint(50, 70)                    # (MODEL  IS UNDER PROCESS )
          # fallback for testing/demo purposes                                            (MODEL  IS UNDER PROCESS )
        img.score = score
        img.save()

        #  BLOCKCHAIN PAYOUT (ONLY ONCE PER USER)
        if request.user.is_authenticated and score >= 80:
          wallet = Wallet.objects.filter(user=request.user).first()

          if not wallet:
            messages.warning(request, " Create a demo wallet to receive rewards")
          else:
             already_paid = RewardTransaction.objects.filter(
             user=request.user,
               is_paid=True
                ).exists()

             if not already_paid:
                tx_hash = send_fake_eth(wallet.address)

                RewardTransaction.objects.create(
                user=request.user,
                score=score,
                wallet_address=wallet.address,
                tx_hash=tx_hash,
                is_paid=True
                )

                messages.success(
                request,
                " Demo ETH reward sent! (Ganache test network)"
                )

        return redirect('home')

    # ===============================
    # DELETE IMAGE
    # ===============================
    if request.method == 'POST' and 'delete_id' in request.POST:
        img_obj = get_object_or_404(ScoredImage, id=request.POST['delete_id'])

        if img_obj.user == request.user or img_obj.user is None:
            img_obj.delete()

        return redirect('home')

    return render(request, 'ai_scoring/home.html', {
        'images': images,
        'leaderboard': leaderboard,
        'has_leaderboard': has_leaderboard,
    })





from django.contrib import messages
@login_required
def upload_to_leaderboard(request, image_id):
    # Check if user already has an image on leaderboard
    existing = ScoredImage.objects.filter(user=request.user, is_leaderboard=True).first()
    if existing:
        messages.warning(request, "You already have an image on the leaderboard!")
        return redirect('home')

    # Get the image and mark it as leaderboard
    try:
        image = ScoredImage.objects.get(id=image_id, user=request.user)
        image.is_leaderboard = True
        image.save()
        messages.success(request, "Image uploaded to leaderboard!")
    except ScoredImage.DoesNotExist:
        messages.error(request, "Image not found!")

    return redirect('home')

