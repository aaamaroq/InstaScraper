

# Instagram Node Generator and K-Means Clustering

Este proyecto tiene como objetivo la generación de un grafo de nodos a partir del scraping de perfiles de Instagram. El grafo resultante representa todas las relaciones entre seguidores y seguidos en la red social. Además, incluye un algoritmo de clasificación basado en K-Means para agrupar estos nodos por colores, identificando grupos cercanos en la red. Este proyecto se ha desarrollado por motivos de estudio y curiosidad.

## Funcionalidad

El proyecto consta de dos partes principales:

1. **Generación de Nodos de Instagram**: El script en Python se encarga de extraer información de perfiles de Instagram a través de técnicas de scraping. Esto resulta en la creación de un grafo que representa las relaciones entre los seguidores y seguidos de una cuenta de Instagram.

2. **Clasificación con K-Means**: Una vez que se ha generado el grafo, el proyecto utiliza el algoritmo de K-Means para agrupar los nodos en diferentes categorías por colores. Esto permite identificar grupos de usuarios que tienen relaciones cercanas en la red social.

![image](https://github.com/aaamaroq/InstaScraper/assets/100299154/193a7828-0bbd-4324-b89f-17458b55e78f)


## Cómo utilizar

Para ejecutar el proyecto, sigue estos pasos:

1. Clona este repositorio en tu máquina local.
2. Asegúrate de que tienes las siguientes dependencias instaladas:
   - Python3
   - [instaloader](https://instaloader.github.io/)
   - numpy
3. Abre una terminal y navega hasta la carpeta del proyecto.
4. Ejecuta el siguiente comando, reemplazando `<USERNAME>` y `<PASSWORD>` con tus credenciales de Instagram:

   ```bash
   python main.py --username <USERNAME> --password <PASSWORD>
   ```

   Si tu contraseña contiene caracteres especiales, asegúrate de escaparlos correctamente con "\".

5. El script generará un archivo llamado `unfollowers_<USERNAME>.txt` en tu directorio, que contendrá la lista de personas a quienes dejar de seguir en tu cuenta de Instagram.

## Notas

- Este proyecto no es compatible con cuentas que tengan habilitada la autenticación de dos factores.

¡Esperamos que este proyecto te resulte útil y te inspire a explorar las redes sociales desde una perspectiva más analítica! Si tienes alguna pregunta o sugerencia, no dudes en crear un problema en este repositorio o ponerte en contacto con el autor.

¡Diviértete explorando las relaciones en Instagram con este generador de nodos y clasificador K-Means!
