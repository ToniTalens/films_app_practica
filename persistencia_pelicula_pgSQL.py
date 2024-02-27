#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import psycopg
import logging

class Persistencia_pelicula_pgSQL(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = psycopg.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                dbname=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        with self._conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM PELICULA;""")

        return True
    
    def count(self) -> int:
        with self._conn.cursor() as cursor:
            query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
            cursor.execute(query)
            count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        with self._conn.cursor() as cursor:
            query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
            cursor.execute(query)
            registres = cursor.fetchall()
            cursor._reset()
            resultat = []
            for registre in registres:
                pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        if id==None:
            sql='SELECT * FROM PELICULA LIMIT 10'
        else:
            sql=f'select * from PELICULA WHERE id>{id} LIMIT 10'

        list = []
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            for x in cursor.fetchall():
                pelicula = Pelicula(x[1],x[2],x[3],x[4],self,x[0])
                list.append(pelicula)
            cursor._reset()
        return list
    
    def desa(self,pelicula:Pelicula):
        sql = f"INSERT INTO PELICULA(titulo,anyo,puntuacion,votos) VALUES ('{pelicula.titol}',{pelicula.any},{pelicula.puntuacio},{pelicula.vots})"
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()

    
    def llegeix(self, any: int) -> list:
        sql=f"SELECT * FROM PELICULA WHERE anyo={any}"
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            fin=[]
            peliculaSel = cursor.fetchall()
            for x in peliculaSel:
                dict={}
                dict["id"] = x[0]
                dict["titulo"]=x[1]
                dict["anyo"]=x[2]
                dict["puntuacion"]=x[3]
                dict["votos"]=x[4]
                fin.append(dict)
        return fin

    def canvia(self,pelicula:Pelicula):
        sql = f"UPDATE PELICULA SET titulo = '{pelicula.titol}',anyo = {pelicula.any},puntuacion = {pelicula.puntuacio}, votos = {pelicula.vots} WHERE id={pelicula.id}"
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()
