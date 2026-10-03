from playwright.sync_api import Page
from pathlib import Path
import re


# ----------------------------------------------------------
# Abrir la discusión
# ----------------------------------------------------------

def abrir_discusion(page: Page, nombre_discusion: str):


    links = page.get_by_role("link")

    for i in range(links.count()):

        try:

            link = links.nth(i)

            texto = link.inner_text().strip()

            if nombre_discusion.lower() in texto.lower():


                link.scroll_into_view_if_needed()

                page.wait_for_timeout(500)


                link.click(force=True)
                

                page.wait_for_load_state("domcontentloaded")

                page.wait_for_timeout(1500)
               

                return

        except Exception:
            continue

    raise Exception("No se encontró la discusión.")


# ----------------------------------------------------------
# Abrir responder sobre MI publicación
# ----------------------------------------------------------

def abrir_editor_respuesta(page: Page, nombre_usuario: str):


    menubars = page.get_by_role("menubar")

    total = menubars.count()

    for i in range(total):

        menu = menubars.nth(i)

        try:

            aria = menu.get_attribute("aria-label") or ""


            # Ignorar respuestas
            if aria.startswith("Re:"):
                continue

            esperado = f"Miradas Sistémicas por {nombre_usuario}"

            if aria.strip() == esperado:


                boton = menu.get_by_role(
                    "menuitem",
                    name="Responder"
                )

                boton.scroll_into_view_if_needed()

                boton.click(force=True)

                page.wait_for_load_state("domcontentloaded")

                page.wait_for_timeout(1500)


                return

        except Exception:
            continue

    raise Exception("No se encontró la publicación inicial del usuario.")


# ----------------------------------------------------------
# Editor avanzado
# ----------------------------------------------------------

def abrir_editor_avanzado(page: Page):


    page.get_by_role(
        "button",
        name=re.compile("Avanzada", re.I)
    ).click(force=True)

    page.wait_for_timeout(2000)



# ----------------------------------------------------------
# Cargar HTML desde archivo
# ----------------------------------------------------------

def escribir_respuesta(page: Page, ruta_html: str):


    html = Path(ruta_html).read_text(
        encoding="utf-8"
    )


    page.locator(".tox-tbtn").first.click()

    page.wait_for_timeout(1000)

    dialogo = page.get_by_role(
        "dialog",
        name=re.compile("Source code", re.I)
    )

    cuadro = dialogo.get_by_role("textbox")

    cuadro.click()

    cuadro.press("Control+A")

    cuadro.fill(html)

    dialogo.get_by_role(
        "button",
        name="Guardar"
    ).click()

    page.wait_for_timeout(1500)



# ----------------------------------------------------------
# Enviar publicación
# ----------------------------------------------------------

def enviar_respuesta(page: Page):

    print("📤 Publicando respuesta...")

    boton = page.get_by_role(
        "button",
        name="Enviar al foro"
    )

    boton.click(force=True)

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(4000)

    # Esperar a que desaparezca el botón de envío
    try:

        boton.wait_for(
            state="detached",
            timeout=10000
        )

    except Exception:
        pass

    url_publicacion = page.url


    return url_publicacion


# ----------------------------------------------------------
# Volver al foro
# ----------------------------------------------------------

def volver_al_foro(page: Page):

    page.go_back(wait_until="domcontentloaded")

    page.wait_for_timeout(2000)
