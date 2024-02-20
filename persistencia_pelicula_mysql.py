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
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
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
        query = "SELECT * FROM PELICULA WHERE id => :{id} ORDER BY id LIMIT 10;"
         
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],registre[0])
            resultat.append(pelicula)
        return resultat
        
      
        #falta codi
    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = """INSERT INTO PELICULA(titulo, anyo, puntuacion, votos) VALUES 
        (%s,%s,%s,%s)"""

        val = (f'{pelicula._titol}',f'{pelicula._any}',f'{pelicula._puntuacio}',f'{pelicula._vots}')

        cursor.execute(query,val)

        self._conn.commit()
        pelicula._id=cursor.lastrowid

        

        

        cursor.close()
        return pelicula
        
        


    
    def llegeix(self, any: int) -> List[Pelicula]:

        cursor = self._conn.cursor(buffered=True)
        query = f"SELECT * FROM PELICULA WHERE anyo = '{any}'"
         
        cursor.execute(query)
        pelis = cursor.fetchall()
        cursor.close()
        resultat = []
        return pelis


    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = """UPDATE PELICULA set titulo = %s, anyo=%s, 
        puntuacion=%s, votos=%s WHERE id = %s
        """


        val = (f'{pelicula._titol}',f'{pelicula._any}',f'{pelicula._puntuacio}',f'{pelicula._vots}',f'{pelicula._id}')



        
        cursor.execute(query,val)

        self._conn.commit()

        cursor.close()

        return pelicula

        


        
        #falta codi

if __name__ =='__main__':
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    credencials = {

         "host":"localhost"
        ,"user":"dam_app",
        "password":"1234"
        ,"database":"Pelis"


    }

    pers_films=Persistencia_pelicula_mysql(credencials)


    p = Pelicula("hola",1990,2.9,34335,pers_films)



       
    
    #print(pers_films.desa(p)) 
    #nueva_peli = Pelicula("Taylor Swift",2023,10,32324242,pers_films, 2)
    #print(pers_films.canvia(nueva_peli))

    print(pers_films.llegeix(1982))
