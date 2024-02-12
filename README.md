# TFG ALVARO DOMINGUEZ PAÑOS UC3M

# CLASIFICADOR DE GESTOS DE LA MANO
## BASADO EN EL BRAZALETE DE MINDROVE

## EXPLICACIÓN REPOSITORIO
En este repositorio se encuentran los códigos y entrenamientos que se han implementado para conseguir desarrollar un clasificador de gestos de la mano mediante señales EMG. Estudio realizado como TFG por Álvaro Domínguez Paños para la universidad UC3M.

## CODIGOS RECURSO

En este directorio se pueden encontrar los código necesarios para la adquisición de datos para formar la base de datos.

[**adquisicion.py**](CODIGOS%20RECURSO/adquisicion.py)
Sirve para la ejecución de una lectura de datos durante un `tiempo_limite`, y almacenando los **MAV Mean Absolute Value**, de las **señales EMG**, **acelerómetro** y **giroscopio**, en un archivo `.csv`.


[**all_adquisicion.py**](CODIGOS%20RECURSO/all_adquisicion.py)
Sirve para realizar el protocolo de adquisición de datos de manera automática tal y como se indica en el documento.


## DATOS
En este directorio se encuentran todos los datos adquiridos para los entrenamientos. Se dividen por carpetas en función del `window_size` usado, además también se incluye el archivo con los datos concatenados, y los datos usados para el test de generalización. También se incluye un directorio con algunos de los datos atípicos que muestran lecturas incongruentes por parte del brazalete.

## ALL ENTRENAMIENTOS
En este directorio se encuentran todos los entrenamientos que se han hecho a lo largo del proyecto, y se consideran parte del estudio, y no han sido de mera investigación, en busca del mejor clasificador. Además también se incluyen, los tests de la capacidad de generalización a datos nuevos de los modelos generados durante el entrenamiento.

## ENTRENAMIENTOS RELEVANTES
En este directorio se encuentran los entrenamientos que han supuesto un impacto en el proyecto, esto se incluye para separarlo del resto de entrenamientos que no han resultado exitosos.

## MEJOR MODELO
En esta carpeta se encuentra el entrenamiento del mejor modelo, y el mejor clasificadores, separado del resto para que sea más sencillo de localizar.

## DEMO APP
En este directorio se encuentra la aplicación demo, un serious game sencillo para la ejecución de clasificador en tiempo real. Se incluyen dos códigos distintos, [**demo.py**](DEMO%20APP/demo.py) para la ejecución de un clasificador con 4 gestos, el mejor clasificador en este caso, y también se incluye un código para la ejecución de un clasificador de 7 gestos, [**demo_7G.py**](DEMO%20APP/demo_7G.py)

## JUEGO 1
En este caso se encuentran los códigos para la ejecución del serious game en dos ordenadores distintos, uno para hacer uso del clasificador y otro para hacer uso del juego, así poder repartir los recursos necesarios para la ejecución, principalmente para otros juego que requieran mejores recursos. Esto es posible gracias a una conexión con un socket TCP/IP. En este caso el [**cliente.py**](JUEGO%201/cliente.py), ejecuta el clasificador y envía un mensaje con la nueva predicción. Por otro lado [**server.py**](JUEGO%201/server.py), el servidor se encarga de recibir el nuevo gestos e interactuar con este en el juego.

## JUEGO 2
Por último se ha desarrollado un segundo juego que consiste en hacer el gesto que se ha generado de manera aleatoria, este juego funciona de la misma forma que el anterior, mediante TCP/IP, y hace uso de una interfaz gráfica muy sencilla para la visualización. 

## LINKS
Además se puede encontrar una ejecución tanto del [**mejor modelo**](https://youtu.be/bM__-uxg694) y de otros de los modelos entrenamientos relevantes para el proyecto, [**ejecucines descartadas**](https://youtu.be/rQ9JOnSBLYA)
