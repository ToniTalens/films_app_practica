import mysql.connector

from typing import List

import MySQLdb
import mysql
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        try:
            self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=str(credencials["password"]),
                database=credencials["database"]
            )

        except mysql.connector.Error as e:
            print(f"Error during database connection: {e}")
            self._conn = None

        if self._conn is not None and not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            with self._conn.cursor(buffered=True) as cursor:
                cursor.execute("SELECT * FROM PELICULA;")
                cursor.reset()
        except MySQLdb.connector.errors.ProgrammingError:
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
        cursor.close()  # Cierra el cursor antes de resetearlo
        cursor = self._conn.cursor(buffered=True)  # Abre un nuevo cursor
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA"
        if id is not None:
            query += f" WHERE id >= {id}"
        query += " LIMIT 10" 
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.close()  # Cierra el cursor antes de resetearlo
        cursor = self._conn.cursor(buffered=True)  # Abre un nuevo cursor
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)
        return resultat


    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        pass
    
    def llegeix(self, any: int) -> Pelicula:
        pass
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        pass