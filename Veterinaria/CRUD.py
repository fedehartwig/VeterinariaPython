import json
import os.path
from datetime import datetime
from json.decoder import JSONDecodeError

import pymysql


class Database():
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Tuvieja22$', #1 2 3 4
            db='proyecto_final_vet'
        )
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")

    def login (self, mail, password):   #ANDA PIOLA - devuelve 1 si esta correcta, 0 sino
        sql= "select Mail, Password from usuarios where Mail = '{}' and Password = '{}' ".format(mail, password)
        flag = 0
        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchone()
            if users != None:
                flag = 1
            # print(users[0])
            # print(users[1])
            return flag
        except Exception as e:
            print("No existe ese mail con esa password")
            return flag

    # ANDA PIOLA - devuelve el user (vacio o no) y un flag. Si flag = 0-> No hay usuarios, si flag=1 devuelve todos los campos del user
    def traer_usuario(self, mail):
        sql = "SELECT Nombre, Apellido, DNI, Telefono, Mail, roluser.nombreRol FROM usuarios JOIN roluser on usuarios.idrolUser = roluser.idroluser where Mail = ('{}')".format(
            mail)
        flag = 0
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            flag = 1
            # print("Nombre:", user[0])
            # print("Apellido:", user[1])
            # print("DNI:", user[2])
            # print("Telefono:", user[3])
            # print("Mail:", user[4])
            # print("Rol:", user[5])
            # print (user)
            return flag, user

        except Exception as e:
            print("No hay nada en la tabla")
            return flag, user

    # ANDA PIOLA devuelve mascotas (vacio o no) y un flag. Si flag = 0-> No hay mascotas, si flag=1 devuelve todos los campos de mascotas del user
    def traer_mascotas_usuario(self, mail):
        sql = "SELECT mascotas.Nombre, Edad, Peso, Imagen FROM mascotas join usuarios on mascotas.ID_Usuarios = usuarios.ID_Usuarios where usuarios.Mail = ('{}')".format(
            mail)
        flag = 0
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchall()
            # print(user)
            flag = 1
            return user, flag

        except Exception as e:
            print("No hay nada en la tabla")
            return flag

    # ANDA PIOLA - devuelve 1 si creo el user, 0 sino
    def create_usuarios(self, nombre, apellido, dni, telefono, mail, password):
        sql1 = 'select idrolUser from roluser where nombreRol = "Usuario"'
        self.cursor.execute(sql1)
        idrolUser = self.cursor.fetchone()
        
        sql = "insert into usuarios (Nombre, Apellido, DNI, Telefono, Mail, Password, idrolUser) values ('{}', '{}', '{}', '{}', '{}', '{}','{}')".format(
            nombre, apellido, dni, telefono, mail, password, idrolUser[0])
        flag = 0
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo el usuario")
            return flag

    # ANDA PIOLA - devuelve 1 si creo la especie, 0 sino
    def create_especie(self, tipo):
        sql = "insert into especie (Tipo) values ('{}')".format(
            tipo)
        flag = 0
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo la especie")
            return flag

    def create_roles(self, nombre):  # ANDA PIOLA
        sql = "insert into roles (Nombre_rol) values ('{}')".format(nombre)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo el rol")

    def cambiar_rol_user(self, NombreRol, mailEnviado):  # ANDA PIOLA
        sql = "SELECT * FROM rolUser"
        sql2 = "SELECT Mail FROM usuarios"
        flag = 0
        idRol = 0
        nuevoMail = ""
        try:
            self.cursor.execute(sql)
            roles = self.cursor.fetchall()
            for rol in roles:
                if rol[1] == NombreRol:
                    idRol = rol[0]
            
            self.cursor.execute(sql2)
            mails = self.cursor.fetchall()
            for mail in mails:
                if mail[0] == mailEnviado:
                    nuevoMail = mailEnviado
        except Exception as e:
            print("No hay nada en la tabla")

        sql3 = "Update usuarios SET idrolUser = '{}' WHERE mail = '{}'".format(
                            idRol, nuevoMail)
        try:
            self.cursor.execute(sql3)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo el empleado")
            return flag
        
    def create_sedes(self, direccion, telefono, mail):  # ANDA PIOLA
        flag = 0
        sql = "insert into sedes (Direccion, Telefono, Mail) values ('{}', '{}', '{}')".format(
            direccion, telefono, mail)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo la sede")
            return flag

    # ANDA PIOLA - devuelve 1 si modifico el password, 0 sino
    def modificar_password_usuario(self, mail, passwordNew):
        sql = "SELECT Mail FROM usuarios"
        flag = 0
        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
            for user in users:
                if user[0] == mail:
                    try:
                        sql1 = "Update usuarios SET Password = '{}' WHERE mail = '{}'".format(
                            passwordNew, mail)
                        self.cursor.execute(sql1)
                        self.connection.commit()
                    except Exception as e:
                        print("No se modifico el password")
            flag = 1
            return flag

        except Exception as e:
            print("No hay nada en la tabla")
            return flag

    # ANDA PIOLA - devuelve 1 si creo la mascota, 0 sino
    def create_mascota(self, nombreMascota, edadMascota, pesoMascota, imagenMascota, tipo, mail):
        sql = "SELECT * FROM especie"
        flag = 0
        idUsuario = None
        idEspecie = None
        try:
            self.cursor.execute(sql)
            especies = self.cursor.fetchall()
            for especie in especies:
                if especie[1] == tipo:
                    idEspecie = especie[0]
        except Exception as e:
            print("No hay nada en la tabla")

        sql1 = "SELECT ID_Usuarios,Mail FROM usuarios"
        try:
            self.cursor.execute(sql1)
            usuarios = self.cursor.fetchall()
            for usuario in usuarios:
                if usuario[1] == mail:
                    idUsuario = usuario[0]
        except Exception as e:
            print("No hay nada en la tabla")

        sql2 = "insert into mascotas (Nombre, Edad, Peso, Imagen,ID_Usuarios,ID_Especie) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            nombreMascota, edadMascota, pesoMascota, imagenMascota, idUsuario, idEspecie)
        try:
            self.cursor.execute(sql2)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo la mascota")
            return flag

    # ANDA PIOLA - devuelve 1 si creo el empleado, 0 sino
    def create_empleados(self, nombreEmpleado, apellidoEmpleado, DNIEmpleado, NombreRol):
        sql = "SELECT * FROM roles"
        flag = 0
        idRol = None
        try:
            self.cursor.execute(sql)
            roles = self.cursor.fetchall()
            for rol in roles:
                if rol[1] == NombreRol:
                    idRol = rol[0]
        except Exception as e:
            print("No hay nada en la tabla")

        sql2 = "insert into empleados (Nombre, Apellido, DNI,ID_Roles) values ('{}', '{}', '{}', '{}')".format(
            nombreEmpleado, apellidoEmpleado, DNIEmpleado, idRol)
        try:
            self.cursor.execute(sql2)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo el empleado")
            return flag

    # ANDA PIOLA - devuelve 1 si creo el turno, 0 sino
    def create_turno(self, fecha, hora, mailUsuario, direcSede, NombreEmpleado, ApellidoEmpleado):
        sql1 = "SELECT ID_Usuarios,Mail FROM usuarios"
        flag = 0
        try:
            self.cursor.execute(sql1)
            usuarios = self.cursor.fetchall()
            for usuario in usuarios:
                if usuario[1] == mailUsuario:
                    idUsuario = usuario[0]
        except Exception as e:
            print("No hay nada en la tabla usuarios")

        sql2 = "SELECT ID_Sedes,Direccion FROM sedes"
        try:
            self.cursor.execute(sql2)
            sedes = self.cursor.fetchall()
            for sede in sedes:
                if sede[1] == direcSede:
                    idSedes = sede[0]
        except Exception as e:
            print("No hay nada en la tabla sedes")

        sql3 = "SELECT ID_Empleados,Nombre, Apellido FROM empleados"
        try:
            self.cursor.execute(sql3)
            empleados = self.cursor.fetchall()
            for empleado in empleados:
                if empleado[1] == NombreEmpleado and empleado[2] == ApellidoEmpleado:
                    idEmple = empleado[0]
        except Exception as e:
            print("No hay nada en la tabla empleados")

        time_data = fecha + ' ' + hora
        format_data = "%Y-%m-%d %H:%M"
        date = datetime.strptime(time_data, format_data)
        sql4 = "insert into turno (Fecha,ID_Usuarios,ID_Empleados, ID_Sedes) values ('{}', '{}', '{}', '{}')".format(
            date, idUsuario, idEmple, idSedes)
        
        with open('turnos.json', 'r') as file:
            players_data = json.load(file)

        datos = {"fecha": fecha, 
            "hora": hora, 
            "mailUsuario": mailUsuario, 
            "direcSede": direcSede, 
            "NombreEmpleado": NombreEmpleado,
            "ApellidoEmpleado": ApellidoEmpleado,
            "Accion": "se creo turno"
            }

        players_data['turnos'].append(datos)

        with open('turnos.json', 'w') as file:
            json.dump(players_data, file, indent = 2)
            
        try:
            self.cursor.execute(sql4)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo el turno")
            return flag




    # ANDA PIOLA - devuelve 1 si modifico el turno, 0 sino
    def update_turno(self, fecha, hora, mailUsuario, direcSede, NombreEmpleado, ApellidoEmpleado, idConsulta):
        sql1 = "SELECT ID_Usuarios,Mail FROM usuarios"
        flag = 1
        try:
            self.cursor.execute(sql1)
            usuarios = self.cursor.fetchall()
            for usuario in usuarios:
                if usuario[1] == mailUsuario:
                    idUsuario = usuario[0]
        except Exception as e:
            print("No hay nada en la tabla usuarios")

        sql2 = "SELECT ID_Sedes,Direccion FROM sedes"
        try:
            self.cursor.execute(sql2)
            sedes = self.cursor.fetchall()
            for sede in sedes:
                if sede[1] == direcSede:
                    idSedes = sede[0]
        except Exception as e:
            print("No hay nada en la tabla sedes")

        sql3 = "SELECT ID_Empleados,Nombre, Apellido FROM empleados"
        try:
            self.cursor.execute(sql3)
            empleados = self.cursor.fetchall()
            for empleado in empleados:
                if empleado[1] == NombreEmpleado and empleado[2] == ApellidoEmpleado:
                    idEmple = empleado[0]
        except Exception as e:
            print("No hay nada en la tabla empleados")

        time_data = fecha + ' ' + hora
        format_data = "%Y-%m-%d %H:%M"
        date = datetime.strptime(time_data, format_data)
        sql4 = "update turno set Fecha = ('{}'), ID_Usuarios = ('{}'), ID_Empleados = ('{}') , ID_Sedes = ('{}') where ID_Turno = ('{}')".format(
            date, idUsuario, idEmple, idSedes, idConsulta)
        
        with open('turnos.json', 'r') as file:
            players_data = json.load(file)

        datos = {"fecha": fecha, 
            "hora": hora, 
            "mailUsuario": mailUsuario, 
            "direcSede": direcSede, 
            "NombreEmpleado": NombreEmpleado,
            "ApellidoEmpleado": ApellidoEmpleado,
            "Accion": "se modifico turno"
            }

        players_data['turnos'].append(datos)

        with open('turnos.json', 'w') as file:
            json.dump(players_data, file, indent = 2)

        try:
            self.cursor.execute(sql4)
            self.connection.commit()
            flag = 1
            return flag
        except Exception as e:
            print("No se creo el turno")
            return flag

    # ANDA PIOLA - devuelve 1 si trae las consultas del user, 0 sino
    def traer_consultas_usuario(self, mail):
        sql = "select ID_Turno, usuarios.Nombre, usuarios.Apellido, Fecha, sedes.Direccion, empleados.Nombre from turno join usuarios on turno.ID_Usuarios = usuarios.ID_Usuarios join sedes on turno.ID_Sedes = sedes.ID_Sedes join empleados on turno.ID_Empleados = empleados.ID_Empleados where usuarios.Mail = ('{}')".format(
            mail)
        flag = 0
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchall()
            lista = list(user)
           

            # lista = user[0][3].strftime("%Y-%m-%d %H:%M")
            for i in range(len(lista)):
                lista[i] = list(lista[i])
                lista[i][3] = user[i][3].strftime("%Y-%m-%d %H:%M")
            
            
            flag = 1
            return flag, lista

        except Exception as e:
            print("No hay nada en la tabla")
            return flag, []

    def listaMedicos (self):
        sql = "SELECT * from empleados"
        flag = 0
        try:
            self.cursor.execute(sql)
            empleados = self.cursor.fetchall()
            flag = 1
            return flag, empleados

        except Exception as e:
            print("No hay nada en la tabla")
            return flag, empleados

    def listaSedes (self):
        sql = "SELECT Direccion from sedes"
        flag = 0
        try:
            self.cursor.execute(sql)
            sedes = self.cursor.fetchall()
            flag = 1
            return flag, sedes

        except Exception as e:
            print("No hay nada en la tabla")
            return flag, sedes

    def traer_Especies (self):
        sql = "SELECT Tipo from Especie"
        flag = 0
        try:
            self.cursor.execute(sql)
            especies = self.cursor.fetchall()
            flag = 1
            return flag, especies

        except Exception as e:
            print("No hay nada en la tabla")
            return flag, especies

    # FUNCIONES QUE FALTAN: LISTAS DE SEDES (CALLE) Y DE VETERINARIOS (NOMBRE APELLIDO)


