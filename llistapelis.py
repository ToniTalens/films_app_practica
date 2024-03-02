#!/bin/usr/python3

import json
from typing import List
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula

class Llistapelis():
    def __init__ (self, persistencia_pelicula: IPersistencia_pelicula) -> None:
        self._pelicules = []
        self._ult_id = 0
        self._persistencia_pelicula = persistencia_pelicula
        
    @property
    def pelicules(self) -> List[Pelicula]:
        return self._pelicules
    
    @property
    def ult_id(self) -> int:
        return self._ult_id

    @property
    def persistencia_pelicula(self) -> IPersistencia_pelicula:
        return self._persistencia_pelicula
    
    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        pelicules_dict = []
        for pelicula in self._pelicules:
            pelicules_dict.append(json.loads(pelicula.toJSON()))
        self_dict = {
            "pelicules": pelicules_dict
            }   
        return json.dumps(self_dict)
    #Depenent de la consulta aniràs a un mètode o un altre, independentment de si es mysql o postgresql (no afecta)
    def llegeix_de_disc(self,id:int=None, context=None, any=None, peli:list=None, titol:str=None):
        if context["opcio"] == '1':
            self._pelicules = self.persistencia_pelicula.totes_pag(id)
        elif context["opcio"] == '2':
            self._pelicules = self.persistencia_pelicula.totes_pag(id)
        elif context["opcio"] == '5':
            self._pelicules = self.persistencia_pelicula.totes()
        elif context["opcio"] == '3':
            pelicula = Pelicula(peli[0],peli[1],peli[2],peli[3],self)
            self._pelicules = self.persistencia_pelicula.desa(pelicula=pelicula)
        elif context["opcio"] == '4':
            self._pelicules = self.persistencia_pelicula.canvia(titol)
        elif context["opcio"] == '6':
            self._pelicules = self.persistencia_pelicula.llegeix(any)
