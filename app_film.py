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
    print("3.- Insereix una nova pel·lícula")
    print("4.- Modifica una pel·lícula existent")
    print("5.- Consulta totes les pel·lícules")
    print("6.- Consulta totes les pel·lícules per any")
    


def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")
    print("3.- Insereix una nova pel·lícula")
    print("4.- Modifica una pel·lícula existent")
    print("5.- Consulta totes les pel·lícules")
    print("6.- Consulta totes les pel·lícules per any")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis']),
        "3": lambda ctx : mostra_llista(ctx['llistapelis']),
        "4": lambda ctx : mostra_llista(ctx['llistapelis']),
        "5": lambda ctx : mostra_llista(ctx['llistapelis']),
        "6": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int=None, context=None, any:int = None) -> None:
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    
    if context["opcio"] == '1':
        films.llegeix_de_disc(id, context)
    elif context["opcio"] == '2':
        films.llegeix_de_disc(id, context)
    elif context["opcio"] == '3':
        films.llegeix_de_disc(context)
    elif context["opcio"] == '4':
        films.llegeix_de_disc(context)
    elif context["opcio"] == '5':
        films.llegeix_de_disc(context)
    elif context["opcio"] == '6':
        films.llegeix_de_disc(context, any)

    return films

def bucle_principal(context):
    opcio = None
    
    mostra_menu()
    a = 0

    while opcio != '0':
        if a is not 0:
            mostra_menu_next10()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        
        if context["opcio"] == '1':
            #id = None
            id = int(input("Introdueix el id: "))
            films = database_read(id, context)
            context["llistapelis"] = films

        elif context["opcio"] == '2':
            id+=10
            films = database_read(id, context)
            context["llistapelis"] = films
        
        elif context["opcio"] == '3':
            films = database_read(context)
            context["llistapelis"] = films

        elif context["opcio"] == '4':
            films = database_read(context)
            context["llistapelis"] = films

        elif context["opcio"] == '5':
            films = database_read(context)
            context["llistapelis"] = films

        elif context["opcio"] == '6':
            any = int(input("Introdueix l'any per consultar les pel·lícules que hi van sortir: "))
            films = database_read(context, any)
            context["llistapelis"] = films
        procesa_opcio(context)
        a += 1

def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
