import sqlite3
from config import CALIBRE_DB


def conexion_calibre():
    """Abre una conexión de solo lectura a la base de datos de Calibre"""

    base_datos = CALIBRE_DB.resolve()

    if not base_datos.is_file():
        raise FileNotFoundError(
            f"No se encontró la base de datos de Calibre: {base_datos}"
        )

    conexion = sqlite3.connect(
        base_datos.as_uri() + "?mode=ro",
        uri=True,
        timeout=10,
    )

    conexion.row_factory = sqlite3.Row

    return conexion
