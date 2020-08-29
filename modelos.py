
class Serie:

    def __init__(self, serie_db):
        self.posicion = serie_db["posicion"]
        self.nombre = serie_db["nombre"]
        self.estado =  serie_db["estado"]
        self.dia_emision = serie_db["dia_emision"]
        self.manga_visto= serie_db["manga_visto"]
        self.generos = serie_db["generos"]
        self.peliculas = serie_db["peliculas"]


    def mostrar_det(self):
        dia_emision = '' if self.get_dia_emision()=='' else f'\nDia de emisión: {self.get_dia_emision()}\n'
        manga = f'\nManga: No leído\n' if self.manga_visto() == False else f'\nManga: Leído\n'
        generos = '' if len(self.get_generos())==0 else f'\nGeneros: {"-".join(self.get_dia_emision())}\n'
        
        
        datos_generales = f'Posicion: {self.get_posicion()}\nNombre: {self.nombre}Estado: {self.estado}\n'
        

    def mostrar_min(self):
        salida = f'[{self.get_posicion()}]-{self.get_nombre()}\n'
        print(salida)

    
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
        salida = f'[{self.get_indice()}]-{self.get_nombre()}\n'
        print(salida)


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