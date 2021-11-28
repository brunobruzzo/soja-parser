#! /usr/bin/env python3. 

# SojaParser.py - Recolecta los precios diarios de la soja de la Bolsa de Comercio de Rosario.
import requests, bs4, time, datetime, re, Parser


# Crea variable con fecha de hoy
date = datetime.datetime.now()
date_limiter = datetime.datetime(2000, 1, 1)
delta = datetime.timedelta(days=1)

# TODO: Crear diccionario.
price_index = {}

print('loop begins here')
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
    print(seccion_tabla_fecha.strip())
    print(seccion_tabla_precio.strip())
print('loop ends here')

