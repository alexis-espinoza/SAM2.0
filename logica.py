import copy
from acc_datos import Gestor_de_series
from modelos import Serie, Pelicula, Manga
from bot_insercion import Bot
from os import system
from datetime import datetime
import time
import pyperclip
import operator
import math
from os import getcwd, system
import shutil


class Coordinador_de_series():
    se_actualizo = []

    def __init__(self):
        self.dicc_dias = {'Monday':'lunes', 'Tuesday':'martes', 'Wednesday':'miercoles', 'Thursday':'jueves','Friday':'viernes', 'Saturday':'sabado', 'Sunday':'domingo'}
        self.dias_validos=['1','2','3','4','5','6','7']
        self.dicc_estados = {'1':'finalizada','2':'en proceso','3':'en espera'}
        self.alertas = Coordinador_de_alertas()
        self.c_series = None
        self.c_peliculas = None
        self.c_mangas = None
        self.c_en_espera = None
        self.c_en_emision = None
        self.c_en_proceso = None
        self.c_finalizadas = None
    
  #-----------------------------------------------------------------#
    def generar_dashboard(self):
        self.c_series= self.listar_series()
        self.c_peliculas = self.listar_peliculas()
        self.c_mangas = self.listar_mangas()           
        self.c_en_espera = self.listar_series_por_estado(self.dicc_estados.get('3'))
        self.c_en_proceso = self.listar_series_por_estado(self.dicc_estados.get('2')) 
        self.c_finalizadas = self.listar_series_por_estado(self.dicc_estados.get('1'))
        self.c_en_emision= list(filter(lambda Serie: Serie.get_dia_emision()!=None, self.c_series))
        separador_uno = ''
        separador_dos = ''
        #animes    |   #peliculas
        sp = ' '*2 if(len(self.c_series) > 999 or len(self.c_peliculas) > 99 or len(self.c_mangas) > 9) else ' ' #Por si siguiera creciendo
        separador_uno = '_'*113
        separador_dos = '‾'*113
        formato = '|Total de series registradas: [{0}]  /  Total de películas registradas: [{1}]  /  Total de mangas registrados: [{2}]|\n|\t\tFinalizadas: [{3}]  /  En proceso: [{4}]  /  En espera: [{5}]  /  En emison: [{6}]\t\t\t'+sp+'|'
        informe = formato.format(len(self.c_series), len(self.c_peliculas), len(self.c_mangas), len(self.c_finalizadas), len(self.c_en_proceso), len(self.c_en_espera), len(self.c_en_emision))

        return f' {separador_uno}\n{informe}\n {separador_dos}'
    """
    def mask(self, digito):
        if(digito<=9):
            return'0'+str(digito)
        else:
            return digito
    """
#-----------------------------------------------------------------#     
    def copy_data(self):
        try:
            destination_folder = f'{getcwd()}/BACK_UPS/BACK_UP_DATA'
            folder_path1 = f'{getcwd()}/DATA'
            folder_path2 = f'{getcwd()}/LOGS'
            
            shutil.copytree(folder_path1,destination_folder,dirs_exist_ok=True)
            shutil.copytree(folder_path2,destination_folder,dirs_exist_ok=True)
        
        except Exception as e:
            print(f"Error al copiar directorios: {str(e)}")
            return None
    
#-----------------------------------------------------------------#
    def mostrar_diario(self):
        Gestor_de_series().obtener_avance_diario()

#-----------------------------------------------------------------#
    def copiar_indice_del_registro(self,registro_actual):
            text=registro_actual.get_indice()
            pyperclip.copy(text) 

#-----------------------------------------------------------------#
    def confirmar_accion(self):
        confirmacion = str(input('\nDigite 1 para confirmar: '))
        if confirmacion == '1':
            return True
        else:            
            return False

    #-----------------------------------------------------------------#
    def guardar_cambios(self, la_data_actual, la_data_nueva, tipo_msj='NA'):
        if(Gestor_de_series().guardar_cambios(la_data_nueva)):#Cuando NO actualiza correctamente
            self.alertas.mostrar_mensaje("no_save")
            Gestor_de_series().guardar_cambios(la_data_actual)#Se reversa cargando los datos sin cambios
            time.sleep(0.75) 
            return #Cortala ejecución para evitar escritura en bitácora
        else:#Se muestra mensaje de confirmación para inserciones y actualizaciones
            self.se_actualizo.append(1)
            self.alertas.mostrar_mensaje(tipo_msj) if (tipo_msj!='NA') else None

    #-----------------------------------------------------------------#
    def validar_mangas(self, el_nuevo_registro):
        try:
            el_manga_existente = None
            flag_existe=False
            lista_mangas_vigentes = Gestor_de_series().obtener_mangas()
            for manga in lista_mangas_vigentes:
                if(manga.get_nombre()==el_nuevo_registro.get_nombre()):
                    flag_existe=True
                    el_manga_existente=manga
                    el_nuevo_registro.set_manga_visto(True)
                    el_nuevo_registro.set_generos(manga.get_generos()) if manga.get_generos()!=[] else True
                    break
        except Exception:
            pass
        finally:
            if (flag_existe):
                lista_mangas_vigentes.remove(el_manga_existente)
                for i in range(len(lista_mangas_vigentes)):
                        lista_mangas_vigentes[i].set_indice(i+1)
                data_actual = Gestor_de_series().obtener_registros()
                data_nueva = copy.deepcopy(data_actual)
                data_nueva["mangas"] = list(map(lambda Manga: Manga.__dict__,lista_mangas_vigentes))
                self.guardar_cambios(data_actual, data_nueva)

