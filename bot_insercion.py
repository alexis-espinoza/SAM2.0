
#options.set_headless()
#driver.set_window_size(0,500)
from operator import ge
from selenium import webdriver
from modelos import Serie
import copy 
import os



class Bot():
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('---window-position=0,900')
        self.options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.DRIVER = 'chromedriver.exe'
        self.driver = webdriver.Chrome(self.DRIVER, options=self.options, service_log_path=os.devnull)
        
    def obtener_serie(self, url_serie):
        try:
            self.driver.get(url_serie)
            lista_de_generos = self.driver.find_elements_by_xpath("//*[@class='Nvgnrs']//following::a[1]")#Se obtiene el nombre
            nombre = self.driver.find_element_by_xpath("//*[@class='Title']//following::h1[1]")           #Se obtienen los géneros
            
            list_gen=[]
            serie_automatica = Serie()
            serie_automatica.set_indice('###')
            serie_automatica.set_estado('en proceso')
            serie_automatica.set_nombre(nombre.text)
            
            for genero in lista_de_generos[:-1]:
                list_gen.append(genero.text)
            serie_automatica.set_generos(list_gen)    
            self.driver.quit()
            return serie_automatica
        
        except Exception:
            self.driver.quit()
            return Serie()
