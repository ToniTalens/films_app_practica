#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import psycopg #mirar
import logging

class Persistencia_pelicula_postgresql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = psycopg.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                dbname=credencials["database"]
                )

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except:
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
        # print(self._credencials)
        cursor = self._conn.cursor()
        query = f"select id, titulo, anyo, puntuacion, votos from PELICULA WHERE id >= {id} limit 10;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor._reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = f"INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES ('{pelicula.titol}',{pelicula.any},{pelicula.puntuacio},{pelicula.vots});"
        cursor.execute(query)
        self._conn.commit()
        cursor.execute(f"select id, titulo, anyo, puntuacion, votos from PELICULA where titulo = '{pelicula.titol}' and anyo = {pelicula.any}")
        registre = cursor.fetchone()
        cursor._reset()
        return Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])

    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = f"select id, titulo, anyo, puntuacion, votos from PELICULA where anyo = {any};"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor._reset()
        llista = []
        for registre in registres:
            llista.append(Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0]))
        return llista
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = f"UPDATE PELICULA SET TITULO = '{pelicula.titol}', ANYO = {pelicula.any}, PUNTUACION = {pelicula.puntuacio}, VOTOS = {pelicula.vots} WHERE ID = {pelicula.id};"
        cursor.execute(query)
        self._conn.commit()
        cursor.execute(f"select id, titulo, anyo, puntuacion, votos from PELICULA where id = '{pelicula.id}'")
        registre = cursor.fetchone()
        cursor._reset()
        return Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
