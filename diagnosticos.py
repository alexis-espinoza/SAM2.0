
import os
from os import getcwd, system
import json
import time


def leer_registros():
   with open(str(getcwd())+'\\series_peliculas.json','r') as archivo:
            data_json = json.load(archivo)       
   return data_json

   
def contar_registros_con_generos():

   try:
      data_actual = leer_registros()
      cont_sin_generos=0
      cont_con_generos=0
      con_peliculas=0
      for registro in data_actual["series"]:
        if(registro["generos"] == []):
            print(f'{registro["indice"]}-{registro["nombre"]}')
            cont_sin_generos+=1
        else:
         if("aventura" in registro["generos"]):
            print(f'{registro["indice"]}-{registro["nombre"]}')      
         cont_con_generos+=1
            #print(f'{registro["indice"]}-{registro["nombre"]}')
      print(f"\n{'-'*40}\n\tTOTAL SIN generos registrados: {cont_sin_generos}")
      print(f"\n{'-'*40}\n\tTOTAL CON generos registrados: {cont_con_generos}")
   except Exception as e:
      system('cls')
      print('\n¡No se pudo ejecutar!\n', e)


def mostrar_series_peliculas():
  # try:
      data_actual = leer_registros()
      for registro in data_actual["series"]:
         flag=False
         for pelicula in data_actual["peliculas"]:
           if(registro["indice"] == pelicula["id_serie"]):
               flag = True
               if(flag==True):
                  print(f'\n{registro["indice"]}-{registro["nombre"]}')
                  flag = False
               print(f'{pelicula["indice"]}-{pelicula["nombre"]}')                    
   #except Exception as e:
    #  system('cls')
     # print('\n¡No se pudo ejecutar!\n', e)
    
      
contar_registros_con_generos()
#mostrar_series_peliculas()
input()
   

   


