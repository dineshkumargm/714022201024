from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
import string
import random

from .models import ShortURL, Click
from .serializers import CreateShortURLSerializer, ShortURLStatsSerializer

# -------------------------
# Existing helpers and classes
# -------------------------

ALPHANUM = string.ascii_letters + string.digits
DEFAULT_VALIDITY_MINUTES = 30
HOSTNAME = 'http://localhost:8000'  # used in responses

def generate_shortcode(length=6):
    return ''.join(random.choices(ALPHANUM, k=length))

def is_valid_custom_shortcode(s: str) -> bool:
    return 3 <= len(s) <= 50 and all(ch in ALPHANUM for ch in s)

# -------------------------
# Add this simple home view
# -------------------------
def home(request):
    return HttpResponse("<h1>Welcome to the URL Shortener!</h1><p>Use /shorturls/ to create links.</p>")

# -------------------------
# Your existing API views
# -------------------------
class CreateShortURL(APIView):
    def post(self, request):
        serializer = CreateShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        validity = serializer.validated_data.get('validity', DEFAULT_VALIDITY_MINUTES)
        shortcode = serializer.validated_data.get('shortcode')

        if shortcode:
            if not is_valid_custom_shortcode(shortcode):
                return Response({"error": "Invalid shortcode"}, status=status.HTTP_400_BAD_REQUEST)
            if ShortURL.objects.filter(shortcode=shortcode).exists():
                return Response({"error": "Shortcode already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            for _ in range(10):
                candidate = generate_shortcode()
                if not ShortURL.objects.filter(shortcode=candidate).exists():
                    shortcode = candidate
                    break
            if not shortcode:
                return Response({"error": "Could not generate shortcode"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        expiry = timezone.now() + timedelta(minutes=validity)
        shorturl = ShortURL.objects.create(url=url, shortcode=shortcode, expiry=expiry)
        request._log_event = f"CREATE SHORTCODE={shortcode} URL={url}"

        return Response({
            "shortLink": f"{HOSTNAME}/{shortcode}",
            "expiry": expiry.isoformat()
        }, status=status.HTTP_201_CREATED)

class RedirectView(APIView):
    def get(self, request, shortcode):
        shorturl = get_object_or_404(ShortURL, shortcode=shortcode)
        if timezone.now() > shorturl.expiry:
            return Response({"error": "Expired"}, status=status.HTTP_410_GONE)

        referrer = request.META.get('HTTP_REFERER')
        geo = request.META.get('REMOTE_ADDR')
        Click.objects.create(shorturl=shorturl, referrer=referrer, geo_location=geo)
        shorturl.click_count += 1
        shorturl.save()
        request._log_event = f"REDIRECT SHORTCODE={shortcode} CLIENT={geo}"

        return redirect(shorturl.url)

class StatsView(APIView):
    def get(self, request, shortcode):
        shorturl = get_object_or_404(ShortURL, shortcode=shortcode)
        serializer = ShortURLStatsSerializer(shorturl)
        request._log_event = f"STATS SHORTCODE={shortcode}"
        return Response(serializer.data)
