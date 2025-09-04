from rest_framework import serializers
from .models import ShortURL, Click

class CreateShortURLSerializer(serializers.Serializer):
    url = serializers.URLField()
    validity = serializers.IntegerField(required=False, min_value=1)
    shortcode = serializers.CharField(required=False, allow_blank=False, max_length=50)

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['timestamp', 'referrer', 'geo_location']

class ShortURLStatsSerializer(serializers.ModelSerializer):
    clicks = ClickSerializer(many=True)

    class Meta:
        model = ShortURL
        fields = ['url', 'shortcode', 'created_at', 'expiry', 'click_count', 'clicks']
