1. Què fan els mètodes get_configuracio i get_persistencies?

   - get_configuracio nos permite cargar las configuraciones pasando la ruta del fichero de configuración y nos devolverá como un diccionario.

   - get_persistencies nos permite cargar las configuraciones y generar la conexion a la base de datos a partir del diccionario generado por get_configuracio. Este mètodo devolverá la conexion envolviendolo con un diccionario como container.

2. A procesa_opcio veureu instruccions com aquestes:

   ```
   return {
   "0": lambda ctx : mostra_lent("Fins la propera"),
   "1": lambda ctx : mostra_llista(ctx['llistapelis'])
   }
   ```
   Què fa lambda?

   - lambda es una funcion anónima, nos permite declarar funciones sin tener que asignarle un nombre

   Com es podria reescriure el codi sense utilitzar lambda?

   - Habría que declarar funciones y asignarles un nombre de referencia

   ```
   lambda ctx : mostra_lent("Fins la propera")
   ```
   ```
   def myfun(ctx):
        mostra_lent("Fins la propera")
   ```
   ```
   lambda ctx : mostra_llista(ctx['llistapelis'])
   ```
   ```
   def myfun2(ctx):
   	mostra_llista(ctx['llistapelis'])
   ```

   Quina utilitat hi trobeu a utilitzar lambda?

   - Cuando la funcion sólo va a ser llamada desde 1 sitio y es tan simple que no hace falta describir lo que hace con el nombre. Entonces podemos utilizar lambda para ahorrar el tiempo y trabajo

3. Penseu que s’ha desacoblat suficientment la lògica de negoci de la lògica d’aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer.

   - Sí, ya que la aplicación app_film.py se encarga todo lo que es parte de interactuar con el usuario(mostrar menú, introducir opciones, mostrar resultados) o sea la lógica de negocio. Parte de la lógica de aplicación esta bien separadas, ya que podemos crear otra aplicacion haciendo los imports de las clases necesarias para que tenga un funcionamiento totalmente diferente. 
