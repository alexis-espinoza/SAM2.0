from acc_datos import Gestor_de_series
from modelos import Serie
from os import system
import time
import pyperclip


class Coordinador_de_series:

    def __init__(self):
         self.dicc_dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves','Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
    
    def listar_registos(self):
        return Gestor_de_series.obtener_registros()
    
    #-----------------------------------------------------------------#
    def filtrar_series(self, nombre_a_buscar):
        print()
        return list(filter(lambda Serie: Serie.get_nombre().lower().find(nombre_a_buscar)!=-1, Gestor_de_series().obtener_series()))

    #-----------------------------------------------------------------#
    def obtener_serie(self, indice):
        try:
                print()
                lista_de_series = Gestor_de_series().obtener_series()
                return lista_de_series[indice-1]

        except Exception:
            return False
            print('\n¡No se pudo seleccionar el registro indicado!')

    #-----------------------------------------------------------------#    
    def obtener_pelicula(self, indice):
        try:
                print()
                lista_de_peliculas = Gestor_de_series().obtener_peliculas()
                return lista_de_peliculas[indice-1]

        except Exception:
            return False
            print('\n¡No se pudo seleccionar el registro indicado!')
 
    #-----------------------------------------------------------------#
    def actualizar_serie(self, serie_a_actualizar):
     
        opcion_cambio=int(input('\n1)-Actualizar posicion\n2)-Modificar registro\n3)-Cambiar estado\n4)-Agregar dia de emision\nSeleccione: '))
        if(opcion_cambio==1):
            self.cambiar_posicion(serie_a_actualizar)
            
        elif(opcion_cambio==2):
            flag_cambio=False
            print('\nPara dejar los valores sin cambios presione [enter]')
            nombre = str(input('Digite el nuevo nombre: '))
            generos=[]
            genero='ninguno'
            while(genero!=''):
                genero = str(input('Ingrese un género o [Intro] para finalizar:'))
                if(genero!=''):
                    generos.append(genero)
            peliculas=[]
            pelicula='ninguno'
            while(pelicula!=''):
                pelicula = str(input('Ingrese un indice de pelicula o [Intro] para finalizar:'))
                if(pelicula!=''):
                    peliculas.append(pelicula)
            manga = str(input('Manga visto[s/n]: '))
            
            if(nombre!=''):
                serie_a_actualizar.set_nombre(nombre)
                flag_cambio=True
            if(len(generos)>0):
                serie_a_actualizar.set_generos(generos)
                flag_cambio=True
            if(len(peliculas)>0):
                serie_a_actualizar.set_peliculas(peliculas)
                flag_cambio=True
            if(manga.lower()=='s'):
                serie_a_actualizar.set_manga_visto(True)
                flag_cambio=True
            
            if(flag_cambio==True):
                data_actual = Gestor_de_series().obtener_registros()
                data_actual["series"][serie_a_actualizar.get_posicion()-1]=serie_a_actualizar.obj_to_dicc()
                Gestor_de_series().guardar_cambios(data_actual)
        
        elif(opcion_cambio==3):
                estados = dicc_estados = {1:'finalizada',2:'en proceso',3:'en espera'}
                opcion_estado = int(input('\nSeleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
                nuevo_estado= dicc_estados.get(opcion_estado,'NA')
                print(nuevo_estado)
                if(serie_a_actualizar.get_estado()==nuevo_estado or nuevo_estado == 'NA'):
                    print('¡No se ejecutó el cambio de estado!')
                else:
                    serie_a_actualizar.set_estado(nuevo_estado)
                    data_actual = Gestor_de_series().obtener_registros()
                    data_actual["series"][serie_a_actualizar.get_posicion()-1]=serie_a_actualizar.obj_to_dicc()
                    Gestor_de_series().guardar_cambios(data_actual)
        
        elif(opcion_cambio==4):
                text_emision= f'\n¿Día de emisión de la serie [{serie_a_actualizar.get_nombre()}]'
                valor=1
                for dia in list(self.dicc_dias.values()):
                    text_emision+=f'\n{list(self.dicc_dias.values()).index(dia)+1} = {dia}'
                    valor+=1
                text_emision+="\nSeleccione: "
                indice_dia = int(input(text_emision))
                if(indice_dia>1 and indice_dia<8):
                    dia_emision =  list(self.dicc_dias.values())[indice_dia-1]
                    serie_a_actualizar.set_dia_emision(dia_emision)
                    data_actual = Gestor_de_series().obtener_registros()
                    data_actual["series"][serie_a_actualizar.get_posicion()-1]=serie_a_actualizar.obj_to_dicc()
                    Gestor_de_series().guardar_cambios(data_actual)
                else:
                    print('¡Operación no confirmada!')
        else:
            print('¡Operación no confirmada!')
                
    def actualizar_pelicula(self, pelicula_a_actualizar):
        print()
        flag_cambio=False
        nombre = str(input('Digite el nuevo nombre: '))
        reacciones = str(input('Digite el nuevo valor para las reacciones: '))
        manga = str(input('Manga visto[s/n]: '))
        
        if(nombre!=''):
            pelicula_a_actualizar.set_nombre(nombre)
            flag_cambio=True
        if(reacciones!=''):
            pelicula_a_actualizar.set_reacciones(reacciones)
            flag_cambio=True
        if(manga.lower()=='s'):
            pelicula_a_actualizar.set_manga_visto(True)
            flag_cambio=True
        
        if(flag_cambio==True):
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["peliculas"][pelicula_a_actualizar.get_indice()-1]=pelicula_a_actualizar.obj_to_dicc()
            Gestor_de_series().guardar_cambios(data_actual)
        #text=str(registro_a_actualizar.obj_to_dicc())
        #pyperclip.copy(text)  # now the clipboard content will be string "abc"
        #text = clipboard.paste() 
        #inp = input('pegue: ')  
    
    def cambiar_posicion(self):
        return True

    def generar_dashboard(self):

        todos_los_registros = Gestor_de_series().obtener_registros()
        series= len(todos_los_registros["series"])
        peliculas = len(todos_los_registros["peliculas"])
        mangas = len(todos_los_registros["mangas"])
        en_proceso=0
        en_espera=0
        en_emision=0
        finalizadas=0
        for serie in Gestor_de_series().obtener_series():
            if(serie.get_estado()=="finalizada"):
                finalizadas+=1
            elif (serie.get_estado()=="en espera"):
                en_espera+=1        
            elif (serie.get_estado()=="en proceso"):
                en_proceso+=1
            if(serie.get_dia_emision()!=None):
                en_emision+=1
        separador_uno = ''
        separador_dos = ''
        #animes                      #peliculas
        if(series > 999 or peliculas > 99): #Por si siguiera creciendo
            separador_uno = '_'*76
            separador_dos = '‾'*76
        else:
            separador_uno = '_'*112
            separador_dos = '‾'*112
        formato = '|Total de series registradas: [{0}]  /  Total de películas registradas: [{1}]  /  Total de mangas registrados: [{2}]|\n|\t\tFinalizadas: [{3}]  /  En proceso: [{4}]  /  En espera: [{5}]  /  En emison: [{6}]\t\t\t |'
        informe = formato.format(series, peliculas, mangas, finalizadas, en_proceso, en_espera, en_emision)

        return f' {separador_uno}\n{informe}\n {separador_dos}'
    
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
    
    def listar_peliculas_por_indice(self, lista_indices):
        try:
            return list(filter(lambda Pelicula: str(Pelicula.get_indice()) in lista_indices, Gestor_de_series().obtener_peliculas()))
        except Exception:
            return ''

    
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
    


    