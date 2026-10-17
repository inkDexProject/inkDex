import os
from pathlib import Path

# Ruta de la biblioteca de Calibre
RUTA_CALIBRE_POR_DEFECTO = r"/ruta/a/tu/biblioteca/Calibre"

CALIBRE_LIBRARY = Path(
    os.environ.get(
        "INKDEX_CALIBRE_LIBRARY",
        RUTA_CALIBRE_POR_DEFECTO
    )
).expanduser().resolve()

CALIBRE_DB = CALIBRE_LIBRARY / "metadata.db"
