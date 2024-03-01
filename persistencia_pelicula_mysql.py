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
        query = "select * from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        if id is None:
            query = "SELECT * FROM PELICULA LIMIT 10;"
            cursor.execute(query)
            registres = cursor.fetchall()
            resultat = []
            for registre in registres:
                pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                resultat.append(pelicula)
        else:
            query = f"SELECT * FROM PELICULA WHERE id >= '{id}' LIMIT 10;"
            cursor.execute(query)
            registres = cursor.fetchall()
            resultat = []
            for registre in registres:
                pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                resultat.append(pelicula)
        return resultat
    
    def desa(self,pelicula:Pelicula):
        a=0
        while True:
            if a != 0:
                cont=input("Vols provar d'inserir una nova pel·lícula? [si] o [no] ")
                if cont == "si":
                    titol=input("Introdueix el nom de la pel·lícula que vols inserir dins la base de dades: ")
                    any = int(input("Introdueix l'any: "))
                    puntuacio=float(input("Puntuació: "))
                    vots = int(input("Vots totals: "))
                    pelicula = Pelicula(titol, any, puntuacio, vots, self)
                elif cont == "no":
                    return pelicula

            cursor = self._conn.cursor(buffered=True)
            query = "SELECT TITULO FROM PELICULA WHERE TITULO = %s;"
            cursor.execute(query, (pelicula.titol,))
            myresult = cursor.fetchone()
            cursor.reset()
            if myresult:
                print("Ho sento, aquesta pel·lícula ja està dins de la base de dades. ")
                a+=1
            else:
                query = "INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s);"
                pel = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
                cursor.execute(query, pel)
                self._conn.commit()
                cursor.execute("SELECT * FROM PELICULA ORDER BY ID desc LIMIT 1;")
                registres = cursor.fetchall()
                cursor.reset()
                peli=[]
                for p in registres:
                    pelicula = Pelicula(p[1],p[2],p[3],p[4],self,p[0])
                    peli.append(pelicula)
                return peli
    
    def llegeix(self, any) -> list[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = f"SELECT * FROM PELICULA WHERE anyo = '{any}';"
        cursor.execute(query)  
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def canvia(self,titol:str) -> Pelicula:
        a=0
        while True:
            if a != 0:
                cont=input("Vols modificar una pel·lícula? [si] o [no] ")
                if cont == "si":
                    titol=input("Introdueix el nom de la pel·lícula que vols inserir dins la base de dades: ")
                elif cont == "no":
                    return pelicula

            cursor = self._conn.cursor(buffered=True)
            query = "SELECT TITULO FROM PELICULA WHERE TITULO = %s;"
            cursor.execute(query, (pelicula.titol,))
            myresult = cursor.fetchone()
            cursor.reset()
            if myresult:
                cursor = self._conn.cursor(buffered=True)
                modifica=input("Què vols modificiar de la pel·lícula? any[1], puntuació[2] o vots[3]")
                if modifica == "1":
                    any=int(input("Introdueix el nou any: "))
                    query = "UPDATE PELICULA set anyo = %s WHERE titulo = %s;"
                    cursor.execute(query, (any, pelicula.titol,))
                    self._conn.commit()
                elif modifica == "2":
                    puntuacio=float(input("Introdueix la nova puntuació: "))
                    query = "UPDATE PELICULA set puntuacion = %s WHERE titulo = %s;"
                    cursor.execute(query, (puntuacio, pelicula.titol,))
                    self._conn.commit()
                elif modifica == "3":
                    vots=int(input("Introdueix la nova quantitat de vots: "))
                    query = "UPDATE PELICULA set votos = %s WHERE titulo = %s;"
                    cursor.execute(query, (vots, pelicula.titol,))
                    self._conn.commit()
                registres = cursor.fetchone()
                resultat = []
                for registre in registres:
                    pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                    resultat.append(pelicula)
                return resultat
            else:
                print("Ho sento, aquesta pel·lícula no està dins de la base de dades. ")
                a+=1
                
        
    
    
    
    

#    def existeix(self, input6):
#        cursor = self._conn.cursor(buffered=True)
#        query = "SELECT id, titulo, anyo, puntuacion, votos from PELICULA WHERE titulo = '%s';"
#        cursor.execute(query, input6)
#        myresult = cursor.fetchall()
#        return myresult
