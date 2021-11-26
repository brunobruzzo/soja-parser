#! /usr/bin/env python3. 

# SojaParser.py - Recolecta los precios diarios de la soja de la Bolsa de Comercio de Rosario.
import requests, bs4, time, datetime, re


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
    res = requests.get('https://www.cac.bcr.com.ar/es/precios-de-pizarra/consultas?product=13&type=pizarra&date_start=' + date_format + '&date_end=' + date_format + '&year=&month=&period=day&op=Filtrar')
    res.raise_for_status()
    rosario_soup = bs4.BeautifulSoup(res.text, features="html.parser")
    soja_date = rosario_soup.find_all("td", class_="text-center")       # Recopila la fecha de la cotizacion en una string
    if soja_date is not None and len(soja_date) > 0:
            soja_date_text = soja_date[0].getText()
    else:
        continue
    soja_date_text = soja_date[0].getText()
    soja_date_regex = re.compile(r'\S+') # Limpia la string de la fecha de space bars)
    sorex_date = soja_date_regex.findall(soja_date[0].getText())
    print(soja_date_text)
    precio = soja_date.find_next_sibling("td")
    print(precio)
    soja_price = rosario_soup.find_all("td", class_="text-center")   # Recopila el precio de la soja
    soja_price_text = soja_price[0].getText() 
    # print(soja_price_text.strip())
    soja_regex = re.compile(r'\S\s\S+|S+') # limpia la string del precio de space bars
    sorex = soja_regex.findall(soja_price_text)
    #print('En la fecha ' + sorex_date[0] + ' la soja vale:' + sorex[0])     # Imprime las cotizaciones. 
    print(soja_price)
   # TODO: copiar los valores a diccionario y a CSV file.

print('loop ends here')
