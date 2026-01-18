import os
from pyexpat import model
from ai_scoring.model.model import predict_score

IMAGE_PATH = "media/test.png"

if not os.path.exists(IMAGE_PATH):
    print("❌ Test image not found:", IMAGE_PATH)
else:
    score = predict_score(IMAGE_PATH)
    print("✅ FINAL SCORE:", score)

