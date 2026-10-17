from flask import Flask, abort, render_template, request, send_file
from book_files import obtener_archivo_libro, obtener_portada_libro
from books import (
    obtener_detalle_libro,
    obtener_libros,
    obtener_opciones_filtros,
)


# Configuracion
app = Flask(__name__)

LIBROS_POR_PAGINA = 20

ORDENES_VALIDOS = {
    "titulo_asc",
    "titulo_desc",
    "autor",
    "recientes"
}

FORMATOS_PERMITIDOS = {
    "AZW3",
    "EPUB",
    "PDF",
    "MOBI",
    "KFX",
    "TXT",
    "RTF",
    "DOCX",
    "FB2"
}

# Funciones auxiliares
def validar_id_filtro(valor):
    """Valida un identificador de filtro opcional"""
    if not valor:
        return ""

    try:
        identificador = int(valor)
    except (TypeError, ValueError):
        abort(400, description="El identificador de un filtro no es válido")

    if identificador <= 0:
        abort(400, description="El identificador de un filtro no es válido")

    return str(identificador)


def obtener_url_retorno():
    """Acepta únicamente rutas locales como destino de retorno"""
    url = request.args.get("volver", "")

    if (
        not url.startswith("/")
        or url.startswith("//")
        or "\\" in url
    ):
        return ""

    return url


# Portadas
@app.route("/cover/<int:book_id>")
def portada(book_id):
    """Devuelve la portada de un libro o la imagen predeterminada"""
    archivo_portada = obtener_portada_libro(book_id)

    if archivo_portada is None:
        return send_file(
            app.static_folder + "/sin_portada.jpg",
            mimetype="image/jpeg",
        )

    return send_file(
        archivo_portada,
        mimetype="image/jpeg",
        conditional=True,
    )


# Detalle del libro
@app.route("/book/<int:book_id>")
def detalle_libro(book_id):
    """Muestra la información detallada de un libro"""
    libro = obtener_detalle_libro(book_id)

    if libro is None:
        abort(404)

    return render_template(
        "book.html",
        libro=libro,
        volver_url=obtener_url_retorno(),
    )


# Descarga de libros
@app.route("/download/<int:book_id>/<formato>")
def descargar_libro(book_id, formato):
    """Permite descargar un archivo de un formato admitido"""
    formato = formato.upper()

    if formato not in FORMATOS_PERMITIDOS:
        abort(404)

    archivo = obtener_archivo_libro(book_id, formato)

    if archivo is None:
        abort(404)

    return send_file(
        archivo,
        as_attachment=True,
        download_name=archivo.name,
        conditional=True,
    )


# Pagina principal, búsqueda y filtros
@app.route("/")
def inicio():
    """Muestra el catálogo con búsqueda, filtros y paginación"""
    busqueda = request.args.get("q", "").strip()

    autor_id = validar_id_filtro(request.args.get("autor", ""))
    serie_id = validar_id_filtro(request.args.get("serie", ""))
    etiqueta_id = validar_id_filtro(request.args.get("etiqueta", ""))

    orden = request.args.get("orden", "titulo_asc")

    if orden not in ORDENES_VALIDOS:
        orden = "titulo_asc"

    try:
        pagina = max(1, int(request.args.get("pagina", "1")))
    except (TypeError, ValueError):
        pagina = 1

    libros, total = obtener_libros(
        busqueda=busqueda,
        pagina=pagina,
        por_pagina=LIBROS_POR_PAGINA,
        autor_id=autor_id,
        serie_id=serie_id,
        etiqueta_id=etiqueta_id,
        orden=orden,
    )

    opciones = obtener_opciones_filtros()

    total_paginas = (
        total + LIBROS_POR_PAGINA - 1
    ) // LIBROS_POR_PAGINA

    return render_template(
        "index.html",
        libros=libros,
        busqueda=busqueda,
        pagina=pagina,
        total=total,
        total_paginas=total_paginas,
        autores=opciones["autores"],
        series=opciones["series"],
        etiquetas=opciones["etiquetas"],
        autor_seleccionado=autor_id,
        serie_seleccionada=serie_id,
        etiqueta_seleccionada=etiqueta_id,
        orden_seleccionado=orden,
    )


# Inicio de la app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
