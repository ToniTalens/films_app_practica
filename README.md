1. **Què fan los métodos "get_configuracio" y "get_persistencies"?**
   - "get_configuracio": Este método lee un archivo de configuración (en este caso, un archivo YAML) y devuelve los datos de configuración en forma de diccionario.
   - "get_persistencies": Este método obtiene la configuración del sistema de persistencia e inicializa las instancias necesarias para la persistencia de datos.

2. **¿Qué hace "lambda"? ¿Cómo se podría reescribir el código sin utilizar "lambda"? ¿Qué utilidad encuentras en utilizar "lambda"?**
   - "lambda" es una palabra clave de Python que se utiliza para definir funciones pequeñas y anónimas. Se utiliza aquí para crear funciones simples para cada una de las opciones de la aplicación. El código se podría reescribir utilizando funciones normales en lugar de "lambda", pero el uso de "lambda" hace que el código sea más sencillo y entendible.