from django.urls import path

from . import views

urlpatterns = [
    path('hashtag/',views.HashtagPrediction,name='hashtag'),
    path('polarity/',views.Polarity,name='polarity'),
    
    
    path('',views.index,name='INDEX'),
    path('analyze/',views.analyze,name='ANALYZE'),
    path('analyzeTweet/',views.Polarity,name='ANALYZETWEET'),
    path('components/',views.components,name='COMPONENTS'),
    path('forgotPass/',views.forgotPass,name='FORGOTPASS'),
    path('login/',views.login,name='LOGIN'),
    path('register/',views.register,name='REGISTER'),
    path('logout/', views.userLogOut, name='LOGOUT'), 
    path('contact/',views.contact,name='CONTACT'),
    
]
