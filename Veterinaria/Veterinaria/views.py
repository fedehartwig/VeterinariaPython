from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, redirect
from django.contrib import sessions
from django.core.files.storage import FileSystemStorage

from procesamiento_imagenes import detectar_imagen

from CRUD import Database

db = Database()
def login(request):
    if 'logueado' in request.session: return redirect('home')    
    if 'hubo_error' not in request.session:
        request.session['hubo_error'] = False
    request.session['hubo_error_r'] = False
    request.session.modified = True
    return render(request, "login.html",{"hubo_error" : request.session['hubo_error']})      

def register(request):
    if 'logueado' in request.session: return redirect('home')
    if 'hubo_error_r' not in request.session:
        request.session['hubo_error_r'] = False
    request.session['hubo_error'] = False
    request.session.modified = True
    return render(request, "register.html", {"hubo_error" : request.session['hubo_error_r']} )

def gestionarMascotas(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] == 'Admin': return redirect('home')
    request.session['hubo_error_nc'] = False
    request.session['hubo_error_nueva_c'] = False
    request.session.modified = True
    return render(request, "ingresar_mascota.html", {'nombre' : request.session['nombre'], 'apellido' : request.session['apellido'],"listaEspecies":db.traer_Especies()[1], "flag" : request.session['hubo_error_mascota']})

def modificarCons(request, idConsulta): 
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] == 'Admin': return redirect('home')
    request.session['hubo_error_nc'] = False
    request.session['hubo_error_nueva_c'] = False
    request.session['hubo_error_mascota'] = False
    request.session['idCons'] = idConsulta
    request.session.modified = True
    contexto = {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "listaMedicos" : db.listaMedicos()[1], "listaSedes" : db.listaSedes()[1]}
    return render(request, "modificar_consulta.html", contexto)

