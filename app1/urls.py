from django.urls import path

from . import views

urlpatterns = [
    path('hashtag/',views.HashtagPrediction,name='index'),
    path('polarity/',views.Polarity,name='index'),
    
]
