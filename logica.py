from acc_datos import Gestor_de_series
from modelos import Serie
from os import system
import time
import pyperclip
#from logica import Coordinador_de_alertas as alertas


class Coordinador_de_series():

    def __init__(self):
         self.dicc_dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves','Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
         self.dias_validos=['1','2','3','4','5','6','7']
         self.dicc_estados = {'1':'finalizada','2':'en proceso','3':'en espera'}
         self.alertas = Coordinador_de_alertas()

#-----------------------------------------------------------------#    
    def listar_registos(self):
        return Gestor_de_series.obtener_registros()

#-----------------------------------------------------------------#
    def agregar_generos(self):
        list_generos=[]
        genero='ninguno'
        while(genero!=''):
            genero = str(input('Ingrese un género o [Intro] para finalizar:'))
            if(genero!=''):
                list_generos.append(genero)
        return list_generos

#-----------------------------------------------------------------#
    def agregar_peliculas(self):
        list_peliculas=[]
        pelicula='ninguno'
        while(pelicula!=''):
            pelicula = str(input('Ingrese un indice de pelicula o [Intro] para finalizar:'))
            if(pelicula!=''):
                list_peliculas.append(pelicula)
        return list_peliculas

#-----------------------------------------------------------------#
    def listar_opciones_de_emision(self,la_serie):
        text_emision= f'¿Día de emisión de la serie [{la_serie.get_nombre()}]'
        valor=1
        for dia in list(self.dicc_dias.values()):
            text_emision+=f'\n{list(self.dicc_dias.values()).index(dia)+1} = {dia}'
            valor+=1
        text_emision+="\nSeleccione: "
        return text_emision
     
     #-----------------------------------------------------------------#
    def insertar_serie(self):
        nueva_serie = Serie()
        nueva_serie.set_nombre(input("Digite el nombre de la nueva_serie: "))
        opcion_estado = str(input('Seleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
        nueva_serie.set_estado(self.dicc_estados.get(opcion_estado,'en proceso'))
        indice_dia = str(input(self.listar_opciones_de_emision(nueva_serie)))
        nueva_serie.set_dia_emision(list(self.dicc_dias.values())[(int(indice_dia)-1)] if indice_dia in self.dias_validos else None)
        nueva_serie.set_manga_visto(True if str(input('Manga visto[s/n]: ')).lower()=='s' else False)
        nueva_serie.set_generos(self.agregar_generos())
        nueva_serie.set_peliculas(self.agregar_peliculas())
        if(nueva_serie.get_nombre()!=''):
            data_actual = Gestor_de_series().obtener_registros()
            posicion = len(Gestor_de_series().obtener_series())+1
            nueva_serie.set_posicion(posicion)
            data_actual["series"].append(nueva_serie.obj_to_dicc())
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok')
        else:
            self.alertas.mostrar_mensaje('no_conf')
    #-----------------------------------------------------------------#
    def insertar_pelicula(self):

         pass
         #-----------------------------------------------------------------#
    def insertar_manga(self):

         pass
 
     #-----------------------------------------------------------------#
    def actualizar_pelicula(self, pelicula_a_actualizar):
        system('cls')
        print(pelicula_a_actualizar.mostrar_det())
        nombre = str(input('\nDigite el nuevo nombre: '))
        pelicula_a_actualizar.set_nombre(nombre if nombre!='' else pelicula_a_actualizar.get_nombre())
        reacciones = str(input('Digite el nuevo valor para las reacciones: '))
        pelicula_a_actualizar.set_reacciones(reacciones if reacciones!='' else pelicula_a_actualizar.get_reacciones())
        manga = str(input('Manga visto[s/n]: ')).lower()
        pelicula_a_actualizar.set_manga_visto(True if manga=='s' else pelicula_a_actualizar.get_manga_visto())
        
        data_actual = Gestor_de_series().obtener_registros()
        pelicula_sin_cambios = Serie(data_actual["peliculas"][pelicula_a_actualizar.get_posicion()-1])
        if(pelicula_sin_cambios!= pelicula_a_actualizar):
            data_actual["series"][serie_a_actualizar.get_posicion()-1] = pelicula_a_actualizar.obj_to_dicc()
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok')
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#     
    def actualizar_serie(self,serie_a_actualizar):
        system('cls')
        print(serie_a_actualizar.mostrar_det())
        print('\nPresione [enter] para dejar los valores sin cambios')
        nombre = str(input('Digite el nuevo nombre: '))
        serie_a_actualizar.set_nombre(nombre if nombre!='' else serie_a_actualizar.get_nombre())
        generos=self.agregar_generos()
        serie_a_actualizar.set_generos(generos if len(generos)!=0 else serie_a_actualizar.get_generos())
        peliculas=self.agregar_peliculas()
        serie_a_actualizar.set_peliculas(peliculas if len(peliculas)!=0 else serie_a_actualizar.get_peliculas())
        manga = str(input('Manga visto[s/n]: ')).lower()
        serie_a_actualizar.set_manga_visto(True if manga=='s' else serie_a_actualizar.get_manga_visto())

        data_actual = Gestor_de_series().obtener_registros()
        serie_sin_cambios = Serie(data_actual["series"][serie_a_actualizar.get_posicion()-1])
        if(serie_sin_cambios!= serie_a_actualizar):
            data_actual["series"][serie_a_actualizar.get_posicion()-1] = serie_a_actualizar.obj_to_dicc()
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok')
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#
    def cambiar_estado(self,serie_a_actualizar):
        system('cls')
        print(serie_a_actualizar.mostrar_det())
        opcion_estado = str(input('\nSeleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
        nuevo_estado = self.dicc_estados.get(opcion_estado,'NA')
        if(serie_a_actualizar.get_estado()==nuevo_estado or nuevo_estado == 'NA'):
            self.alertas.mostrar_mensaje('no_conf')
        else:
            serie_a_actualizar.set_dia_emision(None) #Se setea el dia de emision
            serie_a_actualizar.set_estado(nuevo_estado)
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["series"][serie_a_actualizar.get_posicion()-1]=serie_a_actualizar.obj_to_dicc()
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok')
    
    #-----------------------------------------------------------------#
    def agregar_dia_emision(self,serie_a_actualizar):
        system('cls')
        print(serie_a_actualizar.mostrar_det())
        indice_dia = str(input(self.listar_opciones_de_emision(serie_a_actualizar))) #Invoca a una funcion que muestra las opciones de dias
        if(indice_dia in self.dias_validos):
            dia_emision =  list(self.dicc_dias.values())[int(indice_dia)-1]
            serie_a_actualizar.set_dia_emision(dia_emision)
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["series"][serie_a_actualizar.get_posicion()-1]=serie_a_actualizar.obj_to_dicc()
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok')
        else:
            self.alertas.mostrar_mensaje('no_conf')
    
    #-----------------------------------------------------------------#
    def cambiar_posicion(self, la_serie_a_desplazar):
        try:
            system('cls')
            print(la_serie_a_desplazar.mostrar_det())
            lista_de_series = Gestor_de_series().obtener_series()
            posicion_actual = la_serie_a_desplazar.get_posicion()-1
            nueva_posicion = int(input('\n¿Digite la nueva posisición de la serie?: '))-1
            temporal = lista_de_series[nueva_posicion]
            lista_de_series[nueva_posicion] = lista_de_series[posicion_actual]
            pos_act =  lista_de_series[nueva_posicion].get_posicion()
            lista_de_series[nueva_posicion].set_posicion(temporal.get_posicion())
            lista_de_series[posicion_actual] = temporal
            lista_de_series[posicion_actual].set_posicion(pos_act)
            #Se obtienen los datos originales y se cambia el bloque de series por una lista [ordenada y parseada a diccionadrios]
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["series"] = list(map(lambda Serie: Serie.obj_to_dicc(),sorted(lista_de_series)))
            Gestor_de_series().guardar_cambios(data_actual)
        except Exception:
            self.alertas.mostrar_mensaje('no_ok')
    
    #-----------------------------------------------------------------#
    def generar_dashboard(self):
        todos_los_registros = Gestor_de_series().obtener_registros()
        series= len(todos_los_registros["series"])
        peliculas = len(todos_los_registros["peliculas"])
        mangas = len(todos_los_registros["mangas"])
        en_proceso=len(self.listar_series_en_proceso()[0])
        en_espera=len(self.listar_series_en_espera()[0])
        en_emision=len(list(filter(lambda Serie: Serie.get_dia_emision()!=None, Gestor_de_series().obtener_series())))
        finalizadas=len(list(filter(lambda Serie: Serie.get_estado()=='finalizada', Gestor_de_series().obtener_series())))
        separador_uno = ''
        separador_dos = ''
        #animes    |   #peliculas
        if(series > 999 or peliculas > 99): #Por si siguiera creciendo
            separador_uno = '_'*76
            separador_dos = '‾'*76
        else:
            separador_uno = '_'*112
            separador_dos = '‾'*112
        formato = '|Total de series registradas: [{0}]  /  Total de películas registradas: [{1}]  /  Total de mangas registrados: [{2}]|\n|\t\tFinalizadas: [{3}]  /  En proceso: [{4}]  /  En espera: [{5}]  /  En emison: [{6}]\t\t\t |'
        informe = formato.format(series, peliculas, mangas, finalizadas, en_proceso, en_espera, en_emision)

        return f' {separador_uno}\n{informe}\n {separador_dos}'

    #-----------------------------------------------------------------#
    def filtrar_series(self, nombre_a_buscar):
        print()
        return list(filter(lambda Serie: Serie.get_nombre().lower().find(nombre_a_buscar)!=-1, Gestor_de_series().obtener_series()))

    #-----------------------------------------------------------------#
    def obtener_serie(self, indice):
        try:
                lista_de_series = Gestor_de_series().obtener_series()
                return lista_de_series[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False
    
    #-----------------------------------------------------------------#    
    def obtener_pelicula(self, indice):
        try:
                print()
                lista_de_peliculas = Gestor_de_series().obtener_peliculas()
                return lista_de_peliculas[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False
    #-----------------------------------------------------------------#
    def listar_todos(self):
        return True
    #-----------------------------------------------------------------#
    def listar_series(self):
        return (Gestor_de_series().obtener_series(), False)

    #-----------------------------------------------------------------#
    def listar_series_en_proceso(self):
        return (list(filter(lambda Serie: Serie.get_estado()=='en proceso', Gestor_de_series().obtener_series())),'en proceso')
        
    #-----------------------------------------------------------------#
    def listar_series_en_espera(self):
        return (list(filter(lambda Serie: Serie.get_estado()=='en espera', Gestor_de_series().obtener_series())), 'en espera')

    #-----------------------------------------------------------------#
    def listar_series_por_rango(self):
        try:
            rango = str(input('\nIndique el rango de series a mostrar con el formato [inicio-final]: ' ))
            print()
            inicio = int(rango.split('-')[0])
            final = int(rango.split('-')[1])
            if(inicio>final):
                f=final
                final=inicio
                inicio=f
            return (list(filter(lambda Serie: Serie.get_posicion()>=inicio and Serie.get_posicion()<=final, Gestor_de_series().obtener_series())), False)
        except Exception:
            print()

    #-----------------------------------------------------------------#
    def listar_peliculas(self):
        return (Gestor_de_series().obtener_peliculas(),False)

    #-----------------------------------------------------------------#
    def listar_peliculas_por_indice(self, lista_indices):
        try:
            return list(filter(lambda Pelicula: str(Pelicula.get_indice()) in lista_indices, Gestor_de_series().obtener_peliculas()))
        except Exception:
            return ''

    #-----------------------------------------------------------------# 
    def listar_mangas(self):
        return Gestor_de_series.obtener_mangas()    

    #-----------------------------------------------------------------#
    def listar_series_del_dia(self):
        lista_de_registros = Gestor_de_series().obtener_series()
        dia_de_hoy=time.strftime("%A",time.localtime())
        series_del_dia=''
        encabezado='\nSeries en emisión hoy ['+self.dicc_dias.get(dia_de_hoy)+']\n\n'
        for registro_actual in lista_de_registros:
            if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia_de_hoy)):
                series_del_dia+=registro_actual.mostrar_min()
        if(series_del_dia!=''):
                series_del_dia+=encabezado
        return series_del_dia

    #-----------------------------------------------------------------#
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
    

    def consultar_bitacora(self, busqueda):
        print()
        registros_de_bitacora = list(filter(lambda linea: linea.find(busqueda.lower())!=-1, Gestor_de_series().obtener_logs()))
        registro_actual = 0
        total_de_registros=len(registros_de_bitacora)
        formato = '\nMostrando {0} de {1} registros, ¿mostrar más? [s/n]: '
        
        while(registro_actual<total_de_registros):        
            if((registro_actual%10)==0 and registro_actual!=0):           
                mas_datos = input(formato.format(registro_actual,total_de_registros))
                if(mas_datos != 's'):
                    system('cls')
                    return
                else:
                    print('')#Se salta un línea
            print(registros_de_bitacora[registro_actual])
            registro_actual+=1
        if(len(registros_de_bitacora)==0):
            self.alertas.mostrar_mensaje('no_ext')
            return
        cerrar_bitacora = str(input('\nPresione [Intro] para salir de la bitácora'))
        system('cls')                  


class Coordinador_de_alertas():
    def __init__(self):
        self.dicc_mensajes = {
            'def':'\n¡Retornando al menú principal!',
            'ok':'\n¡Operación ejecutada exitosamente!',
            'no_conf':'\n¡La operación no produjo cambios!',
            'no_ok':'\n¡La operación no fue ejecutada!',
            'no_ext':'\n¡No se encontraron coincidencias!',
            'no_sel':'\n¡No se encontró el registro indicado!',
            'no_val':'\n¡No seleccionó una opción válida!'
        }
    def mostrar_mensaje(self,codigo_mensaje):
        system('cls')
        print(self.dicc_mensajes.get(codigo_mensaje))