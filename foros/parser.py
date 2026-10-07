from datetime import datetime
from playwright.sync_api import Page
import unicodedata


def normalizar(texto):

    if texto is None:
        return ""

    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")

    return texto.upper().strip()


def obtener_publicaciones(page: Page):

    publicaciones = []

    posts = page.locator("div.forumpost")

    total = posts.count()

    for i in range(total):

        post = posts.nth(i)

        # -----------------------------
        # ID
        # -----------------------------
        try:
            post_id = post.get_attribute("data-post-id")
        except:
            post_id = ""

        # -----------------------------
        # Autor
        # -----------------------------
        try:
            autor = (
                post.locator("header a")
                .first
                .inner_text()
                .strip()
            )
        except:
            autor = ""

        # -----------------------------
        # Fecha
        # -----------------------------
        try:
            fecha = datetime.fromisoformat(
                post.locator("time").get_attribute("datetime")
            )
        except:
            fecha = None

        # -----------------------------
        # Asunto
        # -----------------------------
        try:
            asunto = (
                post.locator("h3")
                .inner_text()
                .strip()
            )
        except:
            asunto = ""

        # -----------------------------
        # En respuesta a
        # -----------------------------
        try:
            respuesta_a = (
                post.locator("span.sr-only")
                .inner_text()
                .replace("En respuesta a", "")
                .strip()
            )
        except:
            respuesta_a = ""

        # -----------------------------
        # Contenido
        # -----------------------------
        try:
            contenido = (
                post.locator(".post-content-container")
                .inner_text()
                .strip()
            )
        except:
            contenido = ""

        publicaciones.append({

            "id": post_id,

            "autor": autor,

            "fecha": fecha,

            "asunto": asunto,

            "respuesta_a": respuesta_a,

            "contenido": contenido,

            "es_mio": normalizar(autor) == normalizar("VICTOR HUGO MERCADO RAMOS"),

            "requiere_respuesta": False,
            "respondido": False,
            "respondido_por": "",
            "tiempo_respuesta_horas": None,
            "horas_sin_responder": None

        })

    # =====================================================
    # Analizar publicaciones
    # =====================================================

    ahora = datetime.now().astimezone()

    for publicacion in publicaciones:

        if publicacion["es_mio"]:
            continue

        respuestas = []

        for otra in publicaciones:

            if not otra["es_mio"]:
                continue

            if normalizar(publicacion["autor"]) == normalizar(otra["respuesta_a"]):
                respuestas.append(otra)

        if respuestas:

            primera = min(
                respuestas,
                key=lambda x: x["fecha"]
            )

            publicacion["respondido"] = True
            publicacion["respondido_por"] = primera["autor"]

            if (
                primera["fecha"] is not None
                and publicacion["fecha"] is not None
            ):

                horas = (
                    primera["fecha"] -
                    publicacion["fecha"]
                ).total_seconds() / 3600

                publicacion["tiempo_respuesta_horas"] = round(horas, 2)

        else:

            publicacion["requiere_respuesta"] = True

            if publicacion["fecha"] is not None:

                horas = (
                    ahora -
                    publicacion["fecha"]
                ).total_seconds() / 3600

                publicacion["horas_sin_responder"] = round(horas, 2)

    return publicaciones