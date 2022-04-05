from django.urls import path

from . import views

urlpatterns = [
    path('hashtag/',views.HashtagPrediction,name='hashtag'),
    path('polarity/',views.Polarity,name='polarity'),
    
    
    path('',views.index,name='INDEX'),
    
]
