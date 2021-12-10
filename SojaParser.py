#! /usr/bin/env python3. 

# SojaParser.py - Recolecta los precios diarios de la soja de la Bolsa de Comercio de Rosario.
import requests, bs4, time, datetime, re, Parser, psycopg2
from configdb import configdb


# Crea variable con fecha de hoy
date = datetime.datetime.now()
date_limiter = datetime.datetime(2021, 10, 1)
delta = datetime.timedelta(days=1)
print("Variables de fecha creadas\n")

print('loop begins here\n')
while date > date_limiter:
# formatea la fecha para que sea compatible con al sintaxis de la URL de la bolsa de rosario.
    date_year = date.strftime('%Y')
    date_month = date.strftime('%m')
    date_day = date.strftime('%d')
    date_format = date_year + '-' + date_month + '-' + date_day
    # Retrocede un dia
    date = date - delta
    # print(date_format)
    web = requests.get('https://www.cac.bcr.com.ar/es/precios-de-pizarra/consultas?product=13&type=pizarra&date_start=' + date_format + '&date_end=' + date_format + '&year=&month=&period=day&op=Filtrar')
    web.raise_for_status()
    rosario_soup = bs4.BeautifulSoup(web.text, features="html.parser")
    seccion_tabla = rosario_soup.find_all("td", class_="text-center")
    if seccion_tabla is not None and len(seccion_tabla) > 0:
        seccion_tabla_fecha = seccion_tabla[0].getText()
        seccion_tabla_precio = seccion_tabla[1].getText()
    else:
        continue 
    seccion_tabla_fecha = seccion_tabla[0].getText()
    seccion_tabla_precio = seccion_tabla[1].getText()
    fecha_final = datetime.datetime.strptime(seccion_tabla_fecha.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
    precio_final = seccion_tabla_precio.strip().translate({ ord(c): None for c in ".$ " }).translate({ ord(c): "." for c in "," })
    print(fecha_final, precio_final,"\n")
    def insert_precio(fecha_final,precio_final):
        """ insert a new vendor into the vendors table """
        query = """INSERT INTO soja (fecha,precio)
                 VALUES(%s,%s) RETURNING *;"""
        conn = None
        try:
            params = configdb()
            print("Lectura de database configuration\n")
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            print("Conectados a la database\n")
            # create a new cursor
            cur = conn.cursor()
            # commit the changes to the database
            cur.execute(query, (fecha_final,precio_final))
            # read database configuration
            conn.commit()
            print("changes commited to db\n")
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    insert_precio(fecha_final, precio_final)
