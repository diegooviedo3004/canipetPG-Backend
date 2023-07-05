from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.index),
    path('descargar/', views.descargar, name="descargar"),

] 



