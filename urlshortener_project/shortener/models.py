from django.db import models

class ShortURL(models.Model):
    url = models.URLField()
    shortcode = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shortcode} -> {self.url}"

class Click(models.Model):
    shorturl = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=256, null=True, blank=True)
    geo_location = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"Click {self.shorturl.shortcode} at {self.timestamp}"
