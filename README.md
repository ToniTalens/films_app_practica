**1.- Que fan els mètodes get_persistencia i get_configuració?**

- El mètode get_configuracio llegeix un arxiu amb configuració yml i retorna un diccionari amb la configuració d'aquest arxiu, útil per poder fer la connexió més endevant.

- El mètode get_persistencia rep el diccionari del mètode anterior, comprova si el motor és mysql o postgresql, si es així afegeix a un nou diccionari dit credencials les credencials necesaries per poder fer la connexió, retorna una instància de la classe persistencia_pelicula (mysql o postgresql) i li envia el diccionari credencials per poder que la connexió.

**2.- Que fa lambda? Com es podria reescriure el codi sense utilitzar el lambda? Quina utilitat hi trobeu a utilitzar lambda?**

- Lambda es una espècie de mapeig, mapeja opcions del menú per poder relacionar-les amb funcions específiques, quan aquestes opcions siguin seleccionades. En aquest cas el mètode rep el diccionari "context" d'aquest manera fa la crida de altres mètodes depenen de l'opció escollida. T'estalvia codi, ja que si ho haguessis de reescriure s'hauria de fer en el menú, fen les crides manualment, dins dels "if" i segurament afegint algun que altre mètode al codi.
És molt útil, ja que fa com "sub-crides", es com si el codi és dividis, i estalvia codi.

**3.- Penseu que s'ha desacoblat suficientment la lògica de negoci de la lógica d'aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer.**
 
- Si, en aquest cas el bucle_principal permet interectuar, a través de diferents opcions, amb la base de dades (lógica d'aplicació), i la classe pelicula (amb els atributs) i la classe Llistapelis que amb el mètode *llegeix_de_dic* pot consultar pelicules i guardar-les amb llistes. 
Personalment, no hi veig cap millora (ara mateix).