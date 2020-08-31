import json
from modelos import Serie, Pelicula, Manga
from os import getcwd


class Gestor_de_series:

    def obtener_registros(self):
        lista_series = []
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
        lista_pelicuas = []
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)
            for pelicula_actual in data_json["peliculas"]:
                lista_pelicuas.append(Pelicula(pelicula_actual))
        return lista_pelicuas


    def obtener_mangas(self):
        lista_mangas = []
        with open(str(getcwd())+'\\DATA\\series_peliculas.json') as archivo:
            data_json = json.load(archivo)
            for manga_actual in data_json["mangas"]:
                lista_mangas.append(Pelicula(manga_actual))
        return lista_mangas

    
    def guardar_cambios(self, dicc_datos):
        with open(str(getcwd())+'\\DATA\\series_peliculas.json','w') as archivo:
            json.dump(dicc_datos, archivo, indent=3, ensure_ascii=False)

        