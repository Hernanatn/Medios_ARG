from datetime import date, datetime
from dependencias.utiles.utilesBS4 import buscarTodosBS4, buscarBS4, ResultSet, Tag
from dependencias.Notas import Nota,ListaNotas
from re import search
from typing import Callable

#-----------ALIAS TIPOS-----------#

CategoriasNota  = tuple[set[str],int,str]
Categorizador   = Callable[[ResultSet,str],CategoriasNota]
Listador        = Callable[[Categorizador],ListaNotas]


#-----------FUNCIONES INTERFAZ-----------#

def listarNotas( listadorMedio : Listador, categorizadorNotas : Categorizador) -> ListaNotas: 
    return listadorMedio( categorizadorNotas )

#-----------LISTADORES MEDIOS ARGENTINOS-----------#

def listadorPerfil (categorizadorNotas : Categorizador) -> ListaNotas:
    '''
    :param categorizadorNotas:  [Callable] : La función de categorización de notas que el "scrapper" aplicará a cada objeto de tipo Nota. La función debe tomar como parámetros el ResultSet de etiquetas recuperadas con BS4 y (opcionalmente) la "Tag" de sub-búsqueda para cada etiqueta de la nota. Debe devolver un tuple[list[str],int,str] representando: la lista de etiquetas, el grado de relevancia y el bloque temático de la nota.
    :return: [ListaNotas] : Objeto de tipo ListaNotas que contiene las notas de la sección política del portal web del diario Perfil de la fecha de ejecución.
    '''
    MEDIO : str = "Perfil"
    PERFIL_POLITICA : str = "https://www.perfil.com/seccion/politica"

    listaDeNotasHoy : ListaNotas = ListaNotas()
    notasPerfil : ResultSet = buscarTodosBS4(url=PERFIL_POLITICA,etiqueta="article",atributos={"class" : "news--clear-hover"})
    nota : Tag
    for nota in notasPerfil:
        contenido : Tag =   nota    \
                            .find("a")
         
        infoNota : Tag =    contenido   \
                            .find(
                            name = "div",
                            attrs = {"class" : "news__data"})

        urlNota : str = (contenido['href']) 
        tituloNota : str =  infoNota    \
                        .find(name = "h2",
                              attrs = {"class":"news__title"})  \
                        .get_text(strip=True)
        
        fechaNota : date =  datetime.strptime(
                            infoNota    \
                            .find(name = "time",
                                attrs = {"class":"news__datetime"})  \
                            ['datetime'],
                            "%Y-%m-%dT%H:%M:%S%z"
                        ).date()

        etiquetas : ResultSet = buscarTodosBS4(url=urlNota,etiqueta="li",atributos={"class":"article__tags__item"})
        etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas,"a")

        #print(f"[DEBUG] {tituloNota = }")
        #print(f"[DEBUG] {urlNota = }")
        try:
            volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "article__headline"})\
                                .get_text(strip=True)
        except:
            continue

        if fechaNota >= date.today(): 
            estaNota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
            listaDeNotasHoy.agregarNota(estaNota)

    listaDeNotasHoy.sort()
    return listaDeNotasHoy

def listadorLPO (categorizadorNotas : Categorizador) -> ListaNotas:
    
    MEDIO : str = "LPO"
    LPO_POLITICA : str = "https://www.lapoliticaonline.com/seccion/politica/"
    LPO_ECONOMIA : str = "https://www.lapoliticaonline.com/seccion/economia/"

    def buscarNotasLPO(link) -> ListaNotas:
        listaDeNotasHoy : ListaNotas = ListaNotas()
        notasLPO : ResultSet = buscarTodosBS4(url=link,etiqueta="div",atributos={"class" : "item noticia-ar"})
        nota : Tag
        for nota in notasLPO: 
            contenido : Tag =   nota  \
                                .find(name = "h2",
                                attrs = {"class":"title"})  \
                                .find(name ="a")    \


            urlNota : str = "https://www.lapoliticaonline.com/"+contenido['href'] 
            tituloNota : str =  contenido.get_text(strip=True)

            volantaNota: str = ""\




            etiquetas : ResultSet = buscarTodosBS4(url=urlNota,etiqueta="a",atributos={"class":"tag"})
            etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas)

            fechaLPO : str = buscarBS4(url=urlNota,etiqueta="span",atributos={"class":"time"}) \
                            .get_text(strip=True)
            if "HOY" in fechaLPO or "Hace" in fechaLPO:
                fechaNota : date = date.today() 
            else:
                fechaNota : date =  datetime.strptime(
                                fechaLPO,
                                "%d/%m/%Y"
                            ).date()            

            volantaNota : str = buscarBS4(url=urlNota,etiqueta="div",atributos={"class" : "description"})   \
                                .get_text(strip=True)

            if fechaNota >= date.today(): 
                estaNota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
                listaDeNotasHoy.agregarNota(estaNota)

        listaDeNotasHoy.sort()
        return listaDeNotasHoy

    listaNotas = ListaNotas()
    listaNotas  \
        .agregarLista(buscarNotasLPO(LPO_POLITICA)) \
        .agregarLista(buscarNotasLPO(LPO_ECONOMIA))
    
    return listaNotas
           
