# Pràctica 3 UF2 M06 DAM

1. **Què fan els mètodes get_configuracio i get_persistencies?**
   El mètode get_configuracio retorna un diccionari amb les dades d'un fitxer .yml que es passa com parametre, aquest fitxer conté totes les dades de la configuració de la base de dades.

- Motor de la base de dades
- El host
- L'usuari
- La contrasenya
- El nom de base de dades
  
  
El mètode get_persistencies agafa credencials de la base de dades a partir del diccionari que s'ha creat en el mètode get_configuracio.

- En cas de que el motor de la base de dades sigui mysql crearà una instancia de la clase Persistencia_pelicula_mysql amb les credencials corresponents.
- En cas de que el motor de la base de dades sigui postgres crearà una instancia de la clase Persistencia_pelicula_pgSQL amb les credencials corresponents.

2. **A procesa_opcio veureu instruccions com aquestes:
   return {
   "0": lambda ctx : mostra_lent("Fins la propera"),
   "1": lambda ctx : mostra_llista(ctx['llistapelis'])
   }**
   **Què fa lambda? Com es podria reescriure el codi sense utilitzar lambda? Quina utilitat hi trobeu a utilitzar lambda?**

   Lambda es una funció que retorna una funcio a partir de un parametre ctx que correspon al context que es pasa al mètode. La utilitat principal de lambda es estalviar linies de codi.

---

Es podria substituir de la següent forma:
if context["opcio"] == '0': return mostra_lent("Fins la propera")
   elif context["opcio"] == '1': return mostra_llista(context["llistapelis"])
   elif context["opcio"] == '2': return mostra_llista(context["llistapelis"])
   else : return mostra_lent("opcio incorrecta!!!")

---

3. **Penseu que s’ha desacoblat suficientment la lògica de negoci de la lògica d’aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer.**
   Sí, la forma en que s'ha descoblat permet modificar facilment el codi en cas de que volguem afegir altre motor de base de dades o altres metodes.
