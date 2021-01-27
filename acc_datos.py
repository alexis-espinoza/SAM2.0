import json
from modelos import Serie, Pelicula, Manga
#from logica import Coordinador_de_alertas as alertas
import os
from os import getcwd, system


class Gestor_de_series:

    def obtener_avance_diario(self):
        try:
            os.startfile(str(getcwd())+'\\DATA\\proceso en series vistas.txt')
            system('cls')
        except Exception:
            return
  

    def obtener_registros(self):
      
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)       
        return data_json


    def obtener_series(self):
        lista_series = []
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)
            for serie_actual in data_json["series"]:
                lista_series.append(Serie(serie_actual))        
        return lista_series

    
    def obtener_peliculas(self):
        lista_peliculas = []
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)
            for pelicula_actual in data_json["peliculas"]:
                lista_peliculas.append(Pelicula(pelicula_actual))
        return lista_peliculas


    def obtener_mangas(self):
        lista_mangas = []
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)
            for manga_actual in data_json["mangas"]:
                lista_mangas.append(Manga(manga_actual))
        return lista_mangas


    def guardar_cambios(self, dicc_datos):
        with open(str(getcwd())+'\\DATA\\series_peliculas.json','w') as archivo:
            json.dump(dicc_datos, archivo, indent=3, ensure_ascii=False)


    def obtener_logs(self):

        try:
            with open(str(getcwd())+'\\LOGS\\historial.txt','r') as archivo_de_logs:
	            list_registros_log =  list(filter(lambda linea: linea!='\n', archivo_de_logs.readlines()))
            return list_registros_log[3:]
        except Exception:
            return



    def actualizar_logs(self, lista_de_logs):
        try:
            with open(str(getcwd())+'\\LOGS\\historial.txt','a') as archivo_de_logs:
                archivo_de_logs.write(lista_de_logs)    
        except Exception:
            return

    def guardar_lista(self,lista_de_registros):
        try:
            with open(str(getcwd())+'\\LOGS\\lista de series vistas.txt','w') as archivo_de_series_vistas:
                archivo_de_series_vistas.writelines(lista_de_registros)    
        except Exception:
            return