def listadorDestape (categorizadorNotas : Categorizador) -> ListaNotas:

    MEDIO : str = "El Destape"
    URL_DESTAPE : str = "https://www.eldestapeweb.com" 
    DESTAPE_POL : str = "/seccion/politica"
    DESTAPE_ECON : str = "/seccion/economia"        

    def traducirMes(mes: str) -> str:
        meses = {
            "enero"      : '01',
            "febrero"    : '02',  
            "marzo"      : '03',   
            "abril"      : '04',
            "mayo"       : '05',
            "junio"      : '06',
            "julio"      : '07',
            "agosto"     : '08',
            "septiembre" : '09',
            "octubre"    : '10',
            "noviembre"  : '11',
            "diciembre"  : '12',
        }
        try:
            mes_00 = f'{meses[mes.lower()]}'
            return (mes_00)
        except:
            raise ValueError(
                'ERROR: Se intento correr la función "traducirMes" sin proporcionar un valor adecuado. La función solo acepta cadenas de caracteres que contengan el nombre en español de un mes')
    
    def traducirFecha(fecha : str) -> str:
        dia : str = search(pattern="\d\d?",string=fecha)[0]
        mes : str = traducirMes(search(pattern=".*?de (.*),.*",string=fecha.lower()).group(1))
        ano : str = search(pattern="\d\d\d\d?",string=fecha)[0]
        fechaTraducida : str = f"{dia}/{mes}/{ano}"
        return fechaTraducida


    def buscarNotasDestape(link) -> ListaNotas:
        listaDeNotasHoy : ListaNotas = ListaNotas()
        notasDestape : ResultSet = buscarTodosBS4( url       =   link,
                                                   etiqueta  =   "article",
                                                   atributos =   {"class" : "nota"})
        nota : Tag
        for nota in notasDestape: 
            data : Tag =   nota  \
                                .find(name = "div",
                                attrs = {"class":"data"})


            infoTitulo : Tag =  data \
                                .find(name="div",
                                      attrs= {"class" : "titulo"} ) \
                                .find(name="h2")     \
                                .find(name="a")

            urlNota : str = f"{URL_DESTAPE}{infoTitulo['href']}" 

            tituloNota : str =  infoTitulo \
                                .get_text(strip=True)
            
            etiquetas : ResultSet = buscarBS4(url=urlNota,etiqueta="div",atributos={"class":"tags"})   \
                                    .find(name="ul",attrs={"class":"palabras"}) \
                                    .find_all(name="li")
            etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas)

            fecha : Tag = buscarBS4(url=urlNota,etiqueta="div",atributos={"class":"fecha"})\

            try:
                fecha.find("p").find("b")
                fechaNota = date.today()
            
            except AttributeError:
                fechaDestape : str = fecha\
                                .find("span") \
                                .get_text(strip=True)

         
                fechaNota : date =  datetime.strptime(
                                traducirFecha( fechaDestape ),
                                "%d/%m/%Y"
                            ).date()            
            try:
                volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "intro"})   \
                                    .get_text(strip=True)
            except:
                volantaNota : str = ""

            if fechaNota >= date.today(): 
                estaNota = Nota(fecha=fechaNota,url=urlNota,medio=MEDIO,titulo=tituloNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
                listaDeNotasHoy.agregarNota(estaNota)

        listaDeNotasHoy.sort()
        return listaDeNotasHoy

    listaNotas = ListaNotas()
    listaNotas  \
        .agregarLista(buscarNotasDestape(f"{URL_DESTAPE}{DESTAPE_POL}")) \
        .agregarLista(buscarNotasDestape(f"{URL_DESTAPE}{DESTAPE_ECON}"))
    
    return listaNotas
        
def listadorLN (categorizadorNotas : Categorizador) -> ListaNotas:
    
    MEDIO : str = 'La Nación'
    URL_LN : str = 'https://www.lanacion.com.ar'
    LN_POL : str = '/politica/'

    listaDeNotasHoy : ListaNotas = ListaNotas()

    def traducirMes(mes: str) -> str:
        meses = {
            "enero"      : '01',
            "febrero"    : '02',  
            "marzo"      : '03',   
            "abril"      : '04',
            "mayo"       : '05',
            "junio"      : '06',
            "julio"      : '07',
            "agosto"     : '08',
            "septiembre" : '09',
            "octubre"    : '10',
            "noviembre"  : '11',
            "diciembre"  : '12',
        }
        try:
            mes_00 = f'{meses[mes.lower()]}'
            return mes_00
        except:
            raise ValueError(
                'ERROR: Se intento correr la función "traducirMes" sin proporcionar un valor adecuado. La función solo acepta cadenas de caracteres que contengan el nombre en español de un mes')
    
    def traducirFecha(fecha : str) -> str:
        dia : str = search(pattern  =   "\d\d?",
                           string   =   fecha)[0]
       
        mes : str = traducirMes(search(pattern  =   ".*?de (.*) de.*",
                                       string   =   fecha.lower())      \
                                .group(1))
        
        ano : str = search(pattern  =   "\d\d\d\d?",
                           string   =   fecha)[0]
        
        fechaTraducida : str = f"{dia}/{mes}/{ano}"
        return fechaTraducida

    notasLN : ResultSet = buscarTodosBS4( url        =   f"{URL_LN}{LN_POL}",
                                          etiqueta   =   "article",
                                          atributos  =   {"class" : "mod-article"})
    
    nota : Tag
    for nota in notasLN: 
        data : Tag =   nota                     \
                        .find(name = "section",
                        attrs = {"class":"mod-description"})
        
        #titulo
        try: #Por como está diseñada la página de La Nación, se pre-renderizan en el html algunos "articles" que aún no están visibles y no tienen info. 
            infoTitulo : Tag =  data               \
                                .find(name="h2")    \
                                .find(name="a")
        except AttributeError: # Si se llegó a una nota invisible, se asume que se levantaron todas las notas "más actuales" y se corta el ciclo
            break

        urlNota : str = f"{URL_LN}{infoTitulo['href']}" 

        tituloNota : str =  infoTitulo['title']
        
        etiquetas : ResultSet = buscarTodosBS4(url=urlNota,etiqueta="a",atributos={"class":"--tag"})
        etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas)

        #fecha
        try: 
            fecha : Tag = buscarBS4(url=urlNota,etiqueta="span",atributos={"class":"mod-date"})\
                            .find("time",{"class":"com-date"}) \
                            .get_text(strip=True)
        except AttributeError:
            continue
    
        fechaNota : date =  datetime.strptime(
                        traducirFecha( fecha ),
                        "%d/%m/%Y"
                    ).date()            

        try:
            volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "--bajada"})   \
                                .get_text(strip=True)
        except AttributeError:
            volantaNota=""

        if fechaNota >= date.today(): 
            estaNota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
            listaDeNotasHoy.agregarNota(estaNota)

    listaDeNotasHoy.sort()
    return listaDeNotasHoy

