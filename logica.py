from acc_datos import Gestor_de_series
from modelos import Serie, Pelicula, Manga
from os import system
import time
import pyperclip



class Coordinador_de_series():

    def __init__(self):
         self.dicc_dias = {'Monday':'lunes', 'Tuesday':'martes', 'Wednesday':'miercoles', 'Thursday':'jueves','Friday':'viernes', 'Saturday':'sabado', 'Sunday':'domingo'}
         self.dias_validos=['1','2','3','4','5','6','7']
         self.dicc_estados = {'1':'finalizada','2':'en proceso','3':'en espera'}
         self.alertas = Coordinador_de_alertas()

#-----------------------------------------------------------------#    
    def listar_registos(self):
        return Gestor_de_series.obtener_registros()

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
            self.alertas.mostrar_mensaje('no_ok')
            return False

#-----------------------------------------------------------------#
    def validar_mangas(self, el_nuevo_registro):
        #3print()
        '''lista_mangas_vigentes = list(filter(lambda Manga: Manga.get_nombre()!=el_nuevo_registro.get_nombre(), Gestor_de_series().obtener_mangas()))
        for i in range(len(lista_mangas_vigentes)):
            lista_mangas_vigentes[i].set_indice(i+1)
        data_actual = Gestor_de_series().obtener_registros()
        data_actual["mangas"] = list(map(lambda Manga: Manga.__dict__,lista_mangas_vigentes))
        Gestor_de_series().guardar_cambios(data_actual)
        '''
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
                data_actual["mangas"] = list(map(lambda Manga: Manga.__dict__,lista_mangas_vigentes))
                Gestor_de_series().guardar_cambios(data_actual)

