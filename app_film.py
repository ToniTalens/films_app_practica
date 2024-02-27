#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from persistencia_pelicula_pgSQL import Persistencia_pelicula_pgSQL
from llistapelis import Llistapelis
import logging
from pelicula import Pelicula

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
RUTA_FITXER_CONFIGURACIOPGSQL = os.path.join(THIS_PATH, 'configuracio copy.yml') 
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
    elif conf["base de dades"]["motor"].lower().strip() == "psql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
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
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

def inserir(bd):
    pelicula = input("Introdueix el titol de la pelicula:\n")
    any = int(input("Introdueix l'any de la pelicula:\n"))
    puntuacio = float(input("Introdueix la puntuació:\n"))
    vots = int(input("Introdueix la quantitat de vots:\n"))
    inserir = Pelicula(pelicula,any,puntuacio,vots,"","")

    if(bd == "2"):
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIOPGSQL)
    else:
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
        
    persistencies = get_persistencies(la_meva_configuracio)
    bd = persistencies["pelicula"]
    bd.desa(inserir)


def mostra_seguents(llistapelicula):
    os.system('clear')

def update(bd):
    id = int(input("Inserta el ID de la pelicula que desitjes canviar:\n"))
    pelicula = input("Introdueix el titol de la pelicula:\n")
    any = int(input("Introdueix l'any de la pelicula:\n"))
    puntuacio = float(input("Introdueix la puntuació:\n"))
    vots = int(input("Introdueix la quantitat de vots:\n"))
    inserir = Pelicula(pelicula,any,puntuacio,vots,"",id)

    if(bd == "2"):
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIOPGSQL)
    else:
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)

    persistencies = get_persistencies(la_meva_configuracio)
    bd = persistencies["pelicula"]
    bd.canvia(inserir)
    
def buscar(bd):
    any = int(input("Introdueix l'any de la pelicula:\n"))

    if(bd == "2"):
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIOPGSQL)
    else:
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)

    persistencies = get_persistencies(la_meva_configuracio)
    bd = persistencies["pelicula"]
    pelis = bd.llegeix(any)
    mostra_lent(json.dumps(pelis,indent=4))
    print()

def mostra_menu():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")
    print("3.- Insertar una pelicula")
    print("4.- Modificar una pelicula")
    print("5.- Buscar pelicules per any")

def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "3": lambda ctx : inserir(ctx['bd']),
        "4": lambda ctx : update(ctx['bd']),
        "5": lambda ctx : buscar(ctx['bd'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int,bd):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)

    if(bd == "2"):
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIOPGSQL)
    else:
        la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)

    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies['pelicula']
    )
    films.llegeix_de_disc(id)
    return films

def bucle_principal(context):
    opcio = None
    escull_base_dades()
    bd = input()
    context["bd"] = bd
    context["opcio"]=-1
    os.system("clear")
    while opcio != '0': 
        if context["opcio"] != '1':     
            mostra_menu()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        
        if context["opcio"] == '1':
            id = None
            films = database_read(id,context["bd"])
            context["llistapelis"] = films

        elif context["opcio"] == '2':
            id = films.ult_id
            films = database_read(id,context["bd"])
            context["llistapelis"] = films
            context["opcio"] = '1'
        procesa_opcio(context)
        
        if context["opcio"]=='1':
            mostra_menu_next10()

def escull_base_dades():
    print("Escull quina base de dades vols utilitzar: ")
    print("1.MySQL")
    print("2.PostgreSQL")        


def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