mydb = Database()
#hola = print(mydb.traer_usuario("goleador3@gmail.com"))
# mydb.modificar_password_usuario("goleador3@gmail.com","1234")
# mydb.all_usuarios()
# hola = mydb.login("roman@gmail.com", "roman123")
hola = mydb.create_especie("perro")
mydb.create_mascota("RODRI","3","20","Imagen/RODRI.png","perro","goleador3@gmail.com")

mydb.create_roles("Veterinario")
mydb.create_sedes("Rivada 543","1145365123","vet@gmail.com")

mydb.cambiar_rol_user("usuario","goleador3@gmail.com")

mydb.create_usuarios("Martin", "Palermo", "3", "3", "goleador3@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "4", "4", "goleador4@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "5", "5", "goleador5@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "6", "6", "goleador6@gmail.com", "boca123")

mydb.create_empleados("Carlos", "Rodriguez", "32154674", "Veterinario")

mydb.create_turno("2020-10-12", "19:30", "goleador3@gmail.com","Rivada 543" , "Carlos", "Rodriguez")
mydb.update_turno("2020-10-12", "19:30", "goleador3@gmail.com","Rivada 543" , "Carlos", "Rodriguez", 2)

# now='5/5/22'
# print("Before", now)
# now= datetime.strptime(dob,'%m/%d/%y').strftime('%Y-%m-%d')
# print("After", now)
# cursor.execute("INSERT INTO table (name, id, datecolumn) VALUES (%s, %s, %s)",(name, 4,now))

#flag, hola = mydb.traer_usuario("goleador3@gmail.com")

# hola = mydb.traer_mascotas_usuario("goleador3@gmail.com")
#print(hola)
# datos = {
#     "Nombre": hola[0],
#     "Apellido": hola[1],
#     "DNI": hola[2],
#     "Telefono": hola[3],
#     "Mail": hola[4],
#     "Rol" : hola[5]
#     #"Accion": "Se trajo al usuario",
# }



# with open('players.json', 'r') as file:
#     players_data = json.load(file)
# players_data['medicos'].append(datos)

# with open('players.json', 'w') as file:
#     json.dump(players_data, file)