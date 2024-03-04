#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credencials)
        }
    elif conf["base de dades"]["motor"].lower().strip() == "postgres":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['db'] = conf["base de dades"]["db"]
        return {
            'pelicula': Persistencia_pelicula_postgres(credencials)
        }
    else:
        return {
            'pelicula': None
        }
    
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()


def landing_text():
    os.system('clear')
    print("Bienvenido/a a la aplicación de películas")
    time.sleep(1)
    msg = "¡Deseo que te sea útil!"
    mostra_lent(msg)
    input("Presiona la tecla 'Enter' para continuar")
    os.system('clear')

def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()

def mostra_llista(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

def mostra_seguents(llistapelicula):
    os.system('clear')


def mostra_menu():
    print("0.- Salir de la aplicación.")
    print("1.- Mostrar las primeras 10 películas")
    print("2.- Mostrar las siguientes 10 próximas películas")
    print("3.- Contar todas las películas de la base de datos")
    print("4.- Mostrar todas las películas")
    print("5.- Insertar una nueva película")
    print("6.- Recuperar las películas de un año determinado")
    print("7.- Modificar una película de la base de datos.")


def mostra_menu_next10():
    print("0.- Salir de la aplicación.")
    print("2.- Mostrar las siguientes 10 películas")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Hasta la próxima"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("¡Opción incorrecta!"))(context)

def database_read(id:int):
    logging.basicConfig(filename='peliculas.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio("configuracio.yml")
    persistencies = la_meva_configuracio["motor"]
    films = Llistapelis(
        persistencia_pelicula = persistencies
    )
    films.llegeix_de_disc(id)
    return films

def bucle_principal(context):
    opcio = None
    
    mostra_menu()

    while opcio != '0':
        opcio = input("Selecciona una opción: ")
        context["opcio"] = opcio
        
        if context["opcio"] == '1':
            id = None
            films = database_read(id)
            context["llistapelis"] = films

        elif context["opcio"] == '2':
            id = films.ult_id
            films = database_read(id)
            films.pelicules.extend(films.pelicules)

        elif context["opcio"] == '3':
            Persistencia_pelicula_mysql.count()

        elif context["opcio"] == '4':
            Persistencia_pelicula_mysql.totes()

        elif context["opcio"] == '5':
            title = input("Introduce el título : ")
            anyo = input("Introduce el año de la nueva película : ")
            score = input("Introduce la puntuación de la nueva película : ")
            votes = input("Introduce los votos de la nueva película : ")
            Persistencia_pelicula_mysql.desa(title,anyo,score,votes)

        elif context["opcio"] == '6':
            year = input("Introduce el año : ")
            Persistencia_pelicula_mysql.llegeix(year)

        elif context["opcio"] == '7':
            id_to_update = input("Introduce el id de la película a editar : ")
            new_title = input("Introduce el título actualizado de la nueva película : ")
            new_anyo = input("Introduce el año de la nueva película : ")
            new_score = input("Introduce la puntuación de la nueva película : ")
            new_votes = input("Introduce los votos de la nueva película : ")
            Persistencia_pelicula_mysql.canvia(new_title,new_anyo,new_score,new_votes,id_to_update)
  
        procesa_opcio(context)


def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
