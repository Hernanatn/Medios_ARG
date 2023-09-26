from datetime import date 
from dependencias.utiles import utilesBS4 
from functools import total_ordering


@total_ordering
class Nota():

    def __init__(
            self,
            url : str,
            medio : str,
            titulo : str,
            etiquetas : set[str], 
            fecha : date = date.today(),
            relevancia : int = 0,
            bloque: str = "",
            volanta: str =""
            ) -> None:
        
        self.url : str = url
        self.medio : str = medio
        self.titulo : str = titulo
        self.etiquetas : set[str] = etiquetas
        self.fecha : date = fecha
        self.relevancia :int =  relevancia
        self.bloque : str = bloque
        self.volanta: str = volanta
   
    def __gt__(self, otro):
        return self.relevancia < otro.relevancia 
    
    def __lt__(self, otro):
        return self.relevancia > otro.relevancia
    
    def __eq__(self, otro):
        otro : Nota = otro        
        elTituloEsMuySimilar : bool = len([palabra for palabra in self.titulo.split() if palabra in otro.titulo.split()])>=len(self.titulo.split())/2
        compartenMuchasEtiquetas : bool = (len([etiqueta for etiqueta in self.etiquetas if etiqueta in otro.etiquetas])>3)

        sonLaMismaNota : bool = (self.url == otro.url)
        sonNotasCasiIdenticas : bool = elTituloEsMuySimilar and self.fecha == otro.fecha and compartenMuchasEtiquetas
        return sonLaMismaNota or sonNotasCasiIdenticas
    
    def __repr__(self):
        return f"{self.titulo}\n{self.medio} | {self.fecha}\n{self.url}\n Etiquetas: {self.etiquetas}\n{self.volanta}\n"
    
    def __str__(self):
        return f"{self.titulo}\n{self.medio} | {self.fecha}\n{self.url}\n Etiquetas: {self.etiquetas}\n{self.volanta}\n\n"
    
    def __wpp__(self):
        return f"*{self.titulo}*\n_{self.medio}_ | _{self.fecha}_\n{self.url}\n{self.volanta}\n\n"

class ListaNotas( list ):
    def __init__(
            self,
            ) -> None:
        self.podio : list[Nota]

    def ordenarPorRelevancia(self) -> None: 
        self.sort()
        for i in (0,4):
            self.podio[i] = self[i]

    def agregarNota(self, nota : Nota): 
       if type(nota) == Nota:
            if nota not in self:
                print(f"Nota nueva agregada: {nota.titulo} | {nota.medio}")
                self.append(nota)

        
    def agregarLista(self, otro):
        nota : Nota
        for nota in otro:
            self.agregarNota(nota)
        return self


def main():
    pass 

if __name__ == "__main__":
    main()  