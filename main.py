from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from pelicula import Pelicula
from typing import List
import mysql.connector
import logging

logging.basicConfig(filename="pelicules.log", encoding="utf-8", level=logging.DEBUG)
credencials = {
    "host": "localhost",
    "user" : "dam_app",
    "password" : "1234",
    "database" : "pelis"
}

pers_pelis = Persistencia_pelicula_mysql(credencials)

p = Pelicula("La sociedad sin nieve 3", 2010, 5.0, 10000, pers_pelis, 1712)
print(pers_pelis.canvia(p))
