    
from dependencias.Notas import Nota, ListaNotas
from datetime import date, datetime
from os import renames as renombrarArchivo, replace as reemplazarArchivo
from os.path import isfile as esArchivo
from typing import overload, Union

class Informe:
    def __init__(
            self,
            fecha                       : date       = date.today(),
            bloqueNotasGeneral          : ListaNotas = ListaNotas(),
            resumen                     : str        = "",
            ) -> None:
        
        self.fecha                      : date = fecha
        self.bloqueNotasGeneral         : ListaNotas = bloqueNotasGeneral
        self.resumen                    : str = resumen

    @overload
    @classmethod
    def desdeCSV(cls,archivo : str): ...
    @overload
    @classmethod
    def desdeCSV(cls, fecha : date = date.today()): ...        
    @classmethod
    def desdeCSV(cls, parametro : Union[str | date]):
        if isinstance(parametro, str):
            ARCHIVO         : str = parametro 
        elif isinstance(parametro,date):
            FECHA           : str = parametro.strftime('%Y-%m-%d')
            ARCHIVO         : str = f"Relevamiento_Medios_{FECHA}.csv"
            
        EXISTE_INFORME  : bool = esArchivo(f"./{ARCHIVO}")
        if not EXISTE_INFORME:
            nuevoInforme : Informe =  Informe()
        else:
            nuevoInforme : Informe = Informe()
            nuevaLista   : ListaNotas = ListaNotas()

            with open(ARCHIVO,mode="r",encoding="utf-8") as csv:
                linea : str
                for linea in csv:
                    #print(f"[DEBUG] {linea}")
                    try:
                        campos : list[str] = linea.split(sep=";")
                        urlNota = campos[0]
                        medioNota = campos[1]
                        tituloNota = campos[2]
                        etiquetasNota = campos[3]
                        fechaNota = campos[4]
                        relevanciaNota = campos[5]
                        bloqueNota = campos[6]
                        volantaNota = campos[7]

                        nota : Nota = \
                        Nota(
                                urlNota,
                                medioNota,
                                tituloNota,
                                etiquetasNota, 
                                fechaNota,
                                relevanciaNota,
                                bloqueNota,
                                volantaNota,
                                )
                        nuevaLista.agregarNota(nota)    
                    except:
                        continue

            nuevoInforme.agregarLista(nuevaLista)
        return nuevoInforme

    def __str__(self) -> str:
        return  f'{ f"ELECCIONES 2023. Informe de Medios."}\n\n'  \
                f'{ f"Fecha: {self.fecha}"}\n'                    \
                f'{ f"Resumen Ejecutivo: {self.resumen}"}\n'      \

    def agregarNota(self,notaNueva : Nota):
        if type(notaNueva) == Nota:
            if not notaNueva.bloque:
                self.bloqueNotasGeneral.agregarNota(notaNueva)
            else:
                nombreBloque : str = f"bloqueNotas{notaNueva.bloque}"
                if getattr(self,nombreBloque,False):
                   getattr(self,nombreBloque).agregarNota(notaNueva) 
                else:
                    nuevoBloque : ListaNotas = ListaNotas()
                    nuevoBloque.agregarNota(notaNueva)
                    setattr(self,nombreBloque,nuevoBloque)

        return self
    
    def agregarLista(self,listaNueva : ListaNotas):
        if type(listaNueva) == ListaNotas:
            listaNueva.sort()
            for nota in listaNueva : self.agregarNota(nota)
        return self
    
    def crearMensajeWPP(self, nombreArchivo : str = None):
        if nombreArchivo is None: nombreArchivo = f"Relevamiento_Medios_{self.fecha}"
        
        RUTA_INFORME_HOY : str = f"{nombreArchivo}_wpp.txt"
        EXISTE_INFORME_HOY : bool = esArchivo(f"./{RUTA_INFORME_HOY}")
        #print(f"[DEBUG]  WPP-{EXISTE_INFORME_HOY=}")

        if EXISTE_INFORME_HOY:
            try:
                renombrarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")
            except FileExistsError:
                reemplazarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")   
        
        nota : Nota
        with open(RUTA_INFORME_HOY,mode="w",encoding="utf-8") as txt:
            txt.write(f"*INFORME* | _{self.fecha}_ - {datetime.today().strftime('%H:%M')}\n")
            for bloque, lista in ((bloque, lista) for (bloque, lista) in self.__dict__.items() if (type(lista) == ListaNotas)):
                #print(f"[DEBUG] {bloque = }")
                txt.write(f'----------------------------------------\n') 
                txt.write(f"*{bloque.replace('bloqueNotas','')}*\n")
                for nota in lista : txt.write(f"{nota.__wpp__()}\n")
            txt.write(f'----------------------------------------\n') 

    def crearTxt(self, nombreArchivo : str = None):
        if nombreArchivo is None: nombreArchivo = f"Relevamiento_Medios_{self.fecha}"
        
        RUTA_INFORME_HOY : str = f"{nombreArchivo}.txt"
        EXISTE_INFORME_HOY : bool = esArchivo(f"./{RUTA_INFORME_HOY}")
        #print(f"[DEBUG]  WPP-{EXISTE_INFORME_HOY=}")

        if EXISTE_INFORME_HOY:
            try:
                renombrarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")
            except FileExistsError:
                reemplazarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")   

        nota : Nota
        with open(RUTA_INFORME_HOY,mode="w",encoding="utf-8") as txt:
            txt.write(f"*INFORME* | _{self.fecha}_ - {datetime.today().strftime('%H:%M')}\n")
            for bloque, lista in ((bloque, lista) for (bloque, lista) in self.__dict__.items() if (type(lista) == ListaNotas)):
                #print(f"[DEBUG] {bloque = }")
                txt.write(f'----------------------------------------\n') 
                txt.write(f"*{bloque.replace('bloqueNotas','')}*\n")
                for nota in lista : txt.write(f"{nota}\n")
            txt.write(f'----------------------------------------\n') 

    def crearCSV(self, nombreArchivo : str = None):
        if nombreArchivo is None: nombreArchivo = f"Relevamiento_Medios_{self.fecha}"
        
        RUTA_INFORME_HOY : str = f"{nombreArchivo}.csv"
        EXISTE_INFORME_HOY : bool = esArchivo(f"./{RUTA_INFORME_HOY}")
        #print(f"[DEBUG]  CSV-{EXISTE_INFORME_HOY=}")

        if EXISTE_INFORME_HOY:
            try:
                renombrarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")
            except FileExistsError:
                reemplazarArchivo(f"./{RUTA_INFORME_HOY}",f"./relevamientos_anteriores/{RUTA_INFORME_HOY}")   

        nota : Nota
        with open(RUTA_INFORME_HOY,mode="w",encoding="utf-8") as csv:
            csv.write(f"nota.url;nota.medio;nota.titulo;nota.etiquetas;nota.fecha;nota.relevancia;nota.bloque;nota.volanta\n")
            for bloque, lista in ((bloque, lista) for (bloque, lista) in self.__dict__.items() if  (type(lista) == ListaNotas)):
                #print(f"[DEBUG] {bloque = }")
                for nota in lista : csv.write(f"{nota.url};{nota.medio};{nota.titulo};{nota.etiquetas};{nota.fecha};{nota.relevancia};{nota.bloque};{nota.volanta}\n")

    def agregarAResumen(self, textoAgregar : str):
        self.resumen += textoAgregar


def main(): ...

if __name__ == "__main__":
    main()