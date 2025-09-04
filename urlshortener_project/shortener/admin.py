from django.contrib import admin
from .models import ShortURL, Click

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('shortcode', 'url', 'created_at', 'expiry', 'click_count')
    search_fields = ('shortcode', 'url')

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('shorturl', 'timestamp', 'referrer', 'geo_location')
    list_filter = ('shorturl',)
