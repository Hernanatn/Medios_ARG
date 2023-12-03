from dependencias.Informes import Informe
from dependencias.Medios import listarNotas, listadorPerfil, listadorLPO, listadorDestape, listadorLN, listadorClarin, listadorP12, listadorInfobae, listadorAmbito, CategoriasNota, ResultSet
from datetime import date, datetime
    
# Se define una función categorizadora de notas para proveer al informe.
def miCategorizador(etiquetas:ResultSet, subBusqueda : str = None) -> CategoriasNota:
    etiquetasNota   : set[str] = set()
    relevanciaNota  : int = 0
    bloqueNota      : str = ""

    etiqueta : Tag
    for etiqueta in etiquetas:
        if subBusqueda:
            etq :str =  etiqueta\
                        .find(subBusqueda)\
                        .get_text(strip=True)
        else:
            etq :str =  etiqueta\
                        .getText(strip=True)

        etiquetasNota.add(etq)

    TIENE_MESSI   : bool = len(list(etq for etq in etiquetasNota if "messi" in etq.lower())) > 0
    TIENE_DIEGO   : bool = len(list(etq for etq in etiquetasNota if "maradona" in etq.lower())) > 0

    if TIENE_MESSI  : bloqueNota = "Fútbol"; relevanciaNota += 10
    if TIENE_DIEGO  : bloqueNota = "Fútbol"; relevanciaNota += 10

    TIENE_MALVINAS  : bool = len(list(etq for etq in etiquetasNota if ("malvinas" in etq.lower() or "kelpers" in etq.lower() or "gran malvina" in etq.lower()))) > 0

    if  TIENE_MALVINAS  : bloqueNota = "Geopolítica" ; relevanciaNota += 10
    
    return etiquetasNota, relevanciaNota, bloqueNota


def main():
    FECHA_HOY           : str = date.today().strftime('%Y-%m-%d')
    HORA_AHORA                = datetime.today().time()

    print(f"[DEBUG] Iniciado Relevo de Medios:{FECHA_HOY} | {HORA_AHORA}")
    
    RUTA_INFORME_HOY    : str = f"Relevamiento_Medios_{FECHA_HOY}.csv"
    informeNuevo    : Informe = Informe.desdeCSV()

    informeNuevo                                                          \
        .agregarLista( listarNotas( listadorPerfil , miCategorizador ) )   \
        .agregarLista( listarNotas( listadorLPO    , miCategorizador ) )    \
        .agregarLista( listarNotas( listadorDestape, miCategorizador ) )     \
        .agregarLista( listarNotas( listadorLN     , miCategorizador ) )      \
        .agregarLista( listarNotas( listadorClarin , miCategorizador ) )       \
        .agregarLista( listarNotas( listadorP12    , miCategorizador ) )        \
        .agregarLista( listarNotas( listadorInfobae, miCategorizador ) )         \
        .agregarLista( listarNotas( listadorAmbito , miCategorizador ) )          \

    informeNuevo.crearMensajeWPP()
    informeNuevo.crearCSV()

    print(f"[DEBUG] Concluído Relevo de Medios: {FECHA_HOY} | {HORA_AHORA}")


if __name__ == "__main__":
    main()
