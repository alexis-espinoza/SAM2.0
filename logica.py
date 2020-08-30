from acc_datos import Gestor_de_series
from modelos import Serie
from os import system
import time

class Coordinador_de_series:

    def __init__(self):
         self.dicc_dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves','Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
    
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

    def listar_series_del_dia(self):

        lista_de_registros = Gestor_de_series().obtener_series()
        dia_de_hoy=time.strftime("%A",time.localtime())
        series_del_dia=''
        encabezado='\nSeries en emisión hoy ['+self.dicc_dias.get(dia_de_hoy)+']\n\n'
        
        
        for registro_actual in lista_de_registros:
            if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia_de_hoy)):
                series_del_dia+=registro_actual.mostrar_min()
        if(series_del_dia!=''):
                return(encabezado + series_del_dia)
        else:
            return ''

    def listar_series_por_emision(self):

        lista_de_registros =Gestor_de_series().obtener_series()
        registros_en_dia_actual=''
        salida=''
        registros_en_emision=0
        for dia in list(self.dicc_dias.keys()):
            for registro_actual in lista_de_registros:
                                        
                if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia)):
                    registros_en_dia_actual+=registro_actual.mostrar_min()
                    registros_en_emision+=1

            if(registros_en_dia_actual!=''):
                    salida+=self.dicc_dias.get(dia)+':\n'+registros_en_dia_actual+'\n'
                    registros_en_dia_actual=''

        if(salida!=''):
                conteo='\nCantidad de registros [en emisión]: '+str(registros_en_emision)
                return(salida+conteo)
        else:
                system('cls')
                return('\n¡No existen registros!')
    


    