#-----------------------------------------------------------------#
    def copiar_nombre_del_registro(self,registro_actual):
            text=registro_actual.get_nombre()
            pyperclip.copy(text)  # now the clipboard content will be string "abc"

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
    def agregar_peliculas(self):
        list_peliculas=[]
        pelicula='ninguno'
        #lista_blanca=[0,1,2,3,4,5,6,7,8,9]
        while(pelicula!=''):
            pelicula = str(input('Ingrese un indice de pelicula o [Intro] para finalizar: '))
            try:
                list_peliculas.append(int(pelicula))
            except Exception:
              None
        return list_peliculas

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
        system('cls')
        print('\nNuevo registro de tipo (anime) presione [Intro] para omitir algún campo')
        nueva_serie = Serie()
        nueva_serie.set_nombre(input("\nDigite el nombre de la nueva serie: "))
        opcion_estado = str(input('Seleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
        nueva_serie.set_estado(self.dicc_estados.get(opcion_estado,'en proceso'))
        if(nueva_serie.get_estado()=='en proceso'):
            indice_dia = str(input(self.listar_opciones_de_emision(nueva_serie)))
            nueva_serie.set_dia_emision(list(self.dicc_dias.values())[(int(indice_dia)-1)] if indice_dia in self.dias_validos else None)
        nueva_serie.set_manga_visto(True if str(input('Manga visto[s/n]: ')).lower()=='s' else False)
        nueva_serie.set_generos(self.agregar_generos())
        nueva_serie.set_peliculas(self.agregar_peliculas())
        if(nueva_serie.get_nombre()!='' and self.confirmar_accion()):            
            self.validar_mangas(nueva_serie)
            data_actual = Gestor_de_series().obtener_registros()
            posicion = len(data_actual["series"])+1
            nueva_serie.set_indice(posicion)
            data_actual["series"].append(nueva_serie.__dict__)
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_in')
            self.actualizar_bitacora('insert',['anime',nueva_serie.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')
    #-----------------------------------------------------------------#
    def insertar_pelicula(self):
        system('cls')
        print('\nNuevo registro de tipo (pelicula) presione [Intro] para omitir algún campo')
        nueva_pelicula = Pelicula()
        nueva_pelicula.set_nombre(input("\nDigite el nombre de la nueva pelicula: "))
        reacciones = str(input('Digite un valor para las reacciones: '))
        nueva_pelicula.set_reacciones(reacciones if reacciones!='' else None)
        nueva_pelicula.set_manga_visto(True if str(input('Manga visto[s/n]: ')).lower()=='s' else False)
        
        if(nueva_pelicula.get_nombre()!='' and self.confirmar_accion()):
            self.validar_mangas(nueva_pelicula)
            data_actual = Gestor_de_series().obtener_registros()
            peliculas = Gestor_de_series().obtener_peliculas()
            list(map(lambda Pelicula: Pelicula.set_indice(Pelicula.get_indice()+1), peliculas))
            peliculas.append(nueva_pelicula)
            data_actual["peliculas"] = list(map(lambda Pelicula: Pelicula.__dict__,sorted(peliculas))) #sorted(list_peliculas)
            Gestor_de_series().guardar_cambios(data_actual)
            self.organizar_series_peliculas()
            self.alertas.mostrar_mensaje('ok_in')
            self.actualizar_bitacora('insert',['película',nueva_pelicula.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

         #-----------------------------------------------------------------#
    def insertar_manga(self):
        system('cls')
        print('\nNuevo registro de tipo (manga) presione [Intro] para omitir algún campo')
        nuevo_manga = Manga()
        nuevo_manga.set_nombre(input("\nDigite el nombre del nuevo manga: "))
        nuevo_manga.set_generos(self.agregar_generos())
        if(nuevo_manga.get_nombre()!='' and self.confirmar_accion()):
            data_actual = Gestor_de_series().obtener_registros()
            indice = len(data_actual["mangas"])+1
            nuevo_manga.set_indice(indice)
            data_actual["mangas"].append(nuevo_manga.__dict__)
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_in')
            self.actualizar_bitacora('insert',['manga',nuevo_manga.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')
     
     #-----------------------------------------------------------------#
    def actualizar_pelicula(self, pelicula_a_actualizar):
        print('\nPresione [enter] para dejar los valores sin cambios')
        nombre = str(input('Digite el nuevo nombre: '))
        pelicula_a_actualizar.set_nombre(nombre if nombre!='' else pelicula_a_actualizar.get_nombre())
        reacciones = str(input('Digite el nuevo valor para las reacciones: '))
        pelicula_a_actualizar.set_reacciones(reacciones if reacciones!='' else pelicula_a_actualizar.get_reacciones())
        manga = str(input('Manga visto[s/n]: ')).lower()
        pelicula_a_actualizar.set_manga_visto(True if manga=='s' else pelicula_a_actualizar.get_manga_visto())
        
        data_actual = Gestor_de_series().obtener_registros()
        pelicula_sin_cambios = Pelicula(data_actual["peliculas"][pelicula_a_actualizar.get_indice()-1])
        if(pelicula_sin_cambios!= pelicula_a_actualizar and self.confirmar_accion()):
            data_actual["peliculas"][pelicula_a_actualizar.get_indice()-1] = pelicula_a_actualizar.__dict__
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_up')
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
            data_actual["mangas"][manga_a_actualizar.get_indice()-1] = manga_a_actualizar.__dict__
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_up')
            self.actualizar_bitacora('up_dt',[manga_a_actualizar.get_nombre()])
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
        manga_visto = str(input('Manga visto[s/n]: ')).lower()
        dicc_manga_ops={'s':True, 'n':False}
        serie_a_actualizar.set_manga_visto(dicc_manga_ops.get(manga_visto, serie_a_actualizar.get_manga_visto()))

        data_actual = Gestor_de_series().obtener_registros()
        serie_sin_cambios = Serie(data_actual["series"][serie_a_actualizar.get_indice()-1])
        if(serie_sin_cambios!= serie_a_actualizar and self.confirmar_accion()):
            data_actual["series"][serie_a_actualizar.get_indice()-1] = serie_a_actualizar.__dict__
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_up')
            self.actualizar_bitacora('up_dt',[serie_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')

    #-----------------------------------------------------------------#
    def cambiar_estado(self,serie_a_actualizar):
        system('cls')
        print(serie_a_actualizar.mostrar_det())
        estado_anterior = serie_a_actualizar.get_estado()
        opcion_estado = str(input('\nSeleccione el nuevo estado para la serie:\n1)-Finalizada\n2)-En proceso\n3)-En espera\nDigite una opción: '))
        nuevo_estado = self.dicc_estados.get(opcion_estado,'NA')
        if(serie_a_actualizar.get_estado()==nuevo_estado or nuevo_estado == 'NA'):
            self.alertas.mostrar_mensaje('no_conf')
        else:
            if(self.confirmar_accion()):
                serie_a_actualizar.set_dia_emision(None) #Se setea el dia de emision
                serie_a_actualizar.set_estado(nuevo_estado)
                data_actual = Gestor_de_series().obtener_registros()
                data_actual["series"][serie_a_actualizar.get_indice()-1]=serie_a_actualizar.__dict__
                Gestor_de_series().guardar_cambios(data_actual)
                self.alertas.mostrar_mensaje('ok_up')
                self.actualizar_bitacora('up_st',[serie_a_actualizar.get_nombre(),estado_anterior,nuevo_estado])
    
    #-----------------------------------------------------------------#
    def agregar_dia_emision(self,serie_a_actualizar):
        system('cls')
        print(serie_a_actualizar.mostrar_det())
        indice_dia = str(input('\n'+self.listar_opciones_de_emision(serie_a_actualizar))) #Invoca a una funcion que muestra las opciones de dias
        if(indice_dia in self.dias_validos and self.confirmar_accion()):
            dia_emision =  list(self.dicc_dias.values())[int(indice_dia)-1]
            serie_a_actualizar.set_dia_emision(dia_emision)
            serie_a_actualizar.set_estado('en proceso')
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["series"][serie_a_actualizar.get_indice()-1]=serie_a_actualizar.__dict__
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_in')
            self.actualizar_bitacora('up_em',[serie_a_actualizar.get_dia_emision(), serie_a_actualizar.get_nombre()])
        else:
            self.alertas.mostrar_mensaje('no_conf')
    
    #-----------------------------------------------------------------#
    def cambiar_posicion(self, serie_a_desplazar):
        try:
            system('cls')
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
            #Se obtienen los datos originales y se cambia el bloque de series por una lista [ordenada y parseada a diccionadrios]
            for i in range(len(lista_de_series)):
                lista_de_series[i].set_indice(i+1)
            data_actual = Gestor_de_series().obtener_registros()
            data_actual["series"] = list(map(lambda Serie: Serie.__dict__,lista_de_series))
            Gestor_de_series().guardar_cambios(data_actual)
            self.alertas.mostrar_mensaje('ok_up')
            self.actualizar_bitacora('up_ps',[serie_a_desplazar.get_nombre(),posicion_actual+1,nueva_posicion+1])
        except Exception:
            self.alertas.mostrar_mensaje('no_ok')
    
    #-----------------------------------------------------------------#
    def generar_dashboard(self):
        todos_los_registros = Gestor_de_series().obtener_registros()
        series= len(todos_los_registros["series"])
        peliculas = len(todos_los_registros["peliculas"])
        mangas = len(self.listar_mangas()[0])
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

    #-----------------------------------------------------------------# self.filtrar_generos(nombre_a_buscar,Serie)
    def filtrar_series(self, nombre_a_buscar):
        lista_de_resultados = list(filter(lambda Serie: (Serie.get_nombre().lower().find(nombre_a_buscar)!=-1 and nombre_a_buscar!=''), 
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
                print()
                lista_de_peliculas = Gestor_de_series().obtener_peliculas()
                self.copiar_nombre_del_registro(lista_de_peliculas[indice-1])
                return lista_de_peliculas[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False

    #-----------------------------------------------------------------#    
    def obtener_manga(self, indice):
        try:
                print()
                lista_de_mangas = Gestor_de_series().obtener_mangas()
                self.copiar_nombre_del_registro(lista_de_mangas[indice-1])
                return lista_de_mangas[indice-1]
        except Exception:
            self.alertas.mostrar_mensaje('no_sel')
            return False

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
            system('cls')
            rango = str(input('\nIndique el rango de series a mostrar con el formato [inicio-final]: ' ))
            inicio = int(rango.split('-')[0])
            final = int(rango.split('-')[1])
            if(inicio>final):
                f=final
                final=inicio
                inicio=f
            #print()
            return (list(filter(lambda Serie: Serie.get_indice()>=inicio and Serie.get_indice()<=final, Gestor_de_series().obtener_series())), False)
        except Exception:
            self.alertas.mostrar_mensaje('def')
            return False
    #-----------------------------------------------------------------#
    def listar_series_por_genero(self):
        try:
            system('cls')
            genero = str(input('\nIndique el género de anime que desea listar: ' ))
            return (list(filter(lambda Serie: (self.filtrar_generos(genero,Serie) and genero!=''), Gestor_de_series().obtener_series())), f'género {genero}')
        except Exception:
            self.alertas.mostrar_mensaje('def')
            return False

    #-----------------------------------------------------------------#
    def listar_peliculas(self):
        return (Gestor_de_series().obtener_peliculas(),False)

    #-----------------------------------------------------------------#
    def listar_peliculas_por_indice(self, lista_indices):
        try:
            return list(filter(lambda Pelicula: Pelicula.get_indice() in lista_indices, Gestor_de_series().obtener_peliculas()))
        except Exception:
            return ''

    #-----------------------------------------------------------------# 
    def listar_mangas(self):
        lista_de_mangas = Gestor_de_series().obtener_mangas() + list(filter(lambda Serie: Serie.manga_visto == True , Gestor_de_series().obtener_series())) + list(filter(lambda Pelicula: Pelicula.manga_visto == True , Gestor_de_series().obtener_peliculas()))
        for i in range(len(lista_de_mangas)):
            lista_de_mangas[i].set_indice(i+1)
        return (lista_de_mangas, False)#'mA-> Orig. Anime | P-> Orig. Película'


        
    #-----------------------------------------------------------------# 
    def organizar_series_peliculas(self):
        lista_de_series = Gestor_de_series().obtener_series()
        for serie in lista_de_series:
            nueva_lista_indice_peliculas = []
            for indice_pelicula in serie.get_peliculas():
                nueva_lista_indice_peliculas.append(indice_pelicula+1)
                serie.set_peliculas(nueva_lista_indice_peliculas)
        data_actual = Gestor_de_series().obtener_registros()
        data_actual["series"] = list(map(lambda Serie: Serie.__dict__,lista_de_series))
        Gestor_de_series().guardar_cambios(data_actual)

    #-----------------------------------------------------------------#
    def listar_series_del_dia(self):
        lista_de_registros = Gestor_de_series().obtener_series()
        dia_de_hoy=time.strftime("%A",time.localtime())
        series_del_dia=''
        encabezado='\nSeries en emisión hoy ['+self.dicc_dias.get(dia_de_hoy).capitalize()+']\n'
        for registro_actual in lista_de_registros:
            if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia_de_hoy)):
                series_del_dia+=registro_actual.mostrar_min()
        if(series_del_dia!=''):
                series_del_dia= encabezado+series_del_dia
        return series_del_dia

    #-----------------------------------------------------------------#
    def listar_series_por_emision(self):
        print()
        lista_de_registros =Gestor_de_series().obtener_series()
        registros_en_dia_actual=''
        salida=''
        registros_en_emision=0
        for dia in list(self.dicc_dias.keys()):
            for registro_actual in lista_de_registros:                                   
                if (registro_actual.get_dia_emision() == self.dicc_dias.get(dia)):
                    registros_en_dia_actual+=registro_actual.mostrar_min().strip('\n')+'\n'
                    registros_en_emision+=1
            if(registros_en_dia_actual!=''):
                    salida+=self.dicc_dias.get(dia).capitalize()+':\n'+registros_en_dia_actual+'\n'
                    registros_en_dia_actual=''
        if(salida!=''):
                conteo='Cantidad de registros [en emisión]: '+str(registros_en_emision)
                return f'{salida}\n{conteo}'
        else:
            self.alertas.mostrar_mensaje('no_ext')
            return 
    

    def consultar_bitacora(self):
        logs_del_sistema = Gestor_de_series().obtener_logs()
        nueva_busqueda=True
        while(nueva_busqueda==True):
            print('\nBúsqueda en bitácora (ej. de entradas válidas ["26/04/20" - "96" - "Zero" - "en espera"])')
            busqueda = str(input('Ingrese un parámetro de búsqueda: '))
            print()
            registros_de_bitacora = list(filter(lambda linea: linea.lower().find(busqueda.lower())!=-1 and busqueda!='', logs_del_sistema))
            total_de_registros=len(registros_de_bitacora)
            registro_actual = 0
            formato = 'Mostrando [{0}] de [{1}] registros, mostrar más [Intro] | detener [1]: '
            while(registro_actual<total_de_registros):        
                if((registro_actual%10)==0 and registro_actual!=0):           
                    mas_datos = input(formato.format(registro_actual,total_de_registros))
                    if(mas_datos == '1' or mas_datos.lower()=='n'):
                        system('cls')
                        break
                    print('')#Se salta un línea
                print(registros_de_bitacora[registro_actual])
                registro_actual+=1

            self.alertas.mostrar_mensaje('no_ext') if total_de_registros==0 else True
            continuar=input('\nDigite [1] para realizar una nueva búsqueda [Intro] para salir: ')#Condición para nueva búqueda
            if(continuar!='1'):
                nueva_busqueda=False
            system('cls')                  
    
    def actualizar_lista_de_vistos(self):
        lista_de_vistos=[]
        todos_los_registros = Gestor_de_series().obtener_registros()
        for tipo in todos_los_registros.keys():
            lista_de_vistos.append(f'\n\n[[{tipo.upper()}]]\n')
            for registro in todos_los_registros[tipo]:
                lista_de_vistos.append(f'\n[{registro["indice"]}]-{registro["nombre"]}')
        Gestor_de_series().guardar_lista(lista_de_vistos)
         

    def actualizar_bitacora(self, tipo_log, cambios):
      
        cambios=cambios+(['']*2)#Se agregan 2 campos extra vacíos para los casos donde solo viaja un parámetro
        dicc_cambios = {
        'insert': f'Inserción del registro de tipo [{cambios[0]}]: {cambios[1]}',
        'up_st': f'Modificación de estado del registro: {cambios[0]} de [{cambios[1]}] a [{cambios[2]}]',
        'up_dt': f'Modificación de datos del registro: {cambios[0]}',
        'up_em': f'Modificación del dia de emision [{cambios[0]}] para el registro: {cambios[1]}',
        'up_ps': f'Desplazamiento del registro: {cambios[0]} del puesto [{cambios[1]}] al puesto [{cambios[2]}]'
        }
        nuevo_log = f'[{time.strftime("%d/%m/%y")}] <-> {dicc_cambios.get(tipo_log)}\n'
        Gestor_de_series().actualizar_logs(nuevo_log)
        if(tipo_log != 'up_st' and tipo_log != 'up_em'):
            self.actualizar_lista_de_vistos()
        
        

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
            'no_val':'\n¡No seleccionó una opción válida!'
        }
    def mostrar_mensaje(self,codigo_mensaje):
        system('cls')
        print(self.dicc_mensajes.get(codigo_mensaje))
