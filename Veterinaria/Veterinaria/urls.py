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

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name = "home"),
    path('login/', login, name = "login"),
    path('ingreso_sede/', ingreso_sede, name = "ingresar sede"),
    path('post_ingreso_sede/', post_ingr_sede),
    path('ingreso_vet/', ingreso_vet, name = "ingresar vet"),
    path('post_ingreso_vet/', post_ingr_vet),
    path('ingreso_especie/', ingreso_especie, name = "ingresar especie"),
    path('post_ingreso_esp/', post_ingr_esp),    
    path('post_usuario/', post_usuario),
    path('post_register/', post_register),
    path('register/', register, name = "registro"),
    path('agendar_consulta/', agendar_consulta, name = "consulta"),
    path('post_consulta/', post_consulta),  
    path('historial_consultas/',historial_consultas, name = "historial"),
    path('gestionMascotas/', gestionarMascotas, name = "gestion Mascotas"),
    path('post_ingresoMascota/', post_ingresoMascota),
    path('modificar_consulta/<int:idConsulta>/', modificarCons),
    path('post_modificar_consulta/', post_modificar_consulta),
    path('logout/', logout),
    path('cambiar_contrasenia/', modificarCont, name = "modificar contra"),
    path('post_modificar_contrasenia/', post_modificar_contrasenia)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)