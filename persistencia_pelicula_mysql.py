#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT ID , TITULO , ANYO , PUNTUACION , VOTOS FROM PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT ID , TITULO , ANYO , PUNTUACION , VOTOS FROM PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        pass
        #falta codi
    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query_insert = """ INSERT INTO PELICULA (TITULO , ANYO , PUNTUACION , VOTOS)
                           VALUES (%s , %s , %s ,%s);"""
        data = (pelicula._titol , pelicula._any , pelicula._puntuacio, pelicula._vots)
        cursor.execute(query_insert , data)
        self._conn.commit()
#        pelicula._id = cursor._last_insert_id
        pelicula._id = cursor.lastrowid
        cursor.close()
        result = Pelicula(pelicula._titol , pelicula._any , pelicula._puntuacio , pelicula._vots , self ,pelicula._id)
        return result
    
    def llegeix(self, any: int) -> Pelicula:
        pass
        #falta codi
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        pass
        #falta codi



if __name__ == "__main__":
    logging.basicConfig(filename='movies.log',encoding='utf-8',level=logging.DEBUG)
    credentials = {
        "host" : "localhost" ,
        "user" : "dam_app" ,
        "password" : "1234" ,
        "database" : "pelis"
    }

    pers_films = Persistencia_pelicula_mysql(credentials)

    #print(pers_films.allMovies())   // see All movies on terminal


    m = Pelicula("La sociedad sin nieve",2023,5.0,10000,pers_films)
    print("Movie Inserted Successfully .. \n" , m.persistencia.desa(m))

"""     read_movie = pers_films.readMovie("THE MEGG")
    if read_movie:
        print("The Movie Found : " , read_movie)
    else:
        print("Movie doesn't found . ") """