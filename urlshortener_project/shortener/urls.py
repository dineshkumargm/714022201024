from django.urls import path
from .views import CreateShortURL, RedirectView, StatsView

urlpatterns = [
    path('shorturls', CreateShortURL.as_view()),
    path('shorturls/<str:shortcode>', StatsView.as_view()),
    path('<str:shortcode>', RedirectView.as_view()),
]
