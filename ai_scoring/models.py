from django.db import models
from django.conf import settings

class ScoredImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='scored_images/')
    score = models.IntegerField(default=0)
    is_leaderboard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email if self.user else 'Guest'} - {self.score}"
