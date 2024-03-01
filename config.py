import psycopg2
import yaml

with open('configuracionPS.yml', 'r') as file:
    configuracion_bd = yaml.safe_load(file)

try:
    conn = psycopg2.connect(
        host=configuracion_bd["base_de_datos"]["host"],
        user=configuracion_bd["base_de_datos"]["user"],
        password=configuracion_bd["base_de_datos"]["password"],
        database=configuracion_bd["base_de_datos"]["database"]
    )
    print("Conexión exitosa a PostgreSQL")
except psycopg2.Error as e:
    print("Error al conectar a PostgreSQL:", e)
