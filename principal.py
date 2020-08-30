
import os
from os import system
from logica import Coordinador_de_series 

class Principal:

    def menu(self):
        while True:
            #try:
                print(Coordinador_de_series().generar_dashboard())
                principal=Principal()
                opciones = '''0)- Getión de proceso\n1)- Agregar nuevo\n2)- Mostrar lista\n3)- Filtrar lista\n4)- Seleccionar registro\n5)- Consultar bitácora\n6)- Cerrar\nDigite una opción: '''
                opcion_seleccionada = str(input(opciones)) 
                dicc_menu = {
                    '1': principal.abrir_diario,
                    '2': principal.listar_registros,
                    '3': principal.filtrar_lista,
                    '4': principal.seleccionar_registro,
                    '5': principal.consultar_bitacora,
                    '6': principal.cerrar_sistema
                    }
                dicc_menu.get(opcion_seleccionada)()
            #except Exception:
             #   os.system('cls')
              #  print('\n¡Retornando al menú principal!') 

    def abrir_diario(self):
        print('diario')

    def listar_registros(self):
        #listados = '1)-Listar todas\n2)-Listar series\n3)-Listar series en proceso\n4)-Listar series en espera\n5)-Listar series por rango\n6)-Listar peliculas\nSeleccione una opción: '
        system('cls')
        print(Coordinador_de_series().listar_series_del_dia())
        opcion_seleccionada = int(input('----------Opciones de listado----------\n1)-Listar todas\n2)-Listar series\n3)-Listar series en proceso\n4)-Listar series en espera\n5)-Listar series por rango\n6)-Listar peliculas\n7)-Listar por dia de emisión\nSeleccione una opción: '))
        if(opcion_seleccionada<7):
            registros = Coordinador_de_series().listado_general(opcion_seleccionada)
            if(registros[0]):
                for registro in registros[0]:
                    print(registro.mostrar_min())
                if(registros[1]):
                    print(f'Cantidad de registros [{registros[1]}]: {len(registros[0])}\n')
        else:
            print(Coordinador_de_series().listar_series_por_emision())

    def filtrar_lista(self):
        nombre_a_buscar = str(input('¿Digite el nombre de la serie (completo o parcial)?: '))
        series_coincidentes = Coordinador_de_series().filtrar_series(nombre_a_buscar.lower())
        
        if(len(series_coincidentes)>0):
            for serie in series_coincidentes:
                print(serie.mostrar_min())
        else:
            print('\n¡No se encontraron coincidencias!')

    def seleccionar_registro(self):
        
        indice = int(input('¿Digite el indice de la serie?: '))
        registro_seleccionado = Coordinador_de_series().seleccionar_serie(indice)
        print(registro_seleccionado.mostrar_det())
        #print('seleccionar')

    def consultar_bitacora(self):
        print('consultar')

    def cerrar_sistema(self):
        print('cerar')

#if __name__ == '__menu__'
Principal().menu()
      
