
class Serie:

    def __init__(self, serie_db={"indice": "","nombre": "","estado": "","dia_emision": None,"manga_visto": False,"generos": []}):#,"peliculas": []}):

        self.indice = serie_db["indice"]
        self.nombre = serie_db["nombre"]
        self.estado =  serie_db["estado"]
        self.dia_emision = serie_db["dia_emision"]
        self.manga_visto= serie_db["manga_visto"]
        self.generos = serie_db["generos"]
        #self.peliculas = serie_db["peliculas"]

    

    def mostrar_det(self):
        datos_generales = f'\n{"•"*12}Serie{"•"*12}\n\nPosición: {self.get_indice()}\nNombre: {self.get_nombre()}\nEstado: {self.get_estado()}'
        dia_emision = '' if self.get_dia_emision()==None else f'\nEmisión: {self.get_dia_emision()}'
        manga = f'\nManga: no leído/no aplica' if self.get_manga_visto() == False else f'\nManga: leído'
        generos = '' if len(self.get_generos())==0 else f'\nGéneros: {", ".join(self.get_generos())}'
        return datos_generales+manga+dia_emision+generos
        
    def __gt__(self, Serie):
        return self.indice > Serie.indice

    def __ne__(self, Serie):
        return bool(self.indice != Serie.indice 
        or self.nombre != Serie.nombre 
        or self.estado != Serie.estado 
        or self.dia_emision != Serie.dia_emision 
        or self.manga_visto != Serie.manga_visto 
        or self.generos != Serie.generos)
        #or self.peliculas != Serie.peliculas)


    def mostrar_min(self):
        return f'[{self.get_indice()}]-{self.get_nombre()}'


    def set_indice(self, indice):
        self.indice = indice
    
    def get_indice(self):
        return self.indice

    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_nombre(self):
        return self.nombre

    def set_estado(self, estado):
        self.estado = estado
    
    def get_estado(self):
        return self.estado
    
    def set_dia_emision(self, dia_emision):
        self.dia_emision = dia_emision
    
    def get_dia_emision(self):
        return self.dia_emision
    
    def set_generos(self, generos):
        self.generos = generos
    
    def get_generos(self):
        return self.generos

    def set_manga_visto(self, manga_visto):
        self.manga_visto = manga_visto
    
    def get_manga_visto(self):
        return self.manga_visto

class Pelicula:

    def __init__(self, pelicula_db={"id_serie":None,"indice": 1,"nombre": "","reacciones": None,"manga_visto": False}):
        self.id_serie = pelicula_db["id_serie"]
        self.indice = pelicula_db["indice"]
        self.nombre = pelicula_db["nombre"]
        self.reacciones =  pelicula_db["reacciones"]
        self.manga_visto= pelicula_db["manga_visto"]
        

    def mostrar_min(self):
        return f'[{self.get_indice()}]-{self.get_nombre()}'

    def mostrar_det(self): 
        manga = '' if self.get_manga_visto() == False else f'\nManga: leído'
        reacciones = '' if self.get_reacciones() == None else f'\nReacciones: {self.get_reacciones()}'
        salida=f'\n{"♦"*12}Película{"♦"*12}\n\nIndice: {self.get_indice()}\nNombre: {self.get_nombre()}'
        salida+=reacciones
        salida+=manga
        return salida

    def __gt__(self, Pelicula):
        return self.indice > Pelicula.indice

    def __ne__(self, Pelicula):
        return bool(self.indice != Pelicula.indice 
        or self.nombre != Pelicula.nombre 
        or self.reacciones != Pelicula.reacciones
        or self.manga_visto != Pelicula.manga_visto
        or self.id_serie != Pelicula.id_serie)
            

    def set_indice(self, indice):
        self.indice = indice
    
    def get_indice(self):
        return self.indice

    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_nombre(self):
        return self.nombre
    
    def set_reacciones(self, reacciones):
        self.reacciones = reacciones
    
    def get_reacciones(self):
        return self.reacciones

    def set_manga_visto(self, manga_visto):
        self.manga_visto = manga_visto
    
    def get_manga_visto(self):
        return self.manga_visto

    def set_id_serie(self, id_serie):
        self.id_serie = id_serie
    
    def get_id_serie(self):
        return self.id_serie
    

class Manga:
    
    def __init__(self, manga_db= {"indice": "","nombre":"", "generos":[]}):
        self.indice = manga_db["indice"]
        self.nombre = manga_db["nombre"]
        self.generos = manga_db["generos"]

    def mostrar_min(self):
        return f'[{self.get_indice()}]-{self.get_nombre()}'

    def mostrar_det(self):
        datos_generales = f'\n{"»"*12}Manga{"«"*12}\n\nIndice: {self.get_indice()}\nNombre: {self.get_nombre()}'
        generos = '' if len(self.get_generos())==0 else f'\nGéneros: {", ".join(self.get_generos())}'
        return datos_generales+generos
   

    def __ne__(self, Manga):
        return bool(self.indice != Manga.indice 
        or self.nombre != Manga.nombre 
        or self.generos != Manga.generos)

    def set_indice(self, indice):
        self.indice = indice
    
    def get_indice(self):
        return self.indice

    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_nombre(self):
        return self.nombre
    
    def set_generos(self, generos):
        self.generos = generos
    
    def get_generos(self):
        return self.generos