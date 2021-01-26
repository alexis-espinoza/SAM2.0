
import os
import json
import time
import pyperclip
from os import system
from os import getcwd, system
from logica import Coordinador_de_series 
from logica import Coordinador_de_alertas as alertas
from modelos import Serie, Pelicula, Manga

class Principal:

    def menu(self):
        while True:
            #try:
                print(Coordinador_de_series().generar_dashboard())
                principal=Principal()
                opciones = '''0)- Getión de proceso\n1)- Agregar nuevo\n2)- Mostrar lista\n3)- Filtrar lista\n4)- Seleccionar serie\n5)- Seleccionar película\n6)- Seleccionar manga\n7)- Consultar bitácora\nDigite una opción: '''
                opcion_seleccionada = str(input(opciones)) 
                dicc_menu = {
                    '0': principal.abrir_diario,'1': principal.agregar_registro,'2': principal.listar_registros,
                    '3': principal.filtrar_lista,'4': principal.seleccionar_serie,'5': principal.seleccionar_pelicula,
                    '6': principal.seleccionar_manga,'7': principal.consultar_bitacora}
                system('cls')
                dicc_menu.get(opcion_seleccionada)()
            #except Exception:
               #alertas().mostrar_mensaje('def')

    def abrir_diario(self):
            Coordinador_de_series().mostrar_diario()


    def agregar_registro(self):
        opcion_ingreso =  str(input(f'\n{"-"*10}Opciones de registro{"-"*10}\n1)-Anime\n2)-Pelicula\n3)-Manga\nSeleccione una opción: '))
        coordinador = Coordinador_de_series()
        dicc_inserciones = {'1': coordinador.insertar_serie,'2': coordinador.insertar_pelicula,'3': coordinador.insertar_manga}
        opcion_agregar=dicc_inserciones.get(opcion_ingreso, lambda:  'NA')()
        if(opcion_agregar=='NA'):
            alertas().mostrar_mensaje('no_val')

    #-----------------------------------------------------------------#
    def listar_registros(self):
        print(Coordinador_de_series().listar_series_del_dia())
        opcion_seleccionada = str(input(f'\n{"-"*10}Opciones de listado{"-"*10}\n1)-Listar series\n2)-Listar series en proceso\n3)-Listar series en espera\n4)-Listar series por rango\n5)-Listar por dia de emisión\n6)-Listar por género\n7)-Listar peliculas\n8)-Listar mangas\nSeleccione una opción: '))
        coordinador = Coordinador_de_series()
        dicc_listados = {'1': coordinador.listar_series,'2': coordinador.listar_series_en_proceso,'3': coordinador.listar_series_en_espera,
        '4': coordinador.listar_series_por_rango,'5':coordinador.listar_series_por_emision,
        '6':coordinador.listar_series_por_genero,'7': coordinador.listar_peliculas,'8':coordinador.listar_mangas}
        registros = dicc_listados.get(opcion_seleccionada,  lambda: alertas().mostrar_mensaje('no_val'))()
        if(str(type(registros)) == "<class 'tuple'>"):
            system('cls')
            if(len(registros[0])==0):
                alertas().mostrar_mensaje('no_ext')
                return
            for registro in registros[0]:
                print(registro.mostrar_min())
            if(registros[1]):
                print(f'\nCantidad de registros [{registros[1]}]: {len(registros[0])}')
        if(str(type(registros)) == "<class 'str'>"):
            system('cls')
            print(Coordinador_de_series().listar_series_por_emision())
             

    #-----------------------------------------------------------------#
    def filtrar_lista(self):
        nombre_a_buscar = str(input('\n¿Digite el nombre (completo o parcial) del registro [anime-pelicula-manga]?: '))
        registros_coincidentes = Coordinador_de_series().filtrar_series(nombre_a_buscar.lower())
        
        if(len(list(registros_coincidentes.values()))>0):
            for serie in list(registros_coincidentes.values()):
                print(serie.mostrar_min())
            print(f'\n{"-"*75}\nSi desea seleccionar un registro de la lista prosiga, sino presione [Intro]\n↓{" "*36}↓{" "*36}↓')
            self.seleccionar_registro(registros_coincidentes)
        else:
            alertas().mostrar_mensaje('no_ext')
