
class Serie:

    def __init__(self, serie_db={"posicion": "","nombre": "","estado": "","dia_emision": None,"manga_visto": False,"generos": [],"peliculas": []}):

        self.posicion = serie_db["posicion"]
        self.nombre = serie_db["nombre"]
        self.estado =  serie_db["estado"]
        self.dia_emision = serie_db["dia_emision"]
        self.manga_visto= serie_db["manga_visto"]
        self.generos = serie_db["generos"]
        self.peliculas = serie_db["peliculas"]
       # self.obj_pelicula = Pelicula()
    

    def mostrar_det(self):
        datos_generales = f'\n{"•"*12}Serie{"•"*12}\n\nPosicion: {self.get_posicion()}\nNombre: {self.nombre}\nEstado: {self.estado}'
        dia_emision = '' if self.get_dia_emision()==None else f'\nEmisión: {self.get_dia_emision()}'
        manga = f'\nManga: no leído/no aplica' if self.get_manga_visto() == False else f'\nManga: leído'
        generos = '' if len(self.get_generos())==0 else f'\nGéneros: {", ".join(self.get_generos())}'

        return datos_generales+manga+dia_emision+generos
        
    def __gt__(self, Serie):
        return self.posicion > Serie.posicion

    def __ne__(self, Serie):
        return bool(self.posicion != Serie.posicion 
        or self.nombre != Serie.nombre 
        or self.estado != Serie.estado 
        or self.dia_emision != Serie.dia_emision 
        or self.manga_visto != Serie.manga_visto 
        or self.generos != Serie.generos 
        or self.peliculas != Serie.peliculas)


    def mostrar_min(self):
        return f'[{self.get_posicion()}]-{self.get_nombre()}\n'

    def obj_to_dicc(self):
        return {
         "posicion": self.get_posicion(),
         "nombre": self.get_nombre(),
         "estado": self.get_estado(),
         "dia_emision": self.get_dia_emision(),
         "manga_visto": self.get_manga_visto(),
         "generos": self.get_generos(),
         "peliculas": self.get_peliculas()
      }
    
    def set_posicion(self, posicion):
        self.posicion = posicion
    
    def get_posicion(self):
        return self.posicion

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

    def set_peliculas(self, peliculas):
        self.peliculas = peliculas
    
    def get_peliculas(self):
        return self.peliculas
    
    def set_manga_visto(self, manga_visto):
        self.manga_visto = manga_visto
    
    def get_manga_visto(self):
        return self.manga_visto

class Pelicula:

    def __init__(self, pelicula_db):
        self.indice = pelicula_db["indice"]
        self.nombre = pelicula_db["nombre"]
        self.reacciones =  pelicula_db["reacciones"]
        self.manga_visto= pelicula_db["manga_visto"]

    def mostrar_min(self):
        return f'\n[{self.get_indice()}]-{self.get_nombre()}'
        #print(salida)

    def mostrar_det(self):
        manga = '' if self.get_manga_visto() == False else f'\nManga: leído'
        reacciones = '' if self.get_reacciones() == None else f'\nReacciones: {self.get_reacciones()}'
        salida=f'Indice: {self.get_indice()}\nNombre: {self.get_nombre()}'
        salida+=reacciones
        salida+=manga
        return salida

    def __ne__(self, Pelicula):
        return bool(self.posicion != Pelicula.posicion 
        or self.nombre != Pelicula.nombre 
        or self.reacciones != Pelicula.reacciones
        or self.manga_visto != Pelicula.manga_visto )
          
    def obj_to_dicc(self):
        return {
            "indice": self.get_indice(),
            "nombre": self.get_nombre(),
            "reacciones": self.get_reacciones(),
            "manga_visto": self.get_manga_visto()
            }
            

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

class Manga:
    
    def __init__(self, manga_db):
        self.indice = manga_db["indice"]
        self.nombre = manga_db["nombre"]
        self.generos = manga_db["generos"]

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
    
    def get_dia_generos(self):
        return self.generos