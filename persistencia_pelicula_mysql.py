#!/bin/usr/python3

from sqlite3 import Cursor
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
         if id is None:
            query_pag = f"SELECT ID , TITULO , ANYO , PUNTUACION , VOTOS FROM PELICULA LIMIT 10;"

         else:
            query_pag = f"SELECT ID , TITULO , ANYO , PUNTUACION , VOTOS FROM PELICULA WHERE id > {id} ORDER BY id LIMIT 10;"

         Cursor.execute(query_pag)
         results = cursor.fetchall()
         result_pag = []
         for result in results:
             pelicula = Pelicula(result[1],result[2],result[3],result[4],self,result[0])
             result_pag.append(pelicula)
             return result_pag

    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        insert_query = f"INSERT INTO PELICULA(TITULO, ANYO, PUNTUACION, VOTOS) VALUES ('{pelicula.titol}', {pelicula.any}, {pelicula.puntuacio}, {pelicula.vots});"
        cursor.execute(insert_query)
        self._conn.commit()
        select_query = f"SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA WHERE TITULO='{pelicula.titol}' AND ANYO={pelicula.any};"
        cursor.execute(select_query)
        registre = cursor.fetchone()
        return Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        select_query = f"SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA WHERE ANYO={any};"
        cursor.execute(select_query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        update_query = (f"UPDATE PELICULA SET TITULO='{pelicula.titol}', "
                        f"ANYO={pelicula.any}, "
                        f"PUNTUACION={pelicula.puntuacio}, "
                        f"VOTOS={pelicula.vots} "
                        f"WHERE ID={pelicula.id}")
        cursor.execute(update_query)
        select_query = f"SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA WHERE ID={pelicula.id};"
        cursor.execute(select_query)
        registre = cursor.fetchone()
        return Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
