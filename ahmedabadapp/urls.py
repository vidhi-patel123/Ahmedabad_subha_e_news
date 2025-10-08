"""
URL configuration for ahmedabadproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from .views import*

urlpatterns = [
    path('', views.home, name='home'),
    path('api/',ContactView.as_view()),
    path('api/<int:id>/',ContactView.as_view()),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('terms_and_condition', views.terms_and_condition, name='terms_and_condition'),
    path('ahmedabad-subah', views.ahmedabad_subah, name='ahmedabad-subah'),
    path('birch-academia', views.birch_academia, name='birch-academia'),
    path('ignite-digital', views.ignite_digital, name='ignite-digital'),
    path('trending-around', views.trending_around, name='trending-around'),
    
    # -----------------------------E-NEWS CODE----------------------
    path('newspaper', views.newspaper, name='newspaper'),
    path('uploaded', views.uploaded, name='uploaded'),
    path('fetch_videos/', views.fetch_youtube_videos, name='fetch_videos'),
    path('youtube/', views.latest_youtube_videos, name='youtube_videos'),
    
]
