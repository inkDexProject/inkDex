from config import CALIBRE_LIBRARY
from database import conexion_calibre


def _resolver_ruta_segura(ruta, directorio_base):
    """Resuelve una ruta y comprueba que permanezca dentro del directorio permitido"""
    try:
        ruta_resuelta = ruta.resolve()
        ruta_resuelta.relative_to(directorio_base)
    except (ValueError, OSError, RuntimeError):
        return None

    return ruta_resuelta


def obtener_archivo_libro(book_id, formato):
    """Obtiene la ruta de un archivo de un libro si existe"""
    biblioteca = CALIBRE_LIBRARY.resolve()
    conexion = conexion_calibre()

    try:
        registro = conexion.execute(
            """
            SELECT books.path, data.name, data.format
            FROM books
            JOIN data ON data.book = books.id
            WHERE books.id = ?
              AND UPPER(data.format) = UPPER(?)
            LIMIT 1
            """,
            (book_id, formato),
        ).fetchone()
    finally:
        conexion.close()

    if registro is None:
        return None

    carpeta = _resolver_ruta_segura(
        biblioteca / registro["path"],
        biblioteca,
    )

    if carpeta is None or not carpeta.is_dir():
        return None

    archivo = _resolver_ruta_segura(
        carpeta / f"{registro['name']}.{registro['format'].lower()}",
        carpeta,
    )

    if archivo is None or not archivo.is_file():
        return None

    return archivo


def obtener_portada_libro(book_id):
    """Obtiene la portada JPG de un libro si existe"""
    biblioteca = CALIBRE_LIBRARY.resolve()
    conexion = conexion_calibre()

    try:
        libro = conexion.execute(
            "SELECT path FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
    finally:
        conexion.close()

    if libro is None:
        return None

    carpeta = _resolver_ruta_segura(
        biblioteca / libro["path"],
        biblioteca,
    )

    if carpeta is None or not carpeta.is_dir():
        return None

    portada = _resolver_ruta_segura(
        carpeta / "cover.jpg",
        carpeta,
    )

    if portada is None or not portada.is_file():
        return None

    return portada