def listadorClarin(categorizadorNotas : Categorizador) -> ListaNotas:

    MEDIO : str = "Clarín"

    URL_CLARIN = 'https://www.clarin.com'
    CLARIN_POL = '/politica/'
    listaDeNotasHoy : ListaNotas = ListaNotas()
    
    notasClarin : ResultSet = buscarTodosBS4( url        = f"{URL_CLARIN}{CLARIN_POL}",
                                              etiqueta   = "article",
                                              atributos  = {"class" : "content-nota"})
    
    nota : Tag
    for nota in notasClarin:
        urlNota : str = f"{URL_CLARIN}"+        \
                            nota                 \
                            .find(
                                name = 'a',
                                recursive = False)  \
                            ['href']
        
        tituloNota : str =  nota                      \
                            .find(name = "div",
                                attrs = {"class":"mt"}) \
                            .find("h2")\
                            .get_text(strip=True)
        
        fechaNota : date =  datetime.strptime(
                            buscarBS4(urlNota,
                                      etiqueta = "div",
                                      atributos = {
                                        "class" : "entry-breadcrumb"})  \
                            .find(name = "span")                         \
                            .get_text(strip = True),
                            "%d/%m/%Y %H:%M"
                            ).date()

        etiquetas : ResultSet = buscarBS4(
                                url = urlNota,
                                etiqueta = "div",
                                atributos = {
                                            "class":"entry-tags"
                                            })  \
                                .find("ul")      \
                                .find_all("li")
        etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas)


        try:
            volantaNota : str = buscarBS4(url=urlNota,etiqueta="div",atributos={"class" : ["title","check-space"]})   \
                                .find(name="div",attrs={"class":"mt"})                                                 \
                                .find(name="h2")                                                                         \
                                .get_text(strip=True)        
        except:
            volantaNota : str = ""

        if fechaNota >= date.today(): 
            estaNota : Nota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota)
            listaDeNotasHoy.agregarNota(estaNota)

    listaDeNotasHoy.sort()
    return listaDeNotasHoy
    
