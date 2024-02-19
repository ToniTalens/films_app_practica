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
        pass
        #falta codi
    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        
        cursor = self._conn.cursor(buffered=True)
        consulta = "INSERT INTO PELICULA (titol, anyo, puntuacio, vots) VALUES (%s, %s, %s, %s);"
        parametres = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
        cursor.execute(consulta, parametres)
        self._conn.commit()
        cursor.close
        return pelicula
        
    
    def llegeix(self, any: int) -> Pelicula:
        
        cursor = self._conn.cursor(buffered=True)
        consulta = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE anyo = %s;"
        parametres = (pelicula.any)
        cursor.execute(consulta, parametres)
        resultats_consulta = cursor.fetchall()
        any = []
        for resultat in resultats_consulta:
            pelicula = Pelicula(resultat[0],resultat[1],resultat[2],resultat[3],resultat[4])
            any.append(pelicula)
        cursor.close()
        return any
    
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        
        cursor = self._conn.cursor(buffered=True)
        consulta = "UPDATE PELICULA SET titol=%s, anyo=%s, puntuacio=%s, vots=%s WHERE id=%s;"
        parametres = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(consulta, parametres)
        self._conn.commit()
        cursor.close()
        return pelicula