def modificarCont(request):
    if 'logueado' not in request.session: return redirect('login')
    if 'hubo_error_nc' not in request.session:
        request.session['hubo_error_nc'] = False
        request.session['hubo_error_nueva_c'] = False
        request.session['hubo_error_mascota'] = False
        request.session.modified = True
    return render(request, "cambiar_contrasenia.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "hubo_error" : request.session['hubo_error_nc']})

def  post_modificar_consulta(request):
    if 'medico' not in request.POST: return redirect('home')
    fecha = request.POST.get('fecha')
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
        return redirect('home')
    return redirect('historial')

def post_modificar_contrasenia(request):
    if 'actual_password' not in request.POST: return redirect('home')
    contraseniaActual = request.POST.get("actual_password")
    contraseniaNueva = request.POST.get("new_password")
    contraseniaNueva2 = request.POST.get("new_password2")
    if contraseniaActual != request.session['pass'] or contraseniaNueva != contraseniaNueva2:
        request.session['hubo_error_nc'] = True
        request.session.modified = True
        return redirect('modificar contra')

    if db.modificar_password_usuario(request.session['email'], contraseniaNueva):
        return redirect('home')   

    request.session['hubo_error_nc'] = True
    request.session.modified = True
    return redirect('modificar contra')

def post_ingresoMascota(request):
    if 'nombre' not in request.POST: return redirect('home')
    nombreM = request.POST.get("nombre")
    edadM = request.POST.get("edad")
    peso = request.POST.get("peso")
    
    especie = request.POST.get("especie")    
    
    if request.method == 'POST' and request.FILES['img']:
        archivo = request.FILES['img']
        fs = FileSystemStorage()
        nombre_archivo= fs.save(archivo.name, archivo) 
        path_archivo = fs.url(nombre_archivo)
        path_archivo =path_archivo[1:]
    
    
    flag1, flag2 = detectar_imagen(path_archivo,especie)    
    print("Se pudo detecar la imagen:", flag1)
    print("La imagen coincide:", flag2)
    
    if not flag1 or not flag2:
        request.session['hubo_error_mascota'] = True
        request.session.modified = True
        fs.delete(nombre_archivo)
        return redirect('gestion Mascotas')    

    db.create_mascota(nombreM, edadM, peso, path_archivo, especie, request.session['email'])
    return redirect('home')
    
        
def logout(request):
    request.session.clear()
    return redirect('login')

def post_register(request):
    if 'email' not in request.POST: return redirect('home')
    email_usr = request.POST.get("email")        
    flag, usr = db.traer_usuario(email_usr)    

    if usr != None:        
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
            request.session['rol'] = 'Usuario'
            request.session['logueado'] = True
            request.session.modified = True
            return redirect('home')

        return redirect('registro')

def post_usuario(request):
    if 'email' not in request.POST: return redirect('home')
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
        request.session['rol'] = usuario[5] 
        request.session.modified = True        
        return redirect('home')

    request.session['hubo_error'] = True
    request.session.modified = True
    return redirect('login')

def ingreso_sede(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] != 'Admin': return redirect('home')
    request.session['hubo_error_vet'] = False 
    request.session['hubo_error_esp'] = False
    request.session.modified = True     
    return render(request, "ingresar_sede.html", {"nombre" : request.session['nombre'],  "apellido" : request.session['apellido'], "flag" : request.session['hubo_error_sede']})

def ingreso_vet(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] != 'Admin': return redirect('home')
    request.session['hubo_error_sede'] = False 
    request.session['hubo_error_esp'] = False
    request.session.modified = True         
    return render(request, "ingresar_medico.html", {"nombre" : request.session['nombre'],  "apellido" : request.session['apellido'], "flag" : request.session['hubo_error_vet']})

def ingreso_especie(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] != 'Admin': return redirect('home')
    request.session['hubo_error_sede'] = False 
    request.session['hubo_error_vet'] = False
    request.session.modified = True    
    return render(request, "ingresar_especie.html", {"nombre" : request.session['nombre'],  "apellido" : request.session['apellido'], "flag" : request.session['hubo_error_esp']})

def inicio(request):    
    if 'logueado' not in request.session: return redirect('login')       
    request.session['hubo_error_nc'] = False
    if request.session['rol'] == 'Admin':
        request.session['hubo_error_sede'] = False 
        request.session['hubo_error_vet'] = False
        request.session['hubo_error_esp'] = False 
        request.session.modified = True
        return render(request, "home_admin.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido']})
    
    request.session['hubo_error_mascota'] = False
    request.session['hubo_error_nueva_c'] = False 
    request.session.modified = True
    return render(request, "index.html", {"nombre" : request.session['nombre'], "apellido" : request.session['apellido']})

def agendar_consulta(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] == 'Admin': return redirect('home') 
    request.session['hubo_error_nc'] = False
    request.session['hubo_error_mascota'] = False
    request.session.modified = True
    contexto = {"nombre" : request.session['nombre'], "apellido" : request.session['apellido'], "listaMedicos" : db.listaMedicos()[1], "listaSedes" : db.listaSedes()[1], "flag" : request.session['hubo_error_nueva_c']}
    return render(request, "ingreso_consulta.html", contexto)  
        
def post_consulta(request):
    if 'sede' not in request.POST: return redirect('home')
    aux = (request.POST.get("medico")).split(" ")
    email_usr = request.session['email']
    fecha = request.POST.get("fecha")
    hora = fecha.split('T')[1]
    fecha = fecha.split('T')[0]
    nombreM = aux[0]  
    apellidoM = aux[1]
    sede = request.POST.get("sede")
    if db.create_turno(fecha, hora, email_usr, sede, nombreM, apellidoM):
        return redirect('home')     
    request.session['hubo_error_nueva_c'] = True
    request.session.modified = True
    return redirect('consulta')

def historial_consultas(request):
    if 'logueado' not in request.session: return redirect('login')
    if request.session['rol'] == 'Admin': return redirect('home') 
    request.session['hubo_error_nc'] = False
    request.session['hubo_error_nueva_c'] = False
    request.session['hubo_error_mascota'] = False
    request.session.modified = True    
    return render(request, "historial_consultas.html", {"nombre": request.session['nombre'], "apellido" : request.session['apellido'], "consultas" : db.traer_consultas_usuario(request.session['email'])[1]}) #ver como implementar la lista de consultas 
    
def post_ingr_sede(request):
    if 'direccion' not in request.POST: return redirect('home')
    direccion = request.POST.get('direccion')
    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    ##Informar si se puudo crear o no la sede
    if db.create_sedes(direccion, telefono, email): return redirect('home')
    request.session['hubo_error_sede'] = True
    request.session.modified = True
    return redirect('ingresar sede')

def post_ingr_vet(request):
    if 'nombre' not in request.POST: return redirect('home')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    dni = request.POST.get('dni')
    ##Informar si se puudo crear o no el medico
    if db.create_empleados(nombre, apellido, dni, "Veterinario"): return redirect('home')
    request.session['hubo_error_vet'] = True
    request.session.modified = True
    return redirect('ingresar vet')

def post_ingr_esp(request):
    if 'tipo' not in request.POST: return redirect('home')
    tipo = request.POST.get('tipo')    
    ##Informar si se puudo crear o no la especie
    if db.create_especie(tipo): return redirect('home') 
    request.session['hubo_error_esp'] = True
    request.session.modified = True
    return redirect('ingresar especie')




