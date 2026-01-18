from django.contrib import admin
from .models import ScoredImage

@admin.register(ScoredImage)
class ScoredImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'is_leaderboard', 'created_at')
    list_filter = ('is_leaderboard', 'score')
    search_fields = ('user__email',)
    actions = ['remove_from_leaderboard']

    def remove_from_leaderboard(self, request, queryset):
        queryset.update(is_leaderboard=False)

    remove_from_leaderboard.short_description = "Remove selected from leaderboard"
