# Examen_2do_Parcial_MMDD
Examen de segundo parcial de la materia Manejo Masivo de Datos

## Explica la diferencia entre los modos standalone, pseudo-distribuido y totalmente distribuido de Hadoop. ¿En cuál de ellos se usa HDFS?
En *Standalone* Hadoop trabaja en una sola maquina, ejecutando MapReduce en un proceso local y utilizando exclusivamente el sistema de archivos del sistema operativo, en mi caso Windows, sin HDFS.

## ¿Por qué el dataset se monta como volumen y no se copia dentro de la imagen con COPY? Menciona al menos dos razones.
Montar el dataset como volumen lo que hace es permitir separar los datos de la imagen del contenedor, evitando tener que reconstruirla cada vez que el archivo cambia. Además, permite reutilizar el mismo dataset entre diferentes contenedores y facilita administrar archivos más grandes. Evita aumentar innecesariamente el tamaño de la imagen Docker.

## ¿Qué ocurre con los datos de la base de datos al ejecutar docker compose down? ¿Y con docker compose down -v?
Cuando ejecutamos docker compose down, se detienen todos los contenedores y la red y se eliminan, pero los volumenes nombrados permanecen intactos, por lo que los datos de PostgreSQL se conservan. En cambio, al ejecutar docker compose down -v, también se eliminan los volúmenes asociados al proyecto, provocando la pérdida de los datos almacenados en ellos.

## ¿Por qué MapReduce no siempre es más rápido que un script secuencial con un archivo de 400 MB? ¿A partir de qué condiciones conviene?
Mapreduce no siempre es la opcion mas rapida porque necesita un tiempo para iniciar los procesos, dividir los datos, realizar el shuffle y combinar los resultados. En caso de archivos más pequeños, un script secuencial puede terminar más rápido al evitar estos procesos. MapReduce conviene cuando se manejan grandes volúmenes de datos que pueden distribuirse en varios nodos y procesarse en paralelo.

## Diferencia entre CMD y ENTRYPOINT, y entre COPY y ADD.
CMD define el comando o los argumentos predeterminados que ejecutará el contenedor y puede ser reemplazado al iniciarlo.
ENTRYPOINT define el ejecutable principal del contenedor y permite establecer qué programa se ejecutará al iniciar.
COPY copia los archivos o directorios desde el contexto de construcción hacia la imagen Docker.
ADD también copia archivos, pero adicionalmente permite descargar recursos mediante URL y extraer automáticamente archivos comprimidos compatibles.