#-----------------------------------------------------------------#
    def seleccionar_registro(self,registros_coincidentes):
        indice = int(input('\nDigite el indice del registro [anime-pelicula-manga]: '))
        system('cls')
        registro_seleccionado = registros_coincidentes.get(indice,None)
        print(registro_seleccionado)
        if(isinstance(registro_seleccionado, Serie)):
            self.seleccionar_serie(indice)
        elif(isinstance(registro_seleccionado, Pelicula)):
            self.seleccionar_pelicula(indice)
        elif(isinstance(registro_seleccionado, Manga)):
            self.seleccionar_manga(indice)
        else:
            alertas().mostrar_mensaje('no_val')

    #-----------------------------------------------------------------#
    def seleccionar_serie(self,indice_seleccionado=None):
        indice = indice_seleccionado if indice_seleccionado!=None else int(input('\n¿Digite el indice de la serie?: '))
        system('cls')
        serie_seleccionada = Coordinador_de_series().obtener_serie(indice)
        if(serie_seleccionada):
            print(serie_seleccionada.mostrar_det())
            if(len(serie_seleccionada.get_peliculas())>0):
                print('\n♦♦Peliculas♦♦:')
                for pelicula in Coordinador_de_series().listar_peliculas_por_indice(serie_seleccionada.get_peliculas()):
                    print(pelicula.mostrar_min())
            self.actualizar_serie(serie_seleccionada)
    
    #-----------------------------------------------------------------# 
    def actualizar_serie(self,la_serie_a_modficar, actualiza=None):
        
        se_actualiza = actualiza if actualiza!=None else str(input('\n¿Desea actualizar el registro[s/n]?: '))
        system('cls')
        if(se_actualiza.lower()!='s'):
            return
        print(la_serie_a_modficar.mostrar_det())
        opcion_cambio=str(input(f'\n{"-"*5}Opciones de actualización{"-"*5}\n1)-Cambiar estado\n2)-Cambiar posicion\n3)-Modificar serie\n4)-Agregar dia emision\nSeleccione: '))
        coordinador = Coordinador_de_series()
        dicc_actualizaciones = {
        '1': coordinador.cambiar_estado,
        '2': coordinador.cambiar_posicion,
        '3': coordinador.actualizar_serie,
        '4': coordinador.agregar_dia_emision}
        opcion_modificar=dicc_actualizaciones.get(opcion_cambio, lambda serie:  'NA')(la_serie_a_modficar)
        if(opcion_modificar=="NA"):
            alertas().mostrar_mensaje('def')
        else:
            time.sleep(1)
            self.actualizar_serie(la_serie_a_modficar,'s')

    
    #-----------------------------------------------------------------#}
    def seleccionar_pelicula(self,indice_seleccionado=None):
        indice = indice_seleccionado if indice_seleccionado!=None else int(input('\n¿Digite el indice de la pelicula?: '))
        system('cls')
        pelicula_seleccionada = Coordinador_de_series().obtener_pelicula(indice)
        if(pelicula_seleccionada):
            print(pelicula_seleccionada.mostrar_det())
            se_actualiza = str(input('\n¿Desea actualizar el registro[s/n]?: '))
            system('cls')
            if(se_actualiza.lower()=='s'):      
                print('\n'+pelicula_seleccionada.mostrar_det())
                Coordinador_de_series().actualizar_pelicula(pelicula_seleccionada)
            return
    #-----------------------------------------------------------------#}
    def seleccionar_manga(self,indice_seleccionado=None):
        indice = indice_seleccionado if indice_seleccionado!=None else int(input('\n¿Digite el indice del manga?: '))
        system('cls')
        manga_seleccionado = Coordinador_de_series().obtener_manga(indice)
        if(manga_seleccionado):
            print(manga_seleccionado.mostrar_det())
            se_actualiza = str(input('\n¿Desea actualizar el registro[s/n]?: '))
            system('cls')
            if(se_actualiza.lower()=='s'):                 
                print('\n'+manga_seleccionado.mostrar_det())
                Coordinador_de_series().actualizar_manga(manga_seleccionado)
            return
    #-----------------------------------------------------------------#}
    def consultar_bitacora(self):
        
        print('\nBúsqueda en bitácora (ej. de entradas válidas ["26/04/20" - "96" - "Zero" - "en espera"])')
        busqueda = str(input('Ingrese un parámetro de búsqueda: '))
        Coordinador_de_series().consultar_bitacora(busqueda)


#if __name__ == '__menu__'
Principal().menu()