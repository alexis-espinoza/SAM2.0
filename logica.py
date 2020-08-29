from acc_datos import Gestor_de_series
from modelos import Serie
from os import system

class Coordinador_de_series:

    def listar_registos(self):
        return Gestor_de_series.obtener_registros()

    
    def listado_general(self, opcion_de_listado):
        #try:
            system('cls')
            coordinador = Coordinador_de_series()
            dicc_listados = {
            1: coordinador.listar_todos,
            2: coordinador.listar_series,
            3: coordinador.listar_series_en_proceso,
            4: coordinador.listar_series_en_espera,
            5: coordinador.listar_series_por_rango,
            6: coordinador.listar_peliculas}

            return dicc_listados.get(opcion_de_listado)()
        #except Exception:
         #   print('\n¡No se seleccionó una opción de listado válida!')
          #  return False

    def listar_todos(self):
        return True

    def listar_series(self):
        return (Gestor_de_series().obtener_series(), False)

    def listar_series_en_proceso(self):
        return (list(filter(lambda Serie: Serie.get_estado()=='en proceso', Gestor_de_series().obtener_series())),'en proceso')
    
    def listar_series_en_espera(self):
        return (list(filter(lambda Serie: Serie.get_estado()=='en espera', Gestor_de_series().obtener_series())), 'en espera')

    def listar_series_por_rango(self):
        return True

    def listar_peliculas(self):
        return (Gestor_de_series().obtener_peliculas(),False)
    
    def listar_mangas(self):
        return Gestor_de_series.obtener_mangas()    

    