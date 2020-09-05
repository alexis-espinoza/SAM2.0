import json
from modelos import Serie, Pelicula, Manga
from os import getcwd, system


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

    #Agregar mensajes customizados para estas clases
    def obtener_logs(self):

        try:
            with open(str(getcwd())+'\\LOGS\\historial.txt','r') as archivo_de_logs:
	            list_registros_log =  list(filter(lambda linea: linea!='\n', archivo_de_logs.readlines()))
            return list_registros_log[3:]
        except Exception:
                system('cls')
                print('\n¡La opeación en curso produjo errores!')    


    def actualizar_logs(self, lista_de_logs):
        try:
            with open(str(getcwd())+'\\LOGS\\historial.txt','w') as archivo_de_logs:
                encabezado =" _____         ________________\n|FECHA|       |ACCIÓN REALIZADA|\n'''''''       ''''''''''''''''''\n"
                archivo_de_logs.write(encabezado)
                archivo_de_logs.writelines(lista_de_logs)    
        except Exception:
                  system('cls')
                  print('\n¡La opeación en curso produjo errores!')  
