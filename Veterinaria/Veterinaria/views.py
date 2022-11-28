from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, redirect
from django.contrib import messages, sessions

from CRUD import Database

db = Database()
def login(request):
    if 'logueado' in request.session:
        return redirect('home')
    return render(request, "login.html")

def register(request):
    if 'logueado' in request.session:
        return redirect('home')
    return render(request, "register.html")

def gestionarMascotas(request):
    if 'logueado' not in request.session:
        return redirect('login')
    return render(request, "ingresar_mascota.html", {'nombre' : request.session['nombre'], 'apellido' : request.session['apellido']})

def modificarC(request):
    if 'logueado' not in request.session:
        return redirect('login')
    return render(request, "modificar_consulta")

def  post_modificar_consulta(request):
    fecha = request.POST.get("fecha")
    hora = fecha.split('T')[1]
    fecha = fecha.split('T')[0]
    nombreM = request.POST.get("nombre")
    apellidoM = request.POST.get("apellido")
    sede = request.POST.get("sede")
    id = None #ver de donde sacar id y los datos de la consulta original
    if db.update_turno(fecha, hora, request.session['email'], sede, nombreM, apellidoM, id):
        messages.info(request, "su consulta se modifico satisfactoriamente!")
        return redirect('home')
    messages.info(request, "Hubo un error al modificar su consulta")
    return redirect('historial')

def post_ingresoMascota(request):
    nombreM = request.POST.get("nombre")
    edadM = request.POST.get("edad")
    peso = request.POST.get("peso")
    img = request.POST.get("img")
    especie = request.POST.get("especie")
    raza = request.POST.get("raza") #agregar raza al formulario

    #implementar control con reconocimiento de imagenes para ver q la especie se
    #corresponda con la imagen, luego convertir imagen a link/path
    
    linkimg = None #cambiar por conversion a link/path
    if db.create_mascota(nombreM, edadM, peso, linkimg, especie, raza, request.session['email']):
        messages.info(request, "Tu mascota se guardo satisfactoriamente!")
        return redirect('home')
    else:
        messages.info(request, "Ocurrio un error al registrar a tu mascota, por favor intentalo nuevamente")

def logout(request):
    request.session.clear()
    return redirect('login')

def post_register(request):
    email_usr = request.POST.get("email")
    flag, usr = db.traer_usuario(email_usr)
    if flag:  
        messages.error(request, "El mail ya esta registrado")
        return redirect('login')
    else:
        nombre_usr = request.POST.get("nombre")
        apellido_usr = request.POST.get("apellido")
        dni_usr = request.POST.get("dni")
        telefono_usr = request.POST.get("telefono")
        contrasenia_usr = request.POST.get("password")
        if db.create_usuarios(nombre_usr, apellido_usr, dni_usr, telefono_usr, contrasenia_usr):
            request.session['nombre'] = nombre_usr
            request.session['apellido'] = apellido_usr
            request.session['DNI'] = dni_usr
            request.session['telefono'] = telefono_usr
            request.session['email'] = email_usr
            request.session['pass'] = contrasenia_usr
            request.session['logueado'] = True
            request.session.modified = True
            messages.info(request, "El usuario se registro con exito!")
            return redirect('home')
        else:
            messages.info(request, "Hubo un error en el registro, por favor intente nuevamente")
        

def post_usuario(request):
    email_usr = request.POST.get("email")
    contrasenia_usuario = request.POST.get("contrasenia")    
    if db.login(email_usr, contrasenia_usuario):
        flag, usuario = db.traer_usuario(email_usr)        
        request.session['nombre'] = usuario[0]
        request.session['apellido'] = usuario[1]
        request.session['DNI'] = usuario[2]
        request.session['telefono'] = usuario[3]
        request.session['pass'] = contrasenia_usuario
        request.session['email'] = email_usr
        request.session['logueado'] = True
        request.session.modified = True        
        return redirect('home')
    else:
        messages.error(request, "Los datos ingresados son incorrectos o no se corresponden con un usuario registrado")
        return redirect('login')

def inicio(request):
    if 'logueado' not in request.session:
        return redirect('login')
    return render(request, "index.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido']})
    
        

def agendar_consulta(request):
    if 'logueado' not in request.session:
        return redirect('login')
    return render(request, "ingreso_consulta.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido']})  
        


def post_consulta(request):
    email_usr = request.session['email']
    fecha = request.POST.get("fecha")
    hora = fecha.split('T')[1]
    fecha = fecha.split('T')[0]
    nombreM = request.POST.get("nombre") #cambiar la carga para ingresar nombre y apellido del medico 
    apellidoM = request.POST.get("apellido") 
    sede = request.POST.get("sede")
    if db.create_turno(fecha, hora, email_usr, sede, nombreM, apellidoM):
        messages.info(request, "La consulta se agendo correctamente")
    else:
        messages.info(request, "Hubo un error al agendar tu consulta")
    return redirect('home')

def historial_consultas(request):
    if 'logueado' not in request.session:
        return redirect('login')
    return render(request, "historial_consultas.html", {"nombre": request.session['nombre'], "apellido" : request.session['apellido'], "consultas" : db.traer_consultas_usuario(request.session['email'])}) #ver como implementar la lista de consultas 
    
        
#TO DO
#Control de imagegn con csv
#Conversion de img a link/path
#hablar con front sobre:
## post_consulta (formulario nueva consulta)
## post_ingreso_mascota (formulario de nueva mascota)
## formulario para cambiar contraseña, boton para el cambio en login y boton logout en home
# Hablar con front y crud:
## post_modificar_consulta (formulario para modificar consulta)
