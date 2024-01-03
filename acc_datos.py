import json
from modelos import Serie, Pelicula, Manga
#from logica import Coordinador_de_alertas as alertas
import os
from os import getcwd, system


class Gestor_de_series:

    def __init__(self) :
        self.encabezado = "_____         ________________\n|FECHA|       |ACCIÓN REALIZADA|\n'''''''       ''''''''''''''''''\n"

    def obtener_avance_diario(self):
        try:
            os.startfile(str(getcwd())+'/DATA/proceso en series vistas.txt',encoding='latin-1')
            system('clear')
        except Exception:
            return
  

    def obtener_registros(self):
      
        with open(str(getcwd())+'/DATA/series_peliculas.json',encoding='latin-1') as archivo:
            data_json = json.load(archivo)       
        return data_json


    def obtener_series(self):
        lista_series = []
        with open(str(getcwd())+'/DATA/series_peliculas.json',encoding='latin-1') as archivo:
            data_json = json.load(archivo)
            for serie_actual in data_json["series"]:
                lista_series.append(Serie(serie_actual))        
        return lista_series

    
    def obtener_peliculas(self):
        lista_peliculas = []
        with open(str(getcwd())+'/DATA/series_peliculas.json',encoding='latin-1') as archivo:
            data_json = json.load(archivo)
            for pelicula_actual in data_json["peliculas"]:
                lista_peliculas.append(Pelicula(pelicula_actual))
        return lista_peliculas


    def obtener_mangas(self):
        lista_mangas = []
        with open(str(getcwd())+'/DATA/series_peliculas.json',encoding='latin-1') as archivo:
            data_json = json.load(archivo)
            for manga_actual in data_json["mangas"]:
                lista_mangas.append(Manga(manga_actual))
        return lista_mangas


    def guardar_cambios(self, dicc_datos):
        try:
            with open(str(getcwd())+'/DATA/series_peliculas.json','w',encoding='latin-1') as archivo:
                json.dump(dicc_datos, archivo, indent=3, ensure_ascii=False)
            return False
        except Exception:
            return True
            #alertas.mostrar_mensaje("no_ok")


    def obtener_logs(self):

        try:
            with open(str(getcwd())+'/LOGS/historial.txt','r',encoding='latin-1') as archivo_de_logs:
	            list_registros_log =  list(filter(lambda linea: linea!='\n', archivo_de_logs.readlines()))
            return list_registros_log[3:]
        except Exception:
            return



    def agregar_nuevo_log(self, nuevo_registro_de_log):
        try:
            with open(str(getcwd())+'/LOGS/historial.txt','a',encoding='latin-1') as archivo_de_logs:
                archivo_de_logs.write(nuevo_registro_de_log)    
        except Exception:
            return

    def actualizar_historial(self, logs_validos):
        try:
            with open(str(getcwd())+'/LOGS/historial.txt','w',encoding='latin-1') as archivo_de_logs:
                archivo_de_logs.write(self.encabezado)
                archivo_de_logs.writelines(logs_validos)

        except Exception:
            return

    def guardar_lista(self,lista_de_registros):
        try:
            with open(str(getcwd())+'/LOGS/lista de series vistas.txt','w',encoding='latin-1') as archivo_de_series_vistas:
                archivo_de_series_vistas.writelines(lista_de_registros)    
        except Exception:
            return
