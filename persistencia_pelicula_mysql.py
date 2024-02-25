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
        cursor = self._conn.cursor(buffered=True)
        query_pag = ("""SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS
                      FROM PELICULA 
                     WHERE ID > %s 
                     ORDER BY ID ASC LIMIT 10;""")
        cursor.execute(query_pag , (id,))
        results = cursor.fetchall()
        result_pag = []
        for result in results:
            pelicula = Pelicula(result[1],result[2],result[3],result[4],self,result[0])
            result_pag.append(pelicula)
        return result_pag

    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query_insert = """ INSERT INTO PELICULA (TITULO , ANYO , PUNTUACION , VOTOS)
                           VALUES (%s , %s , %s ,%s);"""
        new_movie = (pelicula._titol , pelicula._any , pelicula._puntuacio, pelicula._vots)
        cursor.execute(query_insert , new_movie)
        self._conn.commit()
        #pelicula._id = cursor._last_insert_id
        pelicula._id = cursor.lastrowid
        cursor.close()
        result = Pelicula(pelicula._titol , pelicula._any , pelicula._puntuacio , pelicula._vots , self ,pelicula._id)
        return result
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query_read = "SELECT * FROM PELICULA WHERE ANYO = %s;"
        cursor.execute(query_read, (any,))
        results = cursor.fetchall()
        #result = cursor.fetchone()
        cursor.close()

        movies_of_year = []
        for result in results:
            movie = Pelicula(result[1], result[2], result[3], result[4], self, result[0])
            movies_of_year.append(movie)
    
        print(f"The Movies for the year {any} are : \n")
        for movie in movies_of_year:
            print(movie , "\n")
        return movies_of_year
    
        """if result :
            movie = Pelicula(result[1], result[2], result[3], result[4], self, result[0])
            return print(f"Movie for the year {any} is : \n" , movie)
        else:
            return print("Movie does'nt exist for the year : " , any)"""
        

    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query_update = """UPDATE PELICULA SET TITULO = %s, ANYO = %s,PUNTUACION = %s,VOTOS = %s 
                      WHERE ID = %s;"""
        modifications = (pelicula._titol, pelicula._any, pelicula._puntuacio, pelicula._vots, pelicula._id)
        cursor.execute(query_update, modifications)
        self._conn.commit()
        cursor.close()
        return pelicula


if __name__ == "__main__":
    logging.basicConfig(filename='movies.log',encoding='utf-8',level=logging.DEBUG)
    credencials = {
        "host" : "localhost" ,
        "user" : "dam_app" ,
        "password" : "1234" ,
        "database" : "pelis"
    }

    pers_films = Persistencia_pelicula_mysql(credencials)

    ## count All the Movies in : 
    #print("The number of movies are : \n",pers_films.count())

    ## Show all the movies on console
    #print("All the movies of the PELICULA table are : \n" , pers_films.totes())

    ## Movie's Pagination : 
    #print("The pagination of movies : \n" , pers_films.totes_pag(0))

    ## see All movies on terminal :
    #print(pers_films.totes())   

    ## Insert a new movie and show on terminal : 
    #m = Pelicula("La sociedad sin nieve",2023,5.0,10000,pers_films)
    #pers_films.desa(m)
    #print(" Movie Inserted Successfully .. \n" , m )

    ## read movie of a specific year : 
    #year = 1982
    #pers_films.llegeix(year)

    ## update a movie
    #updated = Pelicula("Magic",2011,7.5,1500,pers_films , id= 1695)
    #update_a_movie = print("Movie Updated : \n" , pers_films.canvia(updated))


