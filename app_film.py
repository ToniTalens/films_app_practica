#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from persistencia_pelicula_postgres import Persistencia_pelicula_postgres
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
    print("Welcome to the movies app")
    time.sleep(1)
    msg = "I hope you find it useful !"
    mostra_lent(msg)
    input("Press the 'Enter' key to continue ")
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
    print("0.- Exit the application .")
    print("1.- Show the first 10 movies")
    print("2.- Show the next 10 movies")
    print("3.- Count all the movies in the datbase")
    print("4.- Show all the movies")
    print("5.- Inserts a new movie into the database")
    print("6.- Retrieves movies for a given year")
    print("7.- Modifies an existing movie in the database")

def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Until next time "),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], 
          lambda ctx : mostra_lent("Incorrect option !!!"))(context)


 #  Reads movies from the database with pagination.
def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(id)
    return films

def bucle_principal(context):
    opcio = None

    while opcio != '0':
        mostra_menu()
        opcio = input("Select an option : ")
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
            title = input("Enter title for a new movie : ")
            anyo = input("Enter year for a new movie : ")
            score = input("Enter score for a new movie : ")
            votes = input("Enter votes for a new movie : ")
            Persistencia_pelicula_mysql.desa(title,anyo,score,votes)

        elif context["opcio"] == '6':
            year = input("Enter the year : ")
            Persistencia_pelicula_mysql.llegeix(year)

        elif context["opcio"] == '7':
            id_to_update = input("Enter the id of movie to update : ")
            new_title = input("Enter updated title for the movie : ")
            new_anyo = input("Enter year for a new movie : ")
            new_score = input("Enter score for a new movie : ")
            new_votes = input("Enter votes for a new movie : ")
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

