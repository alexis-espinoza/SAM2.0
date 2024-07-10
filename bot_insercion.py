#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from modelos import Serie
import os
from datetime import datetime

class Bot():
    def __init__(self) -> None:
       
        self.dicc_dias = {'Monday':'lunes', 'Tuesday':'martes', 'Wednesday':'miercoles', 'Thursday':'jueves','Friday':'viernes', 'Saturday':'sabado', 'Sunday':'domingo'}
        self.service = Service(executable_path="/usr/bin/chromedriver")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.options.add_argument('---window-position=0,10')
        self.options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.DRIVER = 'chromedriver'
        self.driver = webdriver.Chrome(self.DRIVER, service = self.service,options=self.options)
        
    def obtener_dia_emision(self, fecha):
        dia_emision = None
        if(fecha != 'NO VISTO'):#se valida si está en emisión
            spl_fecha = fecha.split('-')
            anio = int(spl_fecha[0])
            mes = int(spl_fecha[1])
            dia = int(spl_fecha[2])
            dia_ingles = datetime(anio, mes, dia).strftime('%A')
            dia_emision = self.dicc_dias.get(dia_ingles,None) #Se asigna el día en español
        return dia_emision

    def obtener_serie(self, url_serie, posicion):
        try:
            
            self.driver.get(url_serie)
            lista_de_generos = self.driver.find_elements("xpath","//*[@class='Nvgnrs']//following::a[1]")#Se obtiene el nombre
            nombre = self.driver.find_element("xpath","//*[@class='Title']//following::h1[1]")           #Se obtienen los géneros
            proxima_fecha = self.driver.find_element("xpath","//*[@class='Title']//following::h3[1]//following::span[1]") #Se obtiene la proxima fecha de emisión     
            str_fecha = proxima_fecha.text
            serie_automatica = Serie() #Se declara el objeto de tipo 'SERIE'
            serie_automatica.set_indice(posicion) #Se recibe por parámetro desde el flujo principal
            serie_automatica.set_estado('en proceso')
            serie_automatica.set_nombre(nombre.text)
            serie_automatica.set_dia_emision(self.obtener_dia_emision(str_fecha))
            list_gen=[]
            for genero in lista_de_generos[:-1]:
                list_gen.append(genero.text)
            serie_automatica.set_generos(list_gen)    
            self.driver.quit()
            return serie_automatica
        
        except Exception as e:
            print(e)
            self.driver.quit()
            return Serie()