def listadorP12 (categorizadorNotas : Categorizador) -> ListaNotas:
    
    MEDIO : str = "Página/12"

    URL_P12 : str = 'https://www.pagina12.com.ar/'
    P12_POL : str = '/secciones/el-pais'

    listaDeNotasHoy : ListaNotas = ListaNotas()

    def traducirMes(mes: str) -> str:
        meses = {
            "enero"      : '01',
            "febrero"    : '02',  
            "marzo"      : '03',   
            "abril"      : '04',
            "mayo"       : '05',
            "junio"      : '06',
            "julio"      : '07',
            "agosto"     : '08',
            "septiembre" : '09',
            "octubre"    : '10',
            "noviembre"  : '11',
            "diciembre"  : '12',
        }
        try:
            mes_00 = f'{meses[mes.lower()]}'
            return mes_00
        except:
            raise ValueError(
                'ERROR: Se intento correr la función "traducirMes" sin proporcionar un valor adecuado. La función solo acepta cadenas de caracteres que contengan el nombre en español de un mes')
    
    def traducirFecha(fecha : str) -> str:
        dia : str = search(pattern  =   "\d\d?",
                           string   =   fecha)[0]
       
        mes : str = traducirMes(search(pattern  =   ".*?de (.*) de.*",
                                       string   =   fecha.lower())      \
                                .group(1))
        
        ano : str = search(pattern  =   "\d\d\d\d?",
                           string   =   fecha)[0]
        
        fechaTraducida : str = f"{dia}/{mes}/{ano}"
        return fechaTraducida

    notasP12 : ResultSet = buscarTodosBS4( url        =   f"{URL_P12}{P12_POL}",
                                          etiqueta   =   "div",
                                          atributos  =   {"class" : "article-item__content-footer-wrapper"})
    
    nota : Tag
    for nota in notasP12: 
        data : Tag =   nota                     \
                        .find(name = "div",
                        attrs = {"class":"article-item__content"})

        try:
            infoTitulo : Tag =  data               \
                                .find(name="h2")    \
                                .find(name="a")
        except AttributeError:
            try:
                infoTitulo : Tag =  data               \
                                    .find(name="h3")    \
                                    .find(name="a")
            except AttributeError:
                try:
                    infoTitulo : Tag =  data               \
                                        .find(name="h4")    \
                                        .find(name="a")
                except AttributeError:
                    continue

        urlNota : str = f"{URL_P12}{infoTitulo['href']}" 

        tituloNota : str =  infoTitulo          \
                            .get_text(strip=True)

        #fecha
 
        fechaP12 : str =   nota                                     \
                    .find(name  = "div",
                          attrs = {"class" : "article-item__footer"}) \
                    .find(name  = "div",
                          attrs = {"class" : "date"})                   \
                    .get_text(strip = True)
    
        fechaNota : date =  datetime.strptime(
                            traducirFecha( fechaP12 ),
                            "%d/%m/%Y"
                            ).date()            
        
        etiquetas : ResultSet = buscarTodosBS4(url=urlNota,etiqueta="a",atributos={"class":"tag"})
        etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas)

        try:
            volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "h3"})   \
                                .get_text(strip=True)        
        except:
            try:
                volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "h4"})   \
                                    .get_text(strip=True)        
            except:
                volantaNota : str = ""

        if fechaNota >= date.today(): 
            estaNota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
            listaDeNotasHoy.agregarNota(estaNota)

    listaDeNotasHoy.sort()
    return listaDeNotasHoy

