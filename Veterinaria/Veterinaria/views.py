from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, redirect
from django.contrib import messages, sessions

from CRUD import Database

db = Database()
def login(request):
    if 'logueado' in request.session:
        return redirect('home')
    
    if 'hubo_error' not in request.session:
        request.session['hubo_error'] = False
    request.session['hubo_error_r'] = False
    request.session.modified = True
    return render(request, "login.html",{"hubo_error" : request.session['hubo_error']})
    #return render(request, "login.html")

def register(request):
    if 'logueado' in request.session:
        return redirect('home')
    if 'hubo_error_r' not in request.session:
        request.session['hubo_error_r'] = False
    request.session['hubo_error'] = False
    request.session.modified = True
    return render(request, "register.html", {"hubo_error" : request.session['hubo_error_r']} )

def gestionarMascotas(request):
    if 'logueado' not in request.session:
        return redirect('login')
    request.session['hubo_error_nc'] = False
    request.session.modified = True
    return render(request, "ingresar_mascota.html", {'nombre' : request.session['nombre'], 'apellido' : request.session['apellido'],"listaEspecies":db.traer_Especies()[1]})

def modificarCons(request, idConsulta): #modificar front para q aparezca la lista de medicos como en agendar consulta
    if 'logueado' not in request.session:
        return redirect('login')
    request.session['hubo_error_nc'] = False
    request.session['idCons'] = idConsulta
    request.session.modified = True
    contexto = {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "listaMedicos" : db.listaMedicos()[1], "listaSedes" : db.listaSedes()[1]}
    return render(request, "modificar_consulta.html", contexto)

