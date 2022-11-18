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

    def all_users (self):   #ANDA PIOLA - devuelve true si hay datos de usuarios, false sino
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
       
    def create_user (self, nombre, apellido, dni, telefono, mail, password):    #ANDA PIOLA
        sql = "insert into usuarios (Nombre, Apellido, DNI, Telefono, Mail, Password) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(nombre, apellido, dni, telefono, mail, password)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo el usuario")

    def especie (self, tipo, raza):
        sql="insert into especie (Tipo, Raza) values ('{}', '{}')".format(tipo, raza)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo la especie")

    def create_mascota (self, nombre, edad, peso, imagen):
        sql = "insert into mascotas (Nombre, Edad, Peso, Imagen, Mail, Password) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(nombre, edad, peso, imagen)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("No se creo el usuario")


mydb = Database()
mydb.all_users()
#hola = mydb.login("roman@gmail.com", "roman123")
#mydb.create_user("Martin", "Palermo", "546225", "564456", "goleador@gmail.com", "boca123")
