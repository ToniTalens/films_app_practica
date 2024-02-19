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
        input6 = input("Nom de la pel·lícula: ")
        comprovacio = existeix(input6)
        input7 = int(input("Any de publicació: "))
        input8 = float(input("Puntuació: "))
        input9 = int(input("Vots: "))
        query = "INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s);"
        #modificar =(input5, input7, input8, input9)
        #cursor.execute(query, modificar)
    
    def llegeix(self, any: int) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id, titulo, anyo, puntuacion, votos from PELICULA WHERE anyo = '%s';"
        cursor.execute(query, any)
        registres = cursor.fetchall()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        pass
        #falta codi
    
    
