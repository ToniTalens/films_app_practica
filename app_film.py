#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
import logging
from persistencia_pelicula_postgresql import Persistencia_pelicula_postgresql
import psycopg

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
RUTA_FITXER_POSTGRESQL = os.path.join(THIS_PATH, 'configuracioPostgresql.yml')
print(RUTA_FITXER_CONFIGURACIO)
print(RUTA_FITXER_POSTGRESQL)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

#Creació del get_configuracio per postgre
def get_conf_postgre(ruta_fitxer_postgresql) -> dict:
    config = {}
    with open(ruta_fitxer_postgresql, 'r') as conn:
        config = yaml.safe_load(conn)
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

#Persistencies per postgre, només he modificat el nom del diccionari i el dbname
def get_persistencies_postgresql(conn: dict) -> dict:
    credencials = {}
    if conn["base de dades"]["motor"].lower().strip() == "postgresql":
        credencials['host'] = conn["base de dades"]["host"]
        credencials['user'] = conn["base de dades"]["user"]
        credencials['password'] = conn["base de dades"]["password"]
        credencials['dbname'] = conn["base de dades"]["dbname"]
        return {
            'pelicula': Persistencia_pelicula_postgresql(credencials)
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

#Totes les opcions del menú, realment ho podria haver fet només amb aquest mètode, no es necessari el mostra_menu_next10()
def mostra_menu():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")
    print("2.- Mostra les següents 10 pel·lícules (Només si ja has escollit la primera opció)")
    print("3.- Insereix una nova pel·lícula")
    print("4.- Modifica una pel·lícula existent")
    print("5.- Consulta totes les pel·lícules")
    print("6.- Consulta totes les pel·lícules per any")
    

#Les mateixes opcions del menú
def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")
    print("2.- Mostra les següents 10 pel·lícules (Només si ja has escollit la primera opció)")
    print("3.- Insereix una nova pel·lícula")
    print("4.- Modifica una pel·lícula existent")
    print("5.- Consulta totes les pel·lícules")
    print("6.- Consulta totes les pel·lícules per any")

#He afegit opcions per poder fer les consultes
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

#He creat un database per cada tipus de consulta i per cada tipus de base de dades
def database_read(id:int=None, context:dict=None, any:int= None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(id=id, context=context, any=any)
    return films

def database_read_postgre(id:int=None, context:dict=None, any:int= None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_conf_postgre(RUTA_FITXER_POSTGRESQL)
    persistencies = get_persistencies_postgresql(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(id=id, context=context, any=any)
    return films

def database_insert(context:dict=None, peli:list=None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(context=context, peli=peli)
    return films

def database_insert_postgre(context:dict=None, peli:list=None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_conf_postgre(RUTA_FITXER_POSTGRESQL)
    persistencies = get_persistencies_postgresql(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(context=context, peli=peli)
    return films

def database_update(context:dict=None, titol:str=None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(context=context, titol=titol)
    return films

def database_update_postgre(context:dict=None, titol:str=None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_conf_postgre(RUTA_FITXER_POSTGRESQL)
    persistencies = get_persistencies_postgresql(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies["pelicula"]
    )
    films.llegeix_de_disc(context=context, titol=titol)
    return films

#Dins del bucle pots escollir quin tipus de consulta vols fer i, a més a més, dins de cada tipus de consulta, pots escollir quina base de dades
#vols per fer la consulta
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
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            if base == "1":
                idmysql = int(input("Introdueix el id: (mysql)"))
                films = database_read(id=idmysql, context=context)
                context["llistapelis"] = films
            elif base == "2":
                idpost = int(input("Introdueix el id: (mysql)"))
                films = database_read_postgre(id=idpost, context=context)
                context["llistapelis"] = films

        elif context["opcio"] == '2':
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            if base == "1":
                idmysql+=10
                films = database_read(id=idmysql, context=context)
                context["llistapelis"] = films
            elif base == "2":
                idpost+=10
                films = database_read_postgre(id=idpost, context=context)
                context["llistapelis"] = films

        elif context["opcio"] == '3':
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            titol = input("Nom de la pel·lícula: ")
            anyo = int(input("Any de publicació: "))
            puntuacio = float(input("Puntuació: "))
            vots = int(input("Vots: "))
            peli=[]
            peli.append(titol), peli.append(anyo), peli.append(puntuacio), peli.append(vots)
            if base == "1":
                films = database_insert(context=context, peli=peli)
                context["llistapelis"] = films
            elif base == "2":
                films = database_insert_postgre(context=context, peli=peli)
                context["llistapelis"] = films

        elif context["opcio"] == '4':
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            titol = input("Introdueix el nom de la pel·lícula que vols modificar: ")
            if base == "1":
                films = database_update(context=context, titol=titol)
                context["llistapelis"] = films
            elif base == "2":
                films = database_update_postgre(context=context, titol=titol)
                context["llistapelis"] = films
        elif context["opcio"] == '5':
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            if base == "1":
                films = database_read(context=context)
                context["llistapelis"] = films
            elif base == "2":
                films = database_read_postgre(context=context)
                context["llistapelis"] = films
        elif context["opcio"] == '6':
            base=input("Amb quina base de dades vols treballar? mysql[1] o postgresql[2] ")
            any = input("Introdueix l'any per consultar les pel·lícules que hi van sortir: ")
            if base == "1":
                films = database_read(context=context, any=any)
                context["llistapelis"] = films
            elif base == "2":
                films = database_read_postgre(context=context, any=any)
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
