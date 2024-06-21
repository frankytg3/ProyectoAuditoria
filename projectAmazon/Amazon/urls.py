from django.urls import path
from .views import *

urlpatterns = [
    
    path('',productos,name='productos'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    
    
]