# PREGUNTES
## DIA 1
- Què fan els mètodes get_configuracio i get_persistencies?
    - La función get_configuracio(ruta_fitxer_configuracio) carga la configuración desde un archivo YAML dado por la ruta especificada. Utiliza la biblioteca yaml para cargar el contenido del archivo y lo devuelve como un diccionario Python.
    - La función get_persistencies(conf: dict) toma la configuración cargada como un diccionario y devuelve un diccionario que contiene objetos de persistencia según la configuración proporcionada.

- A procesa_opcio veureu instruccions com aquestes:

    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
}

- Què fa lambda? Com es podria reescriure el codi sense utilitzar lambda? Quina utilitat hi trobeu a utilitzar lambda?

- Penseu que s’ha desacoblat suficientment la lògica de negoci de la lògica d’aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer.