#!/usr/bin/python3

import mysql.connector
from pelicula import Pelicula
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
mydb = mysql.connector.connect(
    host = "localhost",
    user = "dam_app",
    password = "1234",
    database = "dam_m06"
)
mycursor = mydb.cursor()
mycursor.execute("USE pelis")

def cerca_per_camp(camp: str, valor):
    if type(valor) == str:
        valor = f"'{valor}'"
    mycursor.execute(f"SELECT * FROM PELICULA WHERE {camp} = {valor}")
    print(mydb)
    show_lines(mycursor)

def afegir_pelicula(titol, any, puntuacio, vots):
    mycursor.execute(f"INSERT PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES ('{titol}', {any}, {puntuacio}, {vots})")
    print(mydb)
    show_lines(mycursor)
    mydb.commit()

def modificar_pelicula(id: int, titol, any, puntuacio, vots):
    mycursor.execute(f"UPDATE PELICULA SET TITULO = '{titol}', ANYO = {any}, PUNTUACION = {puntuacio}, VOTOS = {vots} WHERE ID = {id};")
    print(mydb)
    show_lines(mycursor)
    mydb.commit()

#METODE PER MOSTRAR CONSULTA
def show_lines(cursor):
    for x in cursor:
        print(x)

# afegir_pelicula("Salvat", 2024, 10, 5)
# cerca_per_camp("TITULO", "Salvat")
# modificar_pelicula(1705, "Poma", 2025, 10 , 5)
# cerca_per_camp("ID", 1705)
credencials = {
    "host": "localhost",
    "user": "dam_app",
    "password": "1234",
    "database": "pelis"
}

persistencia = Persistencia_pelicula_mysql(credencials)
# peli = Pelicula("GOFRE", 2024, 123.456, 99, persitencia)
peli2 = Pelicula("SALVAT", 2024, 123.456, 99, persistencia)
# print(persistencia.totes())
print(persistencia.totes_pag(5))
# print(persistencia.desa(peli2))
# print(persistencia.llegeix(1990))
# print(persistencia.canvia(Pelicula("SALVATGE", 2024, 123.456, 99, persistencia, 1710)))