#-----------------------------------------------------------------#
    def copiar_nombre_del_registro(self,registro_actual):
            text=registro_actual.get_nombre()
            pyperclip.copy(text)  

#-----------------------------------------------------------------#
    def agregar_generos(self):
        list_generos=[]
        genero='ninguno'
        while(genero!=''):
            genero = str(input('Ingrese un género o [Intro] para finalizar: '))
            if(genero!=''):
                list_generos.append(genero)
        return list_generos

#-----------------------------------------------------------------#
    def filtrar_generos(self, genero, serie):
        for genero_actual in serie.get_generos():
            if(genero_actual.lower().find(genero.lower())!=-1):
                return True
        return False

#-----------------------------------------------------------------#
    def agregar_peliculas(self, leer=True, lista_indices=[], la_serie=None):
        if(leer): #Pre registro
            list_peliculas=[]
            indice_pelicula='ninguno'
            indices_validos = list(map(lambda Pelicula: Pelicula.get_indice(), self.listar_peliculas()))
            while(indice_pelicula!=''):
                try:
                    indice_pelicula = str(input('Ingrese un indice de pelicula o [Intro] para finalizar: '))
                    if(indice_pelicula!=''):
                        list_peliculas.append(int(indice_pelicula)) if int(indice_pelicula) in indices_validos else print('¡Relación no agregada!')
                    else: return list_peliculas
                except Exception as e:
                    print('¡Relación no agregada!')
            return list_peliculas
        else:#Guardardo y dejar en firme
                peliculas = Gestor_de_series().obtener_peliculas()
                for Pelicula in peliculas:
                    if(Pelicula.get_indice() in lista_indices):
                        Pelicula.set_id_serie(la_serie.get_indice())
                        self.actualizar_bitacora('up_dt',[Pelicula.get_nombre()])
                data_actual = Gestor_de_series().obtener_registros()
                data_nueva = copy.deepcopy(data_actual)
                data_nueva["peliculas"] = list(map(lambda Pelicula: Pelicula.__dict__,peliculas))
                self.guardar_cambios(data_actual, data_nueva)

