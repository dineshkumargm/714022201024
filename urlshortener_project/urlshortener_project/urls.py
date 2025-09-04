from django.contrib import admin
from django.urls import path
from shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # root path
    path('shorturls/', views.CreateShortURL.as_view(), name='create_shorturl'),
    path('shorturls/<str:shortcode>/', views.StatsView.as_view(), name='shorturl_stats'),
    path('<str:shortcode>/', views.RedirectView.as_view(), name='redirect'),
]
