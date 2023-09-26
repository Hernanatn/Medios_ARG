from bs4 import BeautifulSoup, ResultSet, Tag, NavigableString
from requests import get as GET
from re import sub as reemplazar

def buscarBS4(url:str,etiqueta:str,atributos:dict = None,**atributosKw)-> Tag | NavigableString | None:
    
    html : str = GET(url).text #texto html de la página
    sopa : BeautifulSoup = BeautifulSoup (html,"html.parser") #creación del objeto BeautifulSoup

    if not atributos:
        dictAtributos : dict = {}
        for id, dato in atributosKw.items():
            dictAtributos[reemplazar("_","",id)] = dato
    else:
        dictAtributos : dict = atributos
    
    try:
        busqueda : ResultSet = sopa.find( 
                                        name=etiqueta,  
                                        attrs=dictAtributos
                                        )
                                        
    except Exception as e:
        print(f"[ERROR] Hubo un error al realizar la búsqueda:\n{e}\n\n")
        busqueda = None  

    return busqueda


def buscarTodosBS4(url:str,etiqueta:str,atributos:dict = None,**atributosKw)->ResultSet:
    
    html : str = GET(url).text

    sopa : BeautifulSoup = BeautifulSoup (html,"html.parser") 

    if not atributos:
        dictAtributos : dict = {}
        for id, dato in atributosKw.items():
            dictAtributos[reemplazar("_","",id)] = dato
    else:
        dictAtributos : dict = atributos
    
    try:
        busqueda : ResultSet = sopa.find_all( 
                                            name=etiqueta,  
                                            attrs=dictAtributos
                                            )
                                        
    except Exception as e:
        print(f"[ERROR] Hubo un error al realizar la búsqueda:\n{e}\n\n")
        busqueda = None  

    return busqueda


def main():
    pass

if __name__ == "__main__":
    main()
