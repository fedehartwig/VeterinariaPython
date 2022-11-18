import pymysql
import json

class Database():
    def __init__(self) :
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password='1234',
            db = 'proyecto_final_vet'
        )
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")

    def login (self, mail, password):   #ANDA PIOLA - devuelve true si esta correcta, false sino
        sql= "select Mail, Password from usuarios where Mail = '{}' and Password = '{}' ".format(mail, password)
        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchone()
            # print(users[0])
            # print(users[1])
            return True
        except Exception as e:
            print("No existe ese mail con esa password")
            return False

    def all_usuarios (self):   #ANDA PIOLA - devuelve true si hay datos de usuarios, false sino
        sql = "SELECT * FROM usuarios"
        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
            print(type(users))
            print(users)
            for user in users:
                print("ID:", user[0])
                print("Nombre:", user[1])
                print("Contrase;a:", user[2])
            return True

        except Exception as e:
            print("No hay nada en la tabla")
            return False
       
    def create_usuarios (self, nombre, apellido, dni, telefono, mail, password):    #ANDA PIOLA
        sql = "insert into usuarios (Nombre, Apellido, DNI, Telefono, Mail, Password) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(nombre, apellido, dni, telefono, mail, password)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo el usuario")

    def create_especie (self, tipo, raza):    #ANDA PIOLA
        sql="insert into especie (Tipo, Raza) values ('{}', '{}')".format(tipo, raza)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo la especie")

    def create_roles (self, nombre):    #ANDA PIOLA
        sql = "insert into roles (Nombre_rol) values ('{}')".format(nombre)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo el rol")
            
    def create_sedes (self, direccion, telefono, mail):    #ANDA PIOLA
        sql = "insert into sedes (Direccion, Telefono, Mail) values ('{}', '{}', '{}')".format(direccion, telefono, mail)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo la sede")

    def modificar_password_usuario (self, mail, passwordNew):    #ANDA PIOLA
        #ANDA PIOLA - devuelve true si hay datos de usuarios, false sino
        sql = "SELECT Mail FROM usuarios"
        try:
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
            for user in users:
                if user[0] == mail:
                    try:
                        sql1="Update usuarios SET Password = '{}' WHERE mail = '{}'".format(passwordNew,mail)
                        self.cursor.execute(sql1)
                        self.connection.commit()
                    except Exception as e:
                        print("No se modifico el password")
                print("Mail:", user[0])
            return True

        except Exception as e:
            print("No hay nada en la tabla")
            return False

    def create_mascota (self, nombreMascota, edadMascota, pesoMascota, imagenMascota, tipo, raza, mail):
        sql = "SELECT * FROM especie"
        try:
            self.cursor.execute(sql)
            especies = self.cursor.fetchall()
            for especie in especies:
                if especie[1] == tipo and especie[2] == raza:
                    idEspecie=especie[0]
                else:
                    print("No se encontro la especie")
            return True
        except Exception as e:
            print("No hay nada en la tabla")

        
        sql1 = "SELECT ID_Usuarios,Mail FROM usuarios"
        try:
            self.cursor.execute(sql1)
            usuarios = self.cursor.fetchall()
            for usuario in usuarios:
                if usuario[1] == mail:
                    idUsuario=especie[0]
                else:
                    print("No se encontro el usuario")
            return True
        except Exception as e:
            print("No hay nada en la tabla")

        
        sql = "insert into mascotas (Nombre, Edad, Peso, Imagen,ID_Usuarios,ID_Especie) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(nombreMascota, edadMascota, pesoMascota, imagenMascota,idUsuario,idEspecie)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo la mascota")
            
       

mydb = Database()
#mydb.modificar_password_usuario("goleador3@gmail.com","1234")
#mydb.all_usuarios()
#hola = mydb.login("roman@gmail.com", "roman123")
#hola = mydb.create_especie("perro","bulldog")
mydb.create_mascota("Wally","5","30","Imagen/wally.png","perro","bulldog","goleador3@gmail.com")

# mydb.create_roles("Veterinario")
#mydb.create_sedes("Rivada 543","1145365123","vet@gmail.com")

# mydb.create_usuarios("Martin", "Palermo", "3", "3", "goleador3@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "4", "4", "goleador4@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "5", "5", "goleador5@gmail.com", "boca123")
# mydb.create_usuarios("Martin", "Palermo", "6", "6", "goleador6@gmail.com", "boca123")