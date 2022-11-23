from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from django.contrib import messages

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
        return inicio(request)

def post_usuario(request):
    email_usr = request.POST["email"]
    contrasenia_usuario = request.POST["contrasenia"]
    if db.login(email_usr,contrasenia_usuario):
        return inicio(request)
    else:
        return login(request, "Los datos ingresados son incorrectos o no se corresponden con un usuario registrado")

def inicio(request):
    usuario = db.user(request.POST["email"]) #crear metodo user en CRUD 
    return render(request, "index.html", {"nombre" : usuario.nombre, "apellido" : usuario.apellido}) 

def agendar_consulta(request):
    return render(request, "ingreso_consulta.html")        

def post_consulta(request):
    usuario = request.POST["usuario"]
    fecha = request.POST["fecha"]
    medico = request.POST["medico"]
    sede = request.POST["sede"]    
    if db.agregarConsulta(usuario, fecha, medico, sede):
        messages.info(request, "La consulta se agendo correctamente")
    else:
        messages.info(request, "Hubo un error al agendar tu consulta")
    return inicio(request)

def historial_consultas(request):
    usuario = db.user(request.POST["email"]) #crear metodo user en CRUD 
    return render(request, "historial_consultas.html", {"nombre": usuario.nombre, "apellido" : usuario.apellido, "consultas" : db.consultas(usuario)}) #ver como implementar la lista de consultas 

# VER COMO PASAR EL USUARIO ENTRE METODOS 