def modificarCont(request):
    if 'logueado' not in request.session:
        return redirect('login')
    if 'hubo_error_nc' not in request.session:
        request.session['hubo_error_nc'] = False
        request.session.modified = True
    return render(request, "cambiar_contrasenia.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "hubo_error" : request.session['hubo_error_nc']})

def  post_modificar_consulta(request):
    fecha = request.POST.get("fecha")
    hora = fecha.split('T')[1]
    fecha = fecha.split('T')[0]
    medico= request.POST.get('medico')
    nombreM = medico.split(' ')[0]
    apellidoM = medico.split(' ')[1]
    sede = request.POST.get('sede')
    id = request.session['idCons']
    request.session.pop('idCons')
    request.session.modified = True
    if db.update_turno(fecha, hora, request.session['email'], sede, nombreM, apellidoM, id):
        messages.info(request, "su consulta se modifico satisfactoriamente!")
        return redirect('home')
    messages.info(request, "Hubo un error al modificar su consulta")
    return redirect('historial')

def post_modificar_contrasenia(request):
    contraseniaActual = request.POST.get("actual_password")
    contraseniaNueva = request.POST.get("new_password")
    contraseniaNueva2 = request.POST.get("new_password2")
    if contraseniaActual != request.session['pass'] or contraseniaNueva != contraseniaNueva2:
        request.session['hubo_error_nc'] = True
        request.session.modified = True
        return redirect('modificar contra')
    elif db.modificar_password_usuario(request.session['email'], contraseniaNueva):
        messages.info(request, "La contraseña fue modificada con exito!")
        return redirect('home')
    else:
        request.session['hubo_error_nc'] = True
        request.session.modified = True
        return redirect('modificar contra')

def post_ingresoMascota(request):
    nombreM = request.POST.get("nombre")
    edadM = request.POST.get("edad")
    peso = request.POST.get("peso")
    img = request.POST.get("img")
    especie = request.POST.get("especie")   
    descripcion = request.POST.get("descripcion") #agregar raza al formulario

    #implementar control con reconocimiento de imagenes para ver q la especie se
    #corresponda con la imagen, luego convertir imagen a link/path
    
    linkimg = None #cambiar por conversion a link/path

    if db.create_mascota(nombreM, edadM, peso, img, especie, request.session['email']):
        messages.info(request, "Tu mascota se guardo satisfactoriamente!")
        return redirect('home')
    else:
        messages.info(request, "Ocurrio un error al registrar a tu mascota, por favor intentalo nuevamente")
        return redirect('historial')
        
        
def logout(request):
    request.session.clear()
    return redirect('login')

def post_register(request):
    email_usr = request.POST.get("email")        
    flag, usr = db.traer_usuario(email_usr)    
    if usr != None:  
        #messages.error(request, "El mail ya esta registrado")
        request.session['hubo_error_r'] = True
        request.session.modified = True
        return redirect('registro')
    else:
        nombre_usr = request.POST.get("nombre")
        apellido_usr = request.POST.get("apellido")
        dni_usr = request.POST.get("dni")
        telefono_usr = request.POST.get("telefono")
        contrasenia_usr = request.POST.get("contra")
        if db.create_usuarios(nombre_usr, apellido_usr, dni_usr, telefono_usr, email_usr, contrasenia_usr):
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
            return redirect('registro')
        

def post_usuario(request):
    email_usr = request.POST.get("email")
    contrasenia_usuario = request.POST.get("contrasenia")
    print("Email:", email_usr)
    print("contra:", contrasenia_usuario)
    print(db.login(email_usr, contrasenia_usuario))    
    if db.login(email_usr, contrasenia_usuario):
        flag, usuario = db.traer_usuario(email_usr)        
        request.session['nombre'] = usuario[0]
        request.session['apellido'] = usuario[1]
        request.session['DNI'] = usuario[2]
        request.session['telefono'] = usuario[3]
        request.session['pass'] = contrasenia_usuario
        request.session['email'] = email_usr
        request.session['logueado'] = True
        request.session['hubo_error'] = False
        request.session.modified = True        
        return redirect('home')
    else:
        #messages.error(request, "Los datos ingresados son incorrectos o no se corresponden con un usuario registrado")
        request.session['hubo_error'] = True
        request.session.modified = True
        return redirect('login')

def inicio(request):
    if 'logueado' not in request.session:
        return redirect('login')
    request.session['hubo_error_nc'] = False
    request.session.modified = True
    return render(request, "index.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido']})
    
        

def agendar_consulta(request):
    if 'logueado' not in request.session:
        return redirect('login')
    request.session['hubo_error_nc'] = False
    request.session.modified = True
    contexto = {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "listaMedicos" : db.listaMedicos()[1], "listaSedes" : db.listaSedes()[1]}
    return render(request, "ingreso_consulta.html", contexto)  
        


def post_consulta(request):
    aux = (request.POST.get("medico")).split(" ")
    email_usr = request.session['email']
    fecha = request.POST.get("fecha")
    hora = fecha.split('T')[1]
    fecha = fecha.split('T')[0]
    nombreM = aux[0] #cambiar la carga para ingresar nombre y apellido del medico 
    apellidoM = aux[1]
    sede = request.POST.get("sede")
    if db.create_turno(fecha, hora, email_usr, sede, nombreM, apellidoM):
        messages.info(request, "La consulta se agendo correctamente")
    else:
        messages.info(request, "Hubo un error al agendar tu consulta")
    return redirect('home')

def historial_consultas(request):
    if 'logueado' not in request.session:
        return redirect('login')
    request.session['hubo_error_nc'] = False
    request.session.modified = True    
    return render(request, "historial_consultas.html", {"nombre": request.session['nombre'], "apellido" : request.session['apellido'], "consultas" : db.traer_consultas_usuario(request.session['email'])[1]}) #ver como implementar la lista de consultas 
    
        
#TO DO
#Control de imagegn con csv
#Conversion de img a link/path
#hablar con front sobre:

## post_consulta (formulario nueva consulta) (todavia hay q ver el tema e los nombres de medicos)
## post_ingreso_mascota (formulario de nueva mascota) (todavia hay q ver lo de la raza) 
# Hablar con front y crud:
## post_modificar_consulta (formulario para modificar consulta) (todavia hay q ver el tema e los nombres de medicos y como mandar id) (integrar al home)
######cambiar los values en los forms por texto ya que el id puede variar
######cambiar como ingresar nombre de medico en modificar consulta a una seleccion como en agendar
###### base de datos metodos q me traigan sedes y medicos 
###### separar especie de raza en base de datos (o directamente eliminar raza y fue)
