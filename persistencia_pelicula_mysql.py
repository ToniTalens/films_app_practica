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
    
    def totes_pag(self, pagina: int, tamany_pagina: int = 10) -> List[Pelicula]:
        print(f"Recuperando películas para la página {pagina}...")
        cursor = self._conn.cursor(buffered=True)
        # Cálculo del índice inicial y final basado en la página y tamaño de página
        index_inicial = (pagina - 1) * tamany_pagina
        index_final = index_inicial + tamany_pagina

        # Consulta SQL con cláusula LIMIT para obtener solo los resultados de la página actual
        query = f"SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA LIMIT {index_inicial}, {tamany_pagina};"
        cursor.execute(query)

        registros = cursor.fetchall()
        cursor.close()

        resultado = []
        for registro in registros:
            pelicula = Pelicula(registro[1], registro[2], registro[3], registro[4], self, registro[0])
            resultado.append(pelicula)

        # Agrega las películas a la lista _pelicules de la instancia de Llistapelis
        if self._llistapelis is not None:
            self._llistapelis.pelicules.extend(resultado)

        print(f"Películas recuperadas: {resultado}")
        return resultado




    
    def desa(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        # Consulta SQL para insertar una nueva película
        query = "INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES (%s, %s, %s, %s);"
        values = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots)
        cursor.execute(query, values)
        self._conn.commit()
        cursor.reset()
        
        # Actualizamos el objeto Pelicula con el ID asignado por la base de datos
        pelicula._id = cursor.lastrowid

        return pelicula
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        # Consulta SQL para recuperar películas de un año específico
        query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE anyo = %s;"
        values = (any,)
        cursor.execute(query, values)
        registres = cursor.fetchall()
        cursor.reset()

        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)

        return resultat
    
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        # Consulta SQL para actualizar una película existente
        query = "UPDATE PELICULA SET titulo=%s, anyo=%s, puntuacion=%s, votos=%s WHERE id=%s;"
        values = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(query, values)
        self._conn.commit()
        cursor.reset()

        return pelicula
    
