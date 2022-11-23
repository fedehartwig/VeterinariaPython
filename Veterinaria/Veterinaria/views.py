from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from django.http import QueryDict
from CRUD import Database

db = Database()

def login(request, error = ""):
    return render(request, "login.html", {"error" : error})

def register(request, error = ""):
    return render(request, "register.html", {"error" : error})

def post_register(request):
    email_usr = request.POST["email"]
    if db.userExists(email_usr): # ver como hacer para checkear existencia de usuario
        return register(request, "El mail ya esta registrado")
    else:
        nombre_usr = request.POST["nombre"]
        apellido_usr = request.POST["apellido"]
        dni_usr = request.POST["dni"]
        telefono_usr = request.POST["telefono"]
        contrasenia_usr = request.POST["password"]
        db.create_user(nombre_usr,apellido_usr,dni_usr,telefono_usr,contrasenia_usr)
        inicio(request)

def post_usuario(request):
    email_usr = request.POST["email"]
    contrasenia_usuario = request.POST["contrasenia"]
    if db.login(email_usr,contrasenia_usuario):
        inicio(request)
    else:
        login(request, "Los datos ingresados son incorrectos o no se corresponden con un usuario registrado")

def inicio(request):
    usuario = db.user(request.POST["email"]) #crear metodo user en CRUD 
    return render(request, "index.html", {"nombre" : usuario.nombre, "apellido" : usuario.apellido}) 

def historial_consultas(request):
    usuario = db.user(request.POST["email"]) #crear metodo user en CRUD 
    return render(request, "historial_consultas.html", {"consultas" : db.consultas(usuario)}) #ver como implementar la lista de consultas 

    
