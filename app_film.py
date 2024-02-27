#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from persistencia_pelicula_pgSQL import Persistencia_pelicula_pgSQL
from llistapelis import Llistapelis
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
# Canviat de constant a variable per el menu
ruta_fitxer_configuracio = os.path.join(THIS_PATH, 'configuracio.yml') 
print(ruta_fitxer_configuracio)
def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    try:
        with open(ruta_fitxer_configuracio, 'r') as conf:
            config = yaml.safe_load(conf)
    except (FileNotFoundError):
        print(f"El fitxer: {ruta_fitxer_configuracio} no existeix")
    return config

def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = str(conf["base de dades"]["password"])
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credencials)
        }
    elif conf["base de dades"]["motor"].lower().strip() == "postgresql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = str(conf["base de dades"]["password"])
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_pgSQL(credencials)
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
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.001)

def mostra_seguents(llistapelicula):
    os.system('clear')


def mostra_menu():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")
    print("2.- Cerca pelicules per l'any")
    print("3.- Insereix una nova pel·licula")
    print("4.- Modificar una pel·licula existent")


def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    # if context["opcio"] == '0': return mostra_lent("Fins la propera")
    # elif context["opcio"] == '1': return mostra_llista(context["llistapelis"])
    # elif context["opcio"] == '2': return mostra_llista(context["llistapelis"])
    # else : return mostra_lent("opcio incorrecta!!!")
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(ruta_fitxer_configuracio)
    persistencies = get_persistencies(la_meva_configuracio)["pelicula"]
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.llegeix_de_disc(id)
    return films

#metode sense utilitzar
def database_readall(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(ruta_fitxer_configuracio)
    persistencies = get_persistencies(la_meva_configuracio)["pelicula"]
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.llegeix_de_disc(id)
    return films

#Metode que retorna films
def database_persistencia(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(ruta_fitxer_configuracio)
    persistencies = get_persistencies(la_meva_configuracio)["pelicula"]
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    return films

def bucle_principal(context):
    opcio = None
    try:
        fitxer = input("Escriu el nom exacte del fitxer de configuracio que vols utilitzar (incloent la extensió): ")
        global ruta_fitxer_configuracio 
        ruta_fitxer_configuracio = os.path.join(THIS_PATH, fitxer) 
        open(ruta_fitxer_configuracio, "rt")
    except (FileNotFoundError):
        print(f"No s'ha trobat el fitxer: {fitxer}")
        sys.exit(1)
        
    print(f"Fitxer {fitxer}")
    while opcio != '0':
        mostra_menu()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        
        if context["opcio"] == '1':
            id = 0
            films = database_read(id)
            context["llistapelis"] = films
            procesa_opcio(context)
            
            mostra_menu_next10()
            opcio = input("Selecciona una opció: ")
            context["opcio"] = opcio

            while context["opcio"] != '0':
                id = films.ult_id
                
                films = database_read(id)
                context["llistapelis"] = films
                procesa_opcio(context)

                mostra_menu_next10()
                opcio = input("Selecciona una opció: ")
                context["opcio"] = opcio

        elif context["opcio"] == '2':
            any = int(input("Escriu un any: "))
            id = None
            films = database_persistencia(id)
            films.llegeixPerAny(any)
            context["llistapelis"] = films
            

        elif context["opcio"] == '3':
            titol = input("Insereix el titol de la pel·licula: ")
            any = int(input("Insereix l'any de la pel·licula: "))
            puntuacio = float(input("Insereix la puntuacio de la pel·licula: "))
            vots = int(input("Insereix el numero de vots de la pel·licula: "))
            id = None
            films = database_persistencia(id)
            films.desa(titol, any, puntuacio, vots)
            context["opcio"] = opcio
            continue
            
        elif context["opcio"] == '4':
            id = int(input("Insereix el id de la pel·licula que vols modificar: "))
            titol = input("Insereix el titol de la pel·licula: ")
            any = int(input("Insereix l'any de la pel·licula: "))
            puntuacio = float(input("Insereix la puntuacio de la pel·licula: "))
            vots = int(input("Insereix el numero de vots de la pel·licula: "))
            films = database_persistencia(id)
            films.canvia(id, titol, any, puntuacio, vots)
            context["opcio"] = opcio
            continue
        
        procesa_opcio(context)

def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)

    (get_configuracio(ruta_fitxer_configuracio))


if __name__ == "__main__":
    main()
