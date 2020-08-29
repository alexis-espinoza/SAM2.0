from acc_datos import Acceso_a_datos

class Logica_de_negocios:

    def listar_registos(self):
        return Acceso_a_datos.obtener_registros()

    def listar_series(self):
        return Acceso_a_datos.obtener_series()

    def listar_peliculas(self):
        return Acceso_a_datos.obtener_peliculas()

    def listar_series(self):
        return Acceso_a_datos.obtener_mangas()    

    