from database import conexion_calibre


# Configuración
ORDENES_PERMITIDOS = {
    "titulo_asc": "books.title COLLATE NOCASE ASC",
    "titulo_desc": "books.title COLLATE NOCASE DESC",
    "autor": "MIN(authors.name) COLLATE NOCASE ASC",
    "recientes": "books.timestamp DESC",
}


# Catálogo, búsqueda, filtros y paginación
def obtener_libros(
    busqueda="",
    pagina=1,
    por_pagina=20,
    autor_id="",
    serie_id="",
    etiqueta_id="",
    orden="titulo_asc",
):
    """Obtiene una página del catálogo y el total de resultados"""
    # Validacion de los valores de paginacion
    try:
        pagina = max(1, int(pagina))
        por_pagina = max(1, int(por_pagina))
    except (TypeError, ValueError):
        pagina = 1
        por_pagina = 20

    # El ordenamiento solo puede usar criterios conocidos
    orden_sql = ORDENES_PERMITIDOS.get(
        orden,
        ORDENES_PERMITIDOS["titulo_asc"],
    )

    termino = f"%{busqueda}%"

    condiciones = [
        """
        (
            books.title LIKE ?
            OR EXISTS (
                SELECT 1
                FROM books_authors_link AS bal
                JOIN authors AS a
                    ON a.id = bal.author
                WHERE bal.book = books.id
                  AND a.name LIKE ?
            )
        )
        """
    ]

    parametros = [termino, termino]

    if autor_id:
        condiciones.append(
            """
            EXISTS (
                SELECT 1
                FROM books_authors_link AS bal
                WHERE bal.book = books.id
                  AND bal.author = ?
            )
            """
        )
        parametros.append(int(autor_id))

    if serie_id:
        condiciones.append(
            """
            EXISTS (
                SELECT 1
                FROM books_series_link AS bsl
                WHERE bsl.book = books.id
                  AND bsl.series = ?
            )
            """
        )
        parametros.append(int(serie_id))

    if etiqueta_id:
        condiciones.append(
            """
            EXISTS (
                SELECT 1
                FROM books_tags_link AS btl
                WHERE btl.book = books.id
                  AND btl.tag = ?
            )
            """
        )
        parametros.append(int(etiqueta_id))

    where_sql = " AND ".join(condiciones)
    desplazamiento = (pagina - 1) * por_pagina

    conexion = conexion_calibre()

    try:
        # Total de libros que cumplen los filtros
        consulta_conteo = f"""
            SELECT COUNT(*)
            FROM books
            WHERE {where_sql}
        """

        total = conexion.execute(
            consulta_conteo,
            parametros,
        ).fetchone()[0]

        # Libros correspondientes a la página solicitada
        consulta_libros = f"""
            SELECT
                books.id,
                books.title,
                books.path,
                COALESCE(
                    GROUP_CONCAT(authors.name, ', '),
                    'Autor desconocido'
                ) AS authors
            FROM books
            LEFT JOIN books_authors_link
                ON books.id = books_authors_link.book
            LEFT JOIN authors
                ON authors.id = books_authors_link.author
            WHERE {where_sql}
            GROUP BY books.id
            ORDER BY {orden_sql}, books.id
            LIMIT ? OFFSET ?
        """

        resultados = conexion.execute(
            consulta_libros,
            parametros + [por_pagina, desplazamiento],
        ).fetchall()

        libros = [dict(libro) for libro in resultados]

        return libros, total

    finally:
        conexion.close()


# Detalle de un libro
def obtener_detalle_libro(book_id):
    """Obtiene los datos principales, autores, series, etiquetas y formatos"""

    conexion = conexion_calibre()

    try:
        # Información principal
        registro = conexion.execute(
            """
            SELECT
                books.id,
                books.title,
                books.path,
                books.pubdate,
                comments.text AS comments
            FROM books
            LEFT JOIN comments
                ON comments.book = books.id
            WHERE books.id = ?
            """,
            (book_id,),
        ).fetchone()

        if registro is None:
            return None

        libro = dict(registro)

        # Autores
        autores = conexion.execute(
            """
            SELECT authors.name
            FROM authors
            JOIN books_authors_link
                ON authors.id = books_authors_link.author
            WHERE books_authors_link.book = ?
            ORDER BY authors.name COLLATE NOCASE
            """,
            (book_id,),
        ).fetchall()

        libro["authors"] = [
            autor["name"] for autor in autores
        ]

        # Series
        series = conexion.execute(
            """
            SELECT
                series.name,
                books.series_index
            FROM series
            JOIN books_series_link
                ON series.id = books_series_link.series
            JOIN books
                ON books.id = books_series_link.book
            WHERE books.id = ?
            ORDER BY series.name COLLATE NOCASE
            """,
            (book_id,),
        ).fetchall()

        libro["series"] = [
            {
                "name": item["name"],
                "index": item["series_index"],
            }
            for item in series
        ]

        # Etiquetas
        etiquetas = conexion.execute(
            """
            SELECT tags.name
            FROM tags
            JOIN books_tags_link
                ON tags.id = books_tags_link.tag
            WHERE books_tags_link.book = ?
            ORDER BY tags.name COLLATE NOCASE
            """,
            (book_id,),
        ).fetchall()

        libro["tags"] = [
            etiqueta["name"] for etiqueta in etiquetas
        ]

        # Formatos disponibles
        formatos = conexion.execute(
            """
            SELECT format, name, uncompressed_size
            FROM data
            WHERE book = ?
            ORDER BY format
            """,
            (book_id,),
        ).fetchall()

        libro["formats"] = [
            dict(formato) for formato in formatos
        ]

        return libro

    finally:
        conexion.close()


# Opciones para los filtros
def obtener_opciones_filtros():
    """Obtiene las opciones de autores, series y etiquetas del catálogo"""

    conexion = conexion_calibre()

    try:
        autores = conexion.execute(
            """
            SELECT authors.id, authors.name
            FROM authors
            WHERE EXISTS (
                SELECT 1
                FROM books_authors_link AS bal
                WHERE bal.author = authors.id
            )
            ORDER BY authors.name COLLATE NOCASE
            """
        ).fetchall()

        series = conexion.execute(
            """
            SELECT series.id, series.name
            FROM series
            WHERE EXISTS (
                SELECT 1
                FROM books_series_link AS bsl
                WHERE bsl.series = series.id
            )
            ORDER BY series.name COLLATE NOCASE
            """
        ).fetchall()

        etiquetas = conexion.execute(
            """
            SELECT tags.id, tags.name
            FROM tags
            WHERE EXISTS (
                SELECT 1
                FROM books_tags_link AS btl
                WHERE btl.tag = tags.id
            )
            ORDER BY tags.name COLLATE NOCASE
            """
        ).fetchall()

        return {
            "autores": [dict(item) for item in autores],
            "series": [dict(item) for item in series],
            "etiquetas": [dict(item) for item in etiquetas],
        }

    finally:
        conexion.close()