#-----------------------------------------------------------------#
    def listar_opciones_de_emision(self,la_serie):
        text_emision= f'¿Día de emisión de la serie [{la_serie.get_nombre()}]?'
        valor=1
        for dia in list(self.dicc_dias.values()):
            text_emision+=f'\n{list(self.dicc_dias.values()).index(dia)+1} = {dia}'
            valor+=1
        text_emision+="\nSeleccione: "
        return text_emision
     
    #-----------------------------------------------------------------#
    def insertar_serie(self):
        system('clear')
        print('\nNuevo registro de tipo (anime) presione [Intro] para omitir algún campo')
        nueva_serie = Serie()        
        nombre = input("\nDigite el nombre de la nueva serie: ")
        peliculas=[]
        auto = False
        #Llamado a BD
        data_actual = Gestor_de_series().obtener_registros()
        data_nueva = copy.deepcopy(data_actual)            
        posicion = len(data_nueva["series"])+1
        if(nombre.find('animeflv.net') != -1):
            auto = True
            system('clear')
            print('\n¡Obteniendo la información en línea!...')
            nueva_serie = copy.deepcopy(Bot().obtener_serie(nombre, posicion))
            print(nueva_serie.mostrar_det()) if nueva_serie.get_nombre()!='' else None
        elif(nombre.find('animeflv.net') == -1):
            nueva_serie.set_nombre(nombre)
            opcion_estado = str(input('Seleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
            nueva_serie.set_estado(self.dicc_estados.get(opcion_estado,'en proceso'))
            if(nueva_serie.get_estado()=='en proceso'):
                indice_dia = str(input(self.listar_opciones_de_emision(nueva_serie)))
                nueva_serie.set_dia_emision(list(self.dicc_dias.values())[(int(indice_dia)-1)] if indice_dia in self.dias_validos else None)
            nueva_serie.set_manga_visto(True if str(input('Manga visto[s/n]: ')).lower()=='s' else False)
            nueva_serie.set_generos(self.agregar_generos())
            peliculas = self.agregar_peliculas()
        if(nueva_serie.get_nombre()!='' and self.confirmar_accion()):            
            self.validar_mangas(nueva_serie)
            #Posicion anterior de llamado a 'BD'
            nueva_serie.set_indice(posicion)
            data_nueva["series"].append(nueva_serie.__dict__)
            self.guardar_cambios(data_actual, data_nueva,'ok_in')
            if(peliculas!=[]):
                self.agregar_peliculas(False, peliculas, nueva_serie)
            self.actualizar_bitacora('insert',['anime',nueva_serie.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf') if not auto else self.alertas.mostrar_mensaje('no_ok')
    #-----------------------------------------------------------------#
    def insertar_pelicula(self):
        system('clear')
        print('\nNuevo registro de tipo (pelicula) presione [Intro] para omitir algún campo')
        opc_id_series = dict(zip(list(map(lambda key: str(key.get_indice()),self.listar_series())),list(range(1, len(self.listar_series())+1))))#Se cargan todas las opciones de id de series disponibles
        opc_id_series['0']=None
        opc_id_series['']=None
        nueva_pelicula = Pelicula()
        nueva_pelicula.set_nombre(input("\nDigite el nombre de la nueva pelicula: "))
        reacciones = str(input('Digite un valor para las reacciones: '))
        nueva_pelicula.set_reacciones(reacciones if reacciones!='' else None)
        nueva_pelicula.set_manga_visto(True if str(input('Manga visto[s/n]: ')).lower()=='s' else False)
        id_serie = str(input('Digite el id serie [0 = ninguno]: '))
        nueva_pelicula.set_id_serie(opc_id_series[id_serie] if opc_id_series.get(id_serie,'NA')!='NA' else opc_id_series[''])
        
        if(nueva_pelicula.get_nombre()!='' and self.confirmar_accion()):
            self.validar_mangas(nueva_pelicula)
            data_actual = Gestor_de_series().obtener_registros()
            data_nueva = copy.deepcopy(data_actual)
            peliculas = Gestor_de_series().obtener_peliculas()
            list(map(lambda Pelicula: Pelicula.set_indice(Pelicula.get_indice()+1), peliculas))
            peliculas.append(nueva_pelicula)
            data_nueva["peliculas"] = list(map(lambda Pelicula: Pelicula.__dict__,sorted(peliculas))) #sorted(list_peliculas)
            self.guardar_cambios(data_actual, data_nueva, 'ok_in')            
            self.actualizar_bitacora('insert',['película',nueva_pelicula.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#
    def insertar_manga(self):
        system('clear')
        print('\nNuevo registro de tipo (manga) presione [Intro] para omitir algún campo')
        nuevo_manga = Manga()
        nuevo_manga.set_nombre(input("\nDigite el nombre del nuevo manga: "))
        nuevo_manga.set_generos(self.agregar_generos())
        if(nuevo_manga.get_nombre()!='' and self.confirmar_accion()):
            data_actual = Gestor_de_series().obtener_registros()
            data_nueva = copy.deepcopy(data_actual)
            indice = len(data_nueva["mangas"])+1
            nuevo_manga.set_indice(indice)
            data_nueva["mangas"].append(nuevo_manga.__dict__)
            self.guardar_cambios(data_actual, data_nueva, 'ok_in')            
            self.actualizar_bitacora('insert',['manga',nuevo_manga.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')
     
     #-----------------------------------------------------------------#
    def actualizar_pelicula(self, pelicula_a_actualizar):
        print('\nPresione [enter] para dejar los valores sin cambios')
        opc_id_series = dict(zip(list(map(lambda key: str(key.get_indice()),self.listar_series())),list(range(1, len(self.listar_series())+1))))#Se cargan todas las opciones de id de series disponibles
        opc_id_series['0']=None
        opc_id_series['']=pelicula_a_actualizar.get_id_serie() 

        nombre = str(input('Digite el nuevo nombre: '))
        pelicula_a_actualizar.set_nombre(nombre if nombre!='' else pelicula_a_actualizar.get_nombre())        
        reacciones = str(input('Digite el nuevo valor para las reacciones: '))
        pelicula_a_actualizar.set_reacciones(reacciones if reacciones!='' else pelicula_a_actualizar.get_reacciones())
        manga = str(input('Manga visto[s/n]: ')).lower()
        pelicula_a_actualizar.set_manga_visto(True if manga=='s' else pelicula_a_actualizar.get_manga_visto())
        id_serie = str(input('Digite el nuevo id serie [0 = eliminar]: '))
        pelicula_a_actualizar.set_id_serie(opc_id_series[id_serie] if opc_id_series.get(id_serie,'NA')!='NA' else opc_id_series[''])
        data_actual = Gestor_de_series().obtener_registros()
        pelicula_sin_cambios = Pelicula(data_actual["peliculas"][pelicula_a_actualizar.get_indice()-1])

        if(pelicula_sin_cambios!=pelicula_a_actualizar and self.confirmar_accion()):
            data_nueva = copy.deepcopy(data_actual)
            data_nueva["peliculas"][pelicula_a_actualizar.get_indice()-1] = pelicula_a_actualizar.__dict__
            self.guardar_cambios(data_actual, data_nueva, 'ok_up')            
            self.actualizar_bitacora('up_dt',[pelicula_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

     #-----------------------------------------------------------------#  
    def actualizar_manga(self, manga_a_actualizar):
        print('\nPresione [enter] para dejar los valores sin cambios')
        nombre = str(input('Digite el nuevo nombre: '))
        manga_a_actualizar.set_nombre(nombre if nombre!='' else manga_a_actualizar.get_nombre())
        generos=self.agregar_generos()
        manga_a_actualizar.set_generos(generos if len(generos)!=0 else manga_a_actualizar.get_generos())
        data_actual = Gestor_de_series().obtener_registros()
        manga_sin_cambios = Manga(data_actual["mangas"][manga_a_actualizar.get_indice()-1])
        if(manga_sin_cambios!= manga_a_actualizar and self.confirmar_accion()):
            data_nueva = copy.deepcopy(data_actual)
            data_nueva["mangas"][manga_a_actualizar.get_indice()-1] = manga_a_actualizar.__dict__
            self.guardar_cambios(data_actual, data_nueva, 'ok_up')            
            self.actualizar_bitacora('up_dt',[manga_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#     
    def actualizar_serie(self,serie_a_actualizar):
        system('clear')
        print(serie_a_actualizar.mostrar_det())
        print('\nPresione [enter] para dejar los valores sin cambios')
        nombre = str(input('Digite el nuevo nombre: '))
        serie_a_actualizar.set_nombre(nombre if nombre!='' else serie_a_actualizar.get_nombre())
        generos=self.agregar_generos()
        serie_a_actualizar.set_generos(generos if len(generos)!=0 else serie_a_actualizar.get_generos())
        peliculas=self.agregar_peliculas()
        manga_visto = str(input('Manga visto[s/n]: ')).lower()
        dicc_manga_ops={'s':True, 'n':False}
        serie_a_actualizar.set_manga_visto(dicc_manga_ops.get(manga_visto, serie_a_actualizar.get_manga_visto()))

        data_actual = Gestor_de_series().obtener_registros()
        serie_sin_cambios = Serie(data_actual["series"][serie_a_actualizar.get_indice()-1])
        if((serie_sin_cambios!= serie_a_actualizar or peliculas!=[]) and self.confirmar_accion()):
            data_nueva = copy.deepcopy(data_actual)
            data_nueva["series"][serie_a_actualizar.get_indice()-1] = serie_a_actualizar.__dict__
            self.guardar_cambios(data_actual, data_nueva, 'ok_up')
            if(peliculas!=[]):
                self.agregar_peliculas(False, peliculas, serie_a_actualizar)            
            self.actualizar_bitacora('up_dt',[serie_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#
    def cambiar_estado(self,serie_a_actualizar):
        system('clear')
        print(serie_a_actualizar.mostrar_det())
        estado_anterior = serie_a_actualizar.get_estado()
        opcion_estado = str(input('\nSeleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
        nuevo_estado = self.dicc_estados.get(opcion_estado,'NA')
        if(serie_a_actualizar.get_estado()==nuevo_estado or nuevo_estado == 'NA'):
            self.alertas.mostrar_mensaje('no_conf')
        else:
            if(self.confirmar_accion()):
                if(nuevo_estado != 'en proceso'):
                    serie_a_actualizar.set_dia_emision(None) #Se setea el dia de emision
                serie_a_actualizar.set_estado(nuevo_estado)
                data_actual = Gestor_de_series().obtener_registros()
                data_nueva  = data_actual
                data_nueva["series"][serie_a_actualizar.get_indice()-1]=serie_a_actualizar.__dict__
                self.guardar_cambios(data_actual, data_nueva, 'ok_up')                
                self.actualizar_bitacora('up_st',[serie_a_actualizar.get_nombre(),estado_anterior,nuevo_estado])
    
    #-----------------------------------------------------------------#
    def agregar_dia_emision(self,serie_a_actualizar):
        system('clear')
        print(serie_a_actualizar.mostrar_det())
        indice_dia = str(input('\n'+self.listar_opciones_de_emision(serie_a_actualizar))) #Invoca a una funcion que muestra las opciones de dias
        dia_emision =  list(self.dicc_dias.values())[int(indice_dia)-1] if indice_dia!='' else None
        if(indice_dia in self.dias_validos and self.confirmar_accion() and serie_a_actualizar.get_dia_emision()!=dia_emision):
            serie_a_actualizar.set_dia_emision(dia_emision)
            estado_anterior = serie_a_actualizar.get_estado()#Se captura el estado actual
            data_actual = Gestor_de_series().obtener_registros()
            data_nueva = copy.deepcopy(data_actual)
            if(serie_a_actualizar.get_estado()!='en proceso'):
                 nuevo_estado = 'en proceso'
                 serie_a_actualizar.set_estado(nuevo_estado)
                 self.actualizar_bitacora('up_st',[serie_a_actualizar.get_nombre(),estado_anterior,nuevo_estado])
            data_nueva["series"][serie_a_actualizar.get_indice()-1]=serie_a_actualizar.__dict__
            self.guardar_cambios(data_actual, data_nueva, 'ok_in')            
            self.actualizar_bitacora('up_em',[serie_a_actualizar.get_dia_emision(), serie_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')
    
    #-----------------------------------------------------------------#
    def cambiar_posicion(self, serie_a_desplazar):
        try:
            system('clear')
            print(serie_a_desplazar.mostrar_det())
            lista_de_series = Gestor_de_series().obtener_series()
            posicion_actual = serie_a_desplazar.get_indice()-1
            nueva_posicion = int(input('\n¿Digite la nueva posición de la serie?: '))-1
            if(nueva_posicion==posicion_actual or nueva_posicion not in range(len(lista_de_series)) or not self.confirmar_accion()):
                  self.alertas.mostrar_mensaje('no_conf')
                  return
            serie_deplazada = lista_de_series[posicion_actual]
            lista_de_series.remove(lista_de_series[posicion_actual])
            lista_de_series.insert(nueva_posicion,serie_deplazada)
            serie_a_desplazar.set_indice(nueva_posicion+1)
            #Se obtienen los datos originales y se cambia el bloque de series por una lista [ordenada y parseada a diccionarios]
            dicc_diferencias = {}
            for i in range(len(lista_de_series)):
                id_anterior = lista_de_series[i].get_indice()
                lista_de_series[i].set_indice(i+1)
                id_actual = lista_de_series[i].get_indice()
                if(id_anterior!=id_actual):
                    dicc_diferencias[id_anterior] = id_actual#Se cargan los desfaces en los indices serie_x_pelicula
            data_actual = Gestor_de_series().obtener_registros()
            data_nueva = copy.deepcopy(data_actual)
            data_nueva["series"] = list(map(lambda Serie: Serie.__dict__,lista_de_series))
            self.guardar_cambios(data_actual, data_nueva, 'ok_up')
            self.sincronizar_series_peliculas(dicc_diferencias)#///Se actualizan las referencias de las películas_x_series///            
            self.actualizar_bitacora('up_ps',[serie_a_desplazar.get_nombre(),posicion_actual+1,nueva_posicion+1])
        except Exception:
            self.alertas.mostrar_mensaje('no_ok')
    
    #-----------------------------------------------------------------#
    def sincronizar_series_peliculas(self, dicc_diferencias):
        lista_de_peliculas = Gestor_de_series().obtener_peliculas()
        for i in  range(len(lista_de_peliculas)):#Recorre la lista original de peliculas
            valor_id_serie = dicc_diferencias.get(lista_de_peliculas[i].get_id_serie(), 'NA')#Valida si la serie tiene una pelicula asociada
            if(valor_id_serie != 'NA'):
                lista_de_peliculas[i].set_id_serie(valor_id_serie)#Cambia la referencia cuando tiene una serie asociada
        data_actual = Gestor_de_series().obtener_registros()
        data_nueva = copy.deepcopy(data_actual)
        data_nueva["peliculas"] = list(map(lambda Pelicula: Pelicula.__dict__,lista_de_peliculas))
        self.guardar_cambios(data_actual, data_nueva)

    #-----------------------------------------------------------------#
    def mostar_vistos_x_genero(self):
        series = self.listar_series()
        total = len(series)
        if(total==0):
            self.alertas.mostrar_mensaje('no_ext')
            return
        dicc_generos = {}
        for serie in  series:
            for genero in serie.get_generos():#Agrega nuevo género o suma a existentes
                dicc_generos[genero.lower()] = 1 if(genero.lower() not in dicc_generos.keys()) else dicc_generos[genero.lower()]+1
        generos_x_porcentaje = sorted(dicc_generos.items(), key=operator.itemgetter(1), reverse=True) #Se ordenan los datos    
        resultados = lambda lista_datos, x: [lista_datos[i:i+x] for i in range(0, len(lista_datos), x)] #Se subdividen
        print("\n Porcentaje de vistas por género:\n")
        for grupo in resultados(generos_x_porcentaje,4):
            salida = ''
            for genero in grupo: #Se da formato a la salida del reporte
                porcentaje = math.ceil(genero[1]*100/total)
                sep = ' |' if (grupo.index(genero)==3) else ''
                salida += f" | {genero[0].capitalize()[0:12]}:".ljust(16) + f"{porcentaje}%".ljust(4).rjust(5)
                salida += f'{genero[1]}{sep}'.rjust(5)
            print(" |","‾"*99,"|")
            print(salida)
            print("  ","‾"*99," ") if (resultados(generos_x_porcentaje,4).index(grupo) == len(resultados(generos_x_porcentaje,4))-1) else True
            
    #-----------------------------------------------------------------# 
    def filtrar_series(self, nombre_a_buscar):#Filtra SERIES-PELICULAS-MANGAS
        if(nombre_a_buscar==''): return
        lista_de_resultados = list(filter(lambda Serie: (Serie.get_nombre().lower().find(nombre_a_buscar)!=-1), 
        Gestor_de_series().obtener_series()+Gestor_de_series().obtener_peliculas()+Gestor_de_series().obtener_mangas()))
        if(len(lista_de_resultados)==1):
            self.copiar_indice_del_registro(lista_de_resultados[0])
        return dict(zip(list(map(lambda key: key.get_indice(),lista_de_resultados)),lista_de_resultados))#lista_de_resultados

    #-----------------------------------------------------------------#
    def obtener_serie(self, indice):
        try:
            lista_de_series = Gestor_de_series().obtener_series()
            self.copiar_nombre_del_registro(lista_de_series[indice-1])
            return lista_de_series[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False
    
    #-----------------------------------------------------------------#    
    def obtener_pelicula(self, indice):
        try:
            lista_de_peliculas = Gestor_de_series().obtener_peliculas()
            self.copiar_nombre_del_registro(lista_de_peliculas[indice-1])
            return lista_de_peliculas[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False

    #-----------------------------------------------------------------#    
    def obtener_manga(self, indice):
        try:
            lista_de_mangas = Gestor_de_series().obtener_mangas()
            self.copiar_nombre_del_registro(lista_de_mangas[indice-1])
            return lista_de_mangas[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False
   
    #-----------------------------------------------------------------#
    def listar_series(self):
        list_series = Gestor_de_series().obtener_series()
        return list_series 
    
    #------------------EN ESPERA - EN PROCESO Y FINALIZADAS-----------------------#
    def listar_series_por_estado(self, estado):
        lista_series_por_estado = list(filter(lambda Serie: Serie.get_estado()==estado, Gestor_de_series().obtener_series()))
        if(estado == 'en proceso'): #Se le quitan los que están en emisión
            lista_series_por_estado = list(filter(lambda Serie: Serie.get_dia_emision()==None, lista_series_por_estado))
        return lista_series_por_estado    
    
    #-----------------------------------------------------------------#
    def listar_series_por_rango(self):
        try:
            system('clear')
            rango = str(input('\nIndique el rango de series a mostrar con el formato [inicio-final]: ' ))
            inicio = int(rango.split('-')[0])
            final = int(rango.split('-')[1])
            if(inicio>final):
                f=final
                final=inicio
                inicio=f
            list_por_rango = list(filter(lambda Serie: Serie.get_indice()>=inicio and Serie.get_indice()<=final, Gestor_de_series().obtener_series()))
            return list_por_rango 
        except Exception:            
            return False
    #-----------------------------------------------------------------#
    def listar_series_por_genero(self):
        try:
            system('clear')
            genero = str(input('\nIndique el género de anime que desea listar: ' ))
            list_por_genero = list(filter(lambda Serie: (self.filtrar_generos(genero,Serie) and genero!=''), Gestor_de_series().obtener_series()))
            return list_por_genero 
        except Exception:            
            return False

    #-----------------------------------------------------------------#
    def listar_peliculas(self):
        return  Gestor_de_series().obtener_peliculas()

    #-----------------------------------------------------------------#
    
    def listar_peliculas_por_id_serie(self, el_id_serie):
            return list(filter(lambda Pelicula: Pelicula.get_id_serie()==el_id_serie, Gestor_de_series().obtener_peliculas()))
  

    #-----------------------------------------------------------------# 
    def listar_mangas(self):
        list_de_mangas = Gestor_de_series().obtener_mangas() + list(filter(lambda Serie: Serie.get_manga_visto() == True , Gestor_de_series().obtener_series())) + list(filter(lambda Pelicula: Pelicula.get_manga_visto() == True , Gestor_de_series().obtener_peliculas()))
        for i in range(len(list_de_mangas)):
            list_de_mangas[i].set_indice(i+1)
        return list_de_mangas 


    #-----------------------------------------------------------------#
    def listar_series_del_dia(self):
        lista_de_registros = Gestor_de_series().obtener_series()
        dia_de_hoy=time.strftime("%A",time.localtime())
        series_del_dia=''
        encabezado='\nSeries en emisión hoy ['+self.dicc_dias.get(dia_de_hoy).capitalize()+']\n\n'
        for registro_actual in lista_de_registros:
            if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia_de_hoy)):
                series_del_dia+=registro_actual.mostrar_min()+'\n'
        if(series_del_dia!=''):
                series_del_dia= encabezado+series_del_dia
        return series_del_dia
       
    #-----------------------------------------------------------------#
    def listar_series_por_emision(self):
        lista_de_registros =Gestor_de_series().obtener_series()
        cont_emision=0
        list_por_emision=[]
        for dia in list(self.dicc_dias.keys()):
            for registro_actual in lista_de_registros:
                dia_it = self.dicc_dias.get(dia)                                  
                if (registro_actual.get_dia_emision() == dia_it): # self.dicc_dias.get(dia)):
                    if(dia_it.capitalize() not in list_por_emision): #Se evita reingresar varias veces los encabezados
                        list_por_emision.append(dia_it.capitalize())
                    list_por_emision.append(registro_actual)
                    cont_emision+=1
        return list_por_emision 

    #-----------------------------------------------------------------#
    def consultar_bitacora(self):
        logs_del_sistema = Gestor_de_series().obtener_logs()
        nueva_busqueda=True
        detener = False
        while(nueva_busqueda==True):
            print('\nBúsqueda en bitácora (ej. de entradas válidas ["26/04/2020" - "96" - "Zero" - "en espera"])')
            busqueda = str(input('Ingrese un parámetro de búsqueda: '))
            dia_como_hoy = datetime.today().strftime("%d/%m/")+'|' #dia como hoy - tiene numeración por defecto
            busqueda = dia_como_hoy if(busqueda=='') else busqueda #Se asigna busqueda 'dia como hoy' por defecto
            reversa = True if(busqueda.find('|')!=-1) else False #bandera para agregar numeración de reversa
            busqueda = busqueda.replace('|','') if(reversa) else busqueda #Se setea nuevamente el texto de búsqueda
            registros_de_bitacora = list(filter(lambda linea: linea.lower().find(busqueda.lower())!=-1 and busqueda!='', logs_del_sistema))
            formato = 'Mostrando [{0}] de [{1}] registros, mostrar más [Intro] | detener [0]: '
            for registro in registros_de_bitacora:
                indice_actual = registros_de_bitacora.index(registro)#Se captura el indice actual
                if(registros_de_bitacora.index(registro)!=0 and (registros_de_bitacora.index(registro)%13)==0):
                    mas_datos = input(formato.format(indice_actual, len(registros_de_bitacora)))
                    detener = True if(mas_datos == '0' or mas_datos.lower()=='n') else print()
                sep = '\n' if(indice_actual==0) else ''
                sep = f'{sep}{indice_actual} - ' if(reversa) else sep #Numeración de reversa según bandera
                print(sep+self.formatear_registro(registro))        
                if(detener==True):
                    detener=False
                    system('clear')  
                    break
            self.alertas.mostrar_mensaje('no_ext') if len(registros_de_bitacora)==0 else True
            continuar=input('\nDigite [m] para realizar una nueva búsqueda [Intro] para salir: ')#Condición para nueva búqueda/borrado de log
            if(continuar!='m'): #Cuando NO es 'm' detiene el ciclo y finaliza la búsqueda
                nueva_busqueda=False
            system('clear')           
            if(continuar.isdigit() and reversa):#Cuando es ún número invoca a la función de borrado de log
                indice_log = continuar 
                log_a_eliminar = registros_de_bitacora[int(indice_log)]
                self.reversar_operacion(log_a_eliminar)
    

    #-----------------------------------------------------------------#
    def formatear_registro(self, registro):
            #Se sacan y modifican todos los textos NO necesarios del log
            registro = registro if(registro.find('del registro de ')==-1) else registro.replace('del registro de ','')
            registro = registro if(registro.find('para el registro')==-1) else registro.replace('para el registro','')
            registro = registro if(registro.find('del dia de emision')==-1) else registro.replace('del dia de emision','emision')            
            registro = registro if(registro.find('del registro ')==-1) else registro.replace('del registro ','')           
            registro = registro if(registro.find('de estado del registro')==-1) else registro.replace('de estado del registro','')
            registro = registro if(registro.find('del registro')==-1) else registro.replace('del registro','')            
            registro = registro if(registro.find('el registro ')==-1) else registro.replace('el registro ','')
            registro = registro if(registro.find('en el ranking ')==-1) else registro.replace('en el ranking ','')
            registro = registro if(registro.find('de [')==-1) else registro.replace('de [','| de [')
            registro = registro if(registro.find('del p')==-1) else registro.replace('del p','| del p')
            registro = registro if(registro.find(' :')==-1) else registro.replace(' :',':')

            #Se ajusta para que todos los logs se puedan mostrar en una sola línea
            arr_registro = registro.split('>')
            #Evalúa las inserciones / dia emisión / modificacion de datos
            if(arr_registro[1].find('Inserción') != -1 or arr_registro[1].find('emision') != -1 or arr_registro[1].find('de datos') != -1 ):
                linea = f'{arr_registro[0]}>{arr_registro[1][:93]}'  #Se arma la nueva línea de log a mostrar
                linea = linea if(linea.find('\n') != -1) else linea+'\n'
            else: #Evalúa los que tienen parámetros de dia estados y posiciones
                data = ''.join(arr_registro[1].split(':')[1:])
                tipo = arr_registro[1].split(':')[0]
                arr_data = data.split('|')
                linea = f'{arr_registro[0]}>{tipo}:{arr_data[0][:45]}|{arr_data[1]}' #Se arma la nueva línea de log a mostrar
            return linea
            
    #-----------------------------------------------------------------#
    def reversar_operacion(self, log_a_eliminar):
        logs_del_sistema = Gestor_de_series().obtener_logs()
        for log in logs_del_sistema:
            if(log == log_a_eliminar):
                logs_del_sistema.remove(log)
                break
        Gestor_de_series().actualizar_historial(logs_del_sistema)
        self.alertas.mostrar_mensaje('ok_up')
    
    #-----------------------------------------------------------------#
    def actualizar_lista_de_vistos(self):
        lista_de_vistos=[]
        todos_los_registros = Gestor_de_series().obtener_registros()
        for tipo in todos_los_registros.keys():
            lista_de_vistos.append(f'\n\n[[{tipo.upper()}]]\n')
            for registro in todos_los_registros[tipo]:
                lista_de_vistos.append(f'\n[{registro["indice"]}]-{registro["nombre"]}')
        Gestor_de_series().guardar_lista(lista_de_vistos)
         
    #-----------------------------------------------------------------#
    def actualizar_bitacora(self, tipo_log, cambios):
      
        cambios=cambios+(['']*2)#Se agregan 2 campos extra vacíos para los casos donde solo viaja un parámetro
        dicc_cambios = {
        'insert': f'Inserción del registro de tipo [{cambios[0]}]: {cambios[1]}',
        'up_st': f'Modificación de estado del registro: {cambios[0]} de [{cambios[1]}] a [{cambios[2]}]',
        'up_dt': f'Modificación de datos del registro: {cambios[0]}',
        'up_em': f'Modificación del dia de emision [{cambios[0]}] para el registro: {cambios[1]}',
        'up_ps': f'Desplazamiento del registro: {cambios[0]} del puesto [{cambios[1]}] al puesto [{cambios[2]}]'
        }
        nuevo_log = f'[{time.strftime("%d/%m/%Y")}] <-> {dicc_cambios.get(tipo_log)}\n'
        Gestor_de_series().agregar_nuevo_log(nuevo_log)
        if(tipo_log != 'up_st' and tipo_log != 'up_em'):
            self.actualizar_lista_de_vistos()
            
            
#-----------------------------------------------------------------#   
#-----------------------------------------------------------------#
class Coordinador_de_alertas:
    def __init__(self):
        self.dicc_mensajes = {
            'def':'\n¡Retornando al menú principal!',
            'ok_in':'\n¡Se agregó exitosamente!',
            'ok_up':'\n¡Se modificó exitosamente!',
            'no_conf':'\n¡La operación no produjo cambios!',
            'no_ok':'\n¡La operación no fue ejecutada!',
            'no_ext':'\n¡No se encontraron coincidencias!',
            'no_sel':'\n¡No se encontró el registro indicado!',
            'no_val':'\n¡No seleccionó una opción válida!',
            'no_save':'\n  ¡Se produjo un error en el proceso!\n**Todos los cambios fueron reversados**',
            'rp_val':'\n¡Validando los cambios realizados!',
            'rp_eje':'\n¡Creando/enviando copia de seguridad!'
        }
    def mostrar_mensaje(self,codigo_mensaje):
        system('clear')
        print(self.dicc_mensajes.get(codigo_mensaje))