def listadorAmbito (categorizadorNotas : Categorizador) -> ListaNotas:
    
    MEDIO : str = "Ámbito"

    URL_AMB : str = 'https://www.ambito.com/'
    AMB_POL : str = '/contenidos/politica.html'

    listaDeNotasHoy : ListaNotas = ListaNotas()

    def traducirMes(mes: str) -> str:
        meses = {
            "enero"      : '01',
            "febrero"    : '02',  
            "marzo"      : '03',   
            "abril"      : '04',
            "mayo"       : '05',
            "junio"      : '06',
            "julio"      : '07',
            "agosto"     : '08',
            "septiembre" : '09',
            "octubre"    : '10',
            "noviembre"  : '11',
            "diciembre"  : '12',
        }
        try:
            mes_00 = f'{meses[mes.lower()]}'
            return mes_00
        except:
            raise ValueError(
                'ERROR: Se intento correr la función "traducirMes" sin proporcionar un valor adecuado. La función solo acepta cadenas de caracteres que contengan el nombre en español de un mes')
    
    def traducirFecha(fecha : str) -> str:
        dia : str = search(pattern  =   "\d\d?",
                           string   =   fecha)[0]
       
        mes : str = traducirMes(search(pattern  =   ".*?de ([a-zA-Z]*)",
                                       string   =   fecha.lower())      \
                                .group(1))
        
        ano : str = search(pattern  =   "\d\d\d\d?",
                           string   =   fecha)[0]
        
        fechaTraducida : str = f"{dia}/{mes}/{ano}"
        return fechaTraducida

    notasAmbito : ResultSet = buscarTodosBS4( url        =   f"{URL_AMB}{AMB_POL}",
                                          etiqueta   =   "article",
                                          atributos  =   {"class" : "news-article"})
    
    nota : Tag
    for nota in notasAmbito: 

        data : Tag =   nota                     \
                        .find(name = "div",
                        attrs = {"class":"news-article__info-wrapper"})
        
        infoTitulo : Tag =  data               \
                            .find(name="h2")    \
                            .find(name="a")

        urlNota : str = f"{infoTitulo['href']}" 

        tituloNota : str =  infoTitulo.get_text(strip = True)
        
        etiquetas : ResultSet = buscarTodosBS4(url=urlNota,etiqueta="li",atributos={"class":"news-topics__list-item"})
        etiquetasNota,relevanciaNota,bloqueNota = categorizadorNotas(etiquetas,"a")

        try: 
            fecha : Tag =   buscarBS4(url=urlNota,etiqueta="span",atributos={"class":"news-headline__publication-date"})\
                            .get_text(strip=True)

            
        except AttributeError:
            continue
    
        fechaNota : date =  datetime.strptime(
                        traducirFecha( fecha ),
                        "%d/%m/%Y"
                    ).date()            

        try:
            volantaNota : str = buscarBS4(url=urlNota,etiqueta="h2",atributos={"class" : "news-headline__article-summary"})   \
                                .get_text(strip=True)        
        except:
            volantaNota : str = ""

        if fechaNota >= date.today(): 
            estaNota = Nota(url=urlNota,medio=MEDIO,titulo=tituloNota,fecha=fechaNota,etiquetas=etiquetasNota,relevancia=relevanciaNota,bloque=bloqueNota,volanta=volantaNota)
            listaDeNotasHoy.agregarNota(estaNota)

    listaDeNotasHoy.sort()
    return listaDeNotasHoy

def listadorInfobae(categorizadorNotas : Categorizador) -> ListaNotas: return None     #[TODO]


def main():
    pass


if __name__=="__main__":
    main()




