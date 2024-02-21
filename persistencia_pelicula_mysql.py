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
        consulta = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA"

        if id is not None:
            consulta += f" WHERE id > {id} ORDER BY id ASC LIMIT 10;"
        else:
            consulta += " ORDER BY id ASC LIMIT 10;"

        cursor.execute(consulta)
        resultats_consulta = cursor.fetchall()
        pag = []

        for resultat in resultats_consulta:
            pelicula = Pelicula(resultat[1],resultat[2],resultat[3],resultat[4],self,resultat[0])
            pag.append(pelicula)
            
        cursor.close()
        return pag

    
    def desa(self,pelicula:Pelicula) -> Pelicula:
        
        cursor = self._conn.cursor(buffered=True)
        consulta = "INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES (%s, %s, %s, %s);"
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
            pelicula = Pelicula(resultat[1],resultat[2],resultat[3],resultat[4], self, resultat[0])
            any.append(pelicula)
        cursor.close()
        return any
    
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        
        cursor = self._conn.cursor(buffered=True)
        consulta = "UPDATE PELICULA SET titulo=%s, anyo=%s, puntuacion=%s, votos=%s WHERE id=%s;"
        parametres = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(consulta, parametres)
        self._conn.commit()
        cursor.close()
        return pelicula
