#! /usr/bin/env python3. 

# SojaParser.py - Recolecta los precios diarios de la soja de la Bolsa de Comercio de Rosario.
import requests, bs4, time, datetime, re


web = requests.get("https://www.cac.bcr.com.ar/es/precios-de-pizarra/consultas?product=13&type=pizarra&date_start=2021-11-23&date_end=2021-11-24&year=&month=&period=day&op=Filtrar")
web.raise_for_status()
rosario_soup = bs4.BeautifulSoup(web.text, features="html.parser")
seccion_tabla = rosario_soup.find_all("td", class_="text-center")
seccion_tabla_fecha = seccion_tabla[0].getText()
seccion_tabla_precio = seccion_tabla[1].getText()
#print(seccion_tabla_fecha.strip())
#print(seccion_tabla_precio.strip())
