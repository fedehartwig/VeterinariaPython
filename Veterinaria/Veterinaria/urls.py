"""Veterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Veterinaria.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', login),
    path('login/', login),
    path('post_usuario/', post_usuario),
    path('post_regsiter/', post_register),
    path('register/', register),
    path('inicio/', inicio),
    path('agendar_consulta/', agendar_consulta),
    path('post_consulta/', post_consulta),  
    path('historial_consultas/',historial_consultas),
]

