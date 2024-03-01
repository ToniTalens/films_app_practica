import psycopg2
import logging
from typing import List
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula

class Persistencia_pelicula_pgSQL(IPersistencia_pelicula):
    def __init__(self, credenciales) -> None:
        self._credenciales = credenciales
        try:
            self._conn = psycopg2.connect(
                host=credenciales["host"],
                user=credenciales["user"],
                password=credenciales["password"],
                database=credenciales["database"]
            )
            if not self.check_table():
                self.create_table()
        except psycopg2.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.fetchall()
        except psycopg2.errors.UndefinedTable:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor()
        query = "SELECT COUNT(*) FROM PELICULA;"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = "SELECT * FROM PELICULA;"
        cursor.execute(query)
        resultats = cursor.fetchall()
        peliculas = []
        for resultat in resultats:
            pelicula = Pelicula(resultat[1], resultat[2], resultat[3], resultat[4], self, resultat[0])
            peliculas.append(pelicula)
        return peliculas
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor()
        peliculas = []
        if id is not None:
            cursor.execute("SELECT * FROM PELICULA WHERE ID = %s LIMIT 10", (id,))
        else:
            cursor.execute("SELECT * FROM PELICULA")
        for x in cursor:
            pelicula = Pelicula(x[0], x[1], x[2], x[3])
            peliculas.append(pelicula)
        return peliculas 
        
    def desa(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM PELICULA WHERE TITULO = %s", (pelicula.titol,))
        existPelicula = cursor.fetchone()
        if not existPelicula:
            cursor.execute("INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s)", (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots))
            logging.info("Película insertada")
        else:
            logging.warning("Este título ya existe. No se permiten títulos duplicados")
        self._conn.commit()
        return pelicula
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM PELICULA WHERE ANYO = %s", (any,))
        peliculas = []
        for x in cursor:
            pelicula = Pelicula(x[0], x[1], x[2], x[3])
            peliculas.append(pelicula)
        return peliculas
    
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        cursor.execute("UPDATE PELICULA SET VOTOS = %s WHERE id = %s", (pelicula.vots, pelicula.id))
        self._conn.commit()
        return pelicula
