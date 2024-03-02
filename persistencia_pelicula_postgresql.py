#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import logging
import psycopg

class Persistencia_pelicula_postgresql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = psycopg.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                dbname=credencials["dbname"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM PELICULA;")
        cursor._reset()
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor()
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    #Retorna totes les pelicules
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = "select * from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor._reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    #Retorna de 10 en 10
    def totes_pag(self, id) -> List[Pelicula]:
        cursor = self._conn.cursor()
        if id is None:
            query = "SELECT * FROM PELICULA LIMIT 10;"
            cursor.execute(query)
            registres = cursor.fetchall()
            cursor._reset()
            resultat = []
            for registre in registres:
                pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                resultat.append(pelicula)
        else:
            query = f"SELECT * FROM PELICULA WHERE id >= '{id}' LIMIT 10;"
            cursor.execute(query)
            registres = cursor.fetchall()
            cursor._reset()
            resultat = []
            for registre in registres:
                pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                resultat.append(pelicula)
        return resultat
    #fa un insert, si la pel·lícula ja existeix, dona la possibilitat de tornar-ho a intentar
    #tantes vegades com volguis, afeguin una nova pel·lícula
    def desa(self,pelicula:Pelicula):
        a=0
        while True:
            if a != 0:
                titol=input("Introdueix el nom de la pel·lícula que vols inserir dins la base de dades: ")
                any = int(input("Introdueix l'any: "))
                puntuacio=float(input("Puntuació: "))
                vots = int(input("Vots totals: "))
                pelicula = Pelicula(titol, any, puntuacio, vots, self)
                
            cursor = self._conn.cursor()
            query = "SELECT TITULO FROM PELICULA WHERE TITULO = %s;"
            cursor.execute(query, (pelicula.titol,))
            myresult = cursor.fetchone()
            cursor._reset()
            if myresult:
                print("Ho sento, aquesta pel·lícula ja està dins de la base de dades. ")
                a+=1
            else:
                #Com a la base de dades no se li va afegir serial, he de buscar l'ùltim id manualment
                #passar la tupla a un string, i finalment passar-ho a un int, treient-li els () i , i sumar-li 1
                query2 = "SELECT id FROM PELICULA ORDER BY id DESC LIMIT 1;"
                cursor.execute(query2)
                registres = cursor.fetchall()
                idStr = str(registres[0])
                idFinal = int(idStr.strip('(,)')) + 1
                query = "INSERT INTO PELICULA (ID, TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s, %s);"
                pel = (idFinal, pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
                cursor.execute(query, pel)
                self._conn.commit()
                #Aquest consulta és per poder veura com s'ha afegit correctament
                cursor.execute("SELECT * FROM PELICULA ORDER BY ID desc LIMIT 1;")
                registres = cursor.fetchall()
                cursor._reset()
                peli=[]
                for p in registres:
                    pelicula = Pelicula(p[1],p[2],p[3],p[4],self,p[0])
                    peli.append(pelicula)
                return peli
    
    #Llegeix per any
    def llegeix(self, any) -> list[Pelicula]:
        cursor = self._conn.cursor()
        query = f"SELECT * FROM PELICULA WHERE anyo = '{any}';"
        cursor.execute(query)  
        registres = cursor.fetchall()
        cursor._reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    #Se li passa un titol, comprova si existeix, i si es així, pot modificar-li 1 de les 3 opcions, l'any,
    #la puntuació o els vots, el id i el títol no te sentit modificar-los (així ho he considerat).
    def canvia(self,titol:str) -> Pelicula:
        a=0
        #També tens la oportunitat de tornar-ho a intentar per si la pel·lícula buscada no existeix
        while True:
            if a != 0:
                titol=input("Introdueix el nom de la pel·lícula que vols modificar dins la base de dades: ")
                
            cursor = self._conn.cursor()
            query = "SELECT * FROM PELICULA WHERE TITULO = %s;"
            cursor.execute(query, (titol,))
            myresult = cursor.fetchone()
            cursor._reset()
            if myresult:
                print("La pel·lícula existeix ")
                print(myresult)
                cursor = self._conn.cursor()
                modifica=input("Què vols modificiar de la pel·lícula? any[1], puntuació[2] o vots[3]")
                if modifica == "1":
                    any=int(input("Introdueix el nou any: "))
                    query = "UPDATE PELICULA set anyo = %s WHERE titulo = %s;"
                    cursor.execute(query, (any, titol,))
                    self._conn.commit()
                    query2="SELECT * FROM PELICULA WHERE titulo = %s"
                    cursor.execute(query2, (titol,))
                    registres = cursor.fetchall()
                    cursor._reset()
                    peli = []
                    for registre in registres:
                        pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                        peli.append(pelicula)
                    return peli
                elif modifica == "2":
                    puntuacio=float(input("Introdueix la nova puntuació: "))
                    query = "UPDATE PELICULA set puntuacion = %s WHERE titulo = %s;"
                    cursor.execute(query, (puntuacio, titol,))
                    self._conn.commit()
                    query2="SELECT * FROM PELICULA WHERE titulo = %s"
                    cursor.execute(query2, (titol,))
                    registres = cursor.fetchall()
                    cursor._reset()
                    peli = []
                    for registre in registres:
                        pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                        peli.append(pelicula)
                    return peli
                elif modifica == "3":
                    vots=int(input("Introdueix la nova quantitat de vots: "))
                    query = "UPDATE PELICULA set votos = %s WHERE titulo = %s;"
                    cursor.execute(query, (vots,titol,))
                    self._conn.commit()
                    query2="SELECT * FROM PELICULA WHERE titulo = %s"
                    cursor.execute(query2, (titol,))
                    registres = cursor.fetchall()
                    cursor._reset()
                    peli = []
                    for registre in registres:
                        pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
                        peli.append(pelicula)
                    return peli
            else:
                print("Ho sento, aquesta pel·lícula no està dins de la base de dades. ")
                a+=1