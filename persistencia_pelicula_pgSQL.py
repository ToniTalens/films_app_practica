#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import psycopg
import logging

class Persistencia_pelicula_pgSQL(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        host=credencials["host"]
        user=credencials["user"]
        password=credencials["password"]
        database=credencials["database"]
        self._conn = psycopg.connect(f"host={host} dbname={database} user={user} password={password}")
            
        

    def check_table(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except (Exception, psycopg.Error):
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
    
    def totes_pag(self, id) -> List[Pelicula]:
        cursor = self._conn.cursor()
        sql = f"SELECT * FROM PELICULA WHERE ID BETWEEN {id} AND ({id} + 10)"
        cursor.execute(sql)
        registres = cursor.fetchall()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        sql = "INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s)"
        val = (pelicula.titol,pelicula.any,pelicula.puntuacio,pelicula.vots)
        cursor.execute(sql, val)
        self._conn.commit()
        print("PELICULA INSERTADA")
        return pelicula
    
    def llegeix(self, any: int) ->  List[Pelicula]:
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT * FROM PELICULA WHERE ANYO = {any}")
        registres = cursor.fetchall()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
        
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        cursor.execute(f"""UPDATE PELICULA
                       SET TITULO = '{pelicula.titol}', ANYO = {pelicula.any}, PUNTUACION = {pelicula.puntuacio}, VOTOS = {pelicula.vots}
                       WHERE ID = {pelicula.id}""")
        self._conn.commit()
        print(f"S'HA ACTUALITZAT LA PELICULA {pelicula.id}")
        return pelicula
