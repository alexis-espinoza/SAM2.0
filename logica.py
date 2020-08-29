from acc_datos import Gestor_de_series
from modelos import Serie

class Coordinador_de_series:

    def listar_registos(self):
        return Gestor_de_series.obtener_registros()

    
    def listado_general(self, opcion_de_listado):
        coordinador = Coordinador_de_series()
        dicc_listados = {
        1: listar_todos,
        2: listar_series,
        3: listar_series_en_proceso,
        4: listar_peliculas,
        5: listar_series_por_rango,
        6: listar_peliculas
        }

    def listar_todos(self):
        return True

     def listar_series(self):
        return Gestor_de_series().obtener_series()

    def listar_series_en_proceso(self):
        return list(map(lambda Serie: Serie.mostrar_min(), Gestor_de_series().obtener_series()))
    
    def listar_series_en_espera(self):
        return True

    def listar_series_por_rango(self):
        return True
    def listar_peliculas(self):
        return Coordinador_de_series.obtener_peliculas()
    
    def listar_mangas(self):
        return Coordinador_de_series.obtener_mangas()    

    