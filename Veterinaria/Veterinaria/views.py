from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from django.http import QueryDict

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

def historial(request):
    #traer datos de historial y pasarlos
    return render(request, "historial_consultas.html", {})

def inicio(request):
    #traer datos de inicio y pasarlos
    return render(request, "index.html", {})

def recibirPOST(request):
    usuario = request.POST["usuario"]
    password = request.POST["password"]
    #checkear con base de datos
    return #responder acorde al checkeo


def recibirRegister(request):
    nombre = request.POST["nombre"]
    apellido = request.POST["apellido"]
    dni = request.POST["DNI"]
    #actualizar base de datos
    return #responder acorde a la actualizacion
    
