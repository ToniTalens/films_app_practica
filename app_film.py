#!/usr/bin/python3

import os, yaml, sys, time, json
from pelicula import Pelicula

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
        credencials['password'] = str(conf["base de dades"]["password"])  

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


def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)






def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio('configuracio.yml')

    persistencies = get_persistencies(la_meva_configuracio)
    films = Llistapelis(
        persistencia_pelicula=persistencies['pelicula'])
    films.llegeix_de_disc(id)
    return films





def bucle_principal(context):
    pagina_actual = 1
    opcio = None

    while opcio != '0':
        mostra_menu()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio

        if context["opcio"] == '1' or context["opcio"] == '2':
            # Asegúrate de utilizar la instancia correcta de Llistapelis y de que persistencia_pelicula esté configurado
            films = context["llistapelis"].persistencia_pelicula.totes_pag(pagina_actual)
            context["llistapelis"].llista = films

            # Mostrem les pel·lícules
            mostra_llista(context["llistapelis"])

            # Incrementem la pàgina si s'ha seleccionat l'opció 2
            if context["opcio"] == '2':
                pagina_actual += 1






           

def main():
    context = {
        "llistapelis": None
    }
    landing_text()

    # Crear instancia de Llistapelis
    context["llistapelis"] = Llistapelis()

    # Obtener configuración y persistencias
    la_meva_configuracio = get_configuracio('configuracio.yml')
    persistencies = get_persistencies(la_meva_configuracio)

    # Asignar la instancia de Persistencia_pelicula_mysql a Llistapelis
    context["llistapelis"].persistencia_pelicula = persistencies['pelicula']

    bucle_principal(context)
    la_meva_configuracio = get_configuracio('configuracio.yml')

    persistencia_config = get_configuracio(RUTA_FITXER_CONFIGURACIO)["base de dades"]
    if persistencia_config["motor"].lower().strip() == "mysql":
        # Cargar configuración específica para MySQL
        persistencia_credenciales = {
            'host': la_meva_configuracio["base de dades"]["host"],
            'user': la_meva_configuracio["base de dades"]["user"],
            'password': str(la_meva_configuracio["base de dades"]["password"]),
            'database': persistencia_config["database"]
        }

        # Crear instancia de Persistencia_pelicula_mysql
        persistencia_mysql = Persistencia_pelicula_mysql(persistencia_credenciales)

        # Crear una nueva película y guardarla en la base de datos
        #nueva_pelicula = Pelicula("Nueva Película", 2022, 9.0, 100, persistencia_mysql,999)
        #persistencia_mysql.desa(nueva_pelicula)

        # Obtener todas las películas y mostrarlas
        #todas_las_peliculas = persistencia_mysql.totes()
        #print("Todas las películas:")
        #for pelicula in todas_las_peliculas:
        #    print(pelicula)

        # Obtener películas de un año específico y mostrarlas
        #peliculas_2022 = persistencia_mysql.llegeix(2022)
        #print(f"Películas del año 2022:")
        #for pelicula in peliculas_2022:
        #    print(pelicula)
    
   
if __name__ == "__main__":

    main()





