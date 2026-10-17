# Inkdex
**Tu biblioteca, siempre a mano.**

Inkdex es una aplicación web ligera para explorar y descargar libros de una biblioteca de [Calibre](https://calibre-ebook.com/) desde el navegador de distintos dispositivos.

Su principal objetivo es permitir el acceso a una biblioteca existente de Calibre **sin necesidad de iniciar el servidor de contenido de Calibre**. También está pensado para lectores Kindle: permite explorar el catálogo y descargar contenido desde el navegador integrado, sin necesidad de instalar KOReader ni aplicaciones similares.

## ¿Por qué Inkdex?

Calibre es una excelente herramienta para organizar bibliotecas digitales. Inkdex complementa esa experiencia con una interfaz web sencilla para consultar la biblioteca desde otros dispositivos de la red local.

- No necesita iniciar el servidor de contenido de Calibre.
- Permite acceder desde el navegador integrado de Kindle u otros dispositivos, incuyendo E-Readers.
- No requiere instalar una aplicación cliente en cada dispositivo.
- Utiliza la biblioteca de Calibre que ya existe; no hace falta migrar los libros a otro sistema.

## Características

- **Catálogo visual:** consulta títulos, autores y portadas.
- **Búsqueda:** encuentra libros por título o autor.
- **Filtros combinables:** filtra por autor, serie y etiqueta.
- **Ordenamiento:** ordena los resultados por título ascendente, título descendente, autor o fecha.
- **Detalles del libro:** consulta la información disponible, las series, las etiquetas y los formatos.
- **Descargas:** descarga archivos disponibles en la biblioteca.
- **Acceso desde Kindle:** utiliza el navegador integrado del dispositivo.
- **Windows y Linux:** incluye scripts para iniciar y detener el servidor.
- **Acceso desde la red local:** utiliza un navegador web en el dispositivo cliente.

## Cómo funciona

Inkdex consulta los metadatos de una biblioteca existente de Calibre y sirve una interfaz web independiente. No reemplaza Calibre y no necesita que su servidor de contenido esté activo.

```text
        Biblioteca existente de Calibre
                      |
                      v
               Servidor Inkdex
                      |
               Red local (Wi-Fi)
                      |
          +-----------+-----------+
          |           |           |
        Kindle     Teléfono        PC
      (navegador) (navegador)  (navegador)
```

La computadora anfitriona debe poder acceder a la carpeta de la biblioteca. Los demás dispositivos acceden al servidor mediante la dirección IP local de esa computadora.

## Requisitos

- Python 3 y las dependencias del proyecto.
- Una biblioteca de Calibre existente y accesible.
- Conectividad de red entre la computadora anfitriona y los dispositivos clientes.

## Instalación

### 1. Obtener el proyecto

Clona el repositorio o descarga el código fuente:

```bash
git clone https://github.com/inkDexProject/inkDex
cd inkDex
```

### 2. Configurar la biblioteca de Calibre

Crea un archivo local `config.py` tomando como referencia `config_example.py`.

Configura la ruta de la biblioteca mediante `RUTA_CALIBRE_POR_DEFECTO` o la variable de entorno `INKDEX_CALIBRE_LIBRARY`. La ruta debe apuntar a la carpeta que contiene `metadata.db`.


### 3. Iniciar Inkdex

Los scripts de inicio preparan el entorno virtual cuando hace falta, comprueban e instalan las dependencias e inician el servidor en segundo plano.

**Windows**

Ejecuta:

```text
iniciar_inkDex.bat
```

**Linux**

Desde la carpeta del proyecto:

```bash
chmod +x iniciar_inkDex.sh
./iniciar_inkDex.sh
```

El lanzador muestra las direcciones disponibles para acceder a Inkdex.

### 4. Detener Inkdex

Para detener el servidor, utiliza el script correspondiente:

- **Windows:** `detener_inkDex.bat`
- **Linux:** `detener_inkDex.sh`

Inkdex se inicia y detiene manualmente. De ser necesario, puedes configurarlo para que arranque automáticamente con el sistema operativo.

## Acceso desde Kindle y otros dispositivos

Una vez iniciado Inkdex, utiliza la dirección IP local que muestra el lanzador. Desde el navegador del Kindle, teléfono, tablet u otra computadora conectada a la misma red, abre:

```text
http://IP_DE_LA_COMPUTADORA:5000
```

Reemplaza `IP_DE_LA_COMPUTADORA` por la dirección IP local de la computadora donde se ejecuta Inkdex.

Si no puedes conectarte, comprueba que ambos dispositivos estén en la misma red y que el firewall permita las conexiones necesarias.

## Seguridad y privacidad

Inkdex está pensado para utilizarse en una red local de confianza.

- La base de datos de Calibre se consulta mediante conexiones de solo lectura.
- Las consultas SQL utilizan parámetros para los valores recibidos.
- Los formatos de descarga están restringidos a una lista permitida.
- Las rutas de archivos se validan para limitar el acceso a la biblioteca.

**Importante:** Inkdex no incorpora autenticación de usuarios en su configuración actual. No lo expongas directamente a Internet sin implementar y evaluar medidas de seguridad adicionales. El tráfico HTTP tampoco está cifrado.

## Tecnologías

- Python
- Flask
- SQLite
- Waitress
- Calibre


## Autor

**José Trepat** — creador y desarrollador de Inkdex.

## Estado del proyecto

Inkdex está actualmente en desarrollo y sumando actualizaciones constantemente.

## Colaboraciones y apoyo

Inkdex es un proyecto independiente. Si te resulta útil y querés apoyar su desarrollo, podés colaborar a través de Cafecito:

[☕ Apoyar Inkdex en Cafecito](https://cafecito.app/inkdex)

También son bienvenidos los reportes de errores, las sugerencias y las contribuciones al código a través del repositorio.

---

**Inkdex — Tu biblioteca, siempre a mano.**
