#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from persistencia_pelicula_postgresql import Persistencia_pelicula_postgresql
from llistapelis import Llistapelis
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)
credencials = {
    "host": "localhost",
    "user": "dam_app",
    "password": "1234",
    "database": "pelis"
}

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
        print(credencials)
        return {
            'persistencia': Persistencia_pelicula_mysql(credencials)
        }
    elif conf["base de dades"]["motor"].lower().strip() == "postgresql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        print(credencials)
        return {
            'persistencia': Persistencia_pelicula_postgresql(credencials)
        }
    else:
        return {
            'persistencia': None
        }
    
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()


def landing_text():
    os.system('clear')
    print("Benvingut a la app de pel·lícules")
    time.sleep(1)
    msg = "Desitjo que et sigui d'utilitat!"
    mostra_lent(msg)
    input("Prem la tecla 'Enter' per a continuar")
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
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")


def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)['persistencia']
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.llegeix_de_disc(id)
    return films

def bucle_principal(context):
    opcio = None
    persistencia = Persistencia_pelicula_mysql(credencials)
    mostra_menu()

    id = 0
    firstOption = False
    while opcio != '0':
        if firstOption:
            mostra_menu_next10() 
        opcio = input("Introdueix una opció: ")
        context["opcio"] = opcio
        
        
        if context["opcio"] == '1':
            firstOption = True
            films = database_read(id)
            context["llistapelis"] = films
            id += 10

        elif context["opcio"] == '2':
            films = database_read(id)
            context['llistapelis'] = films
            id += 10

        procesa_opcio(context)

        #falta codi


def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
