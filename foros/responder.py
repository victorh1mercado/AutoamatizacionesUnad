from playwright.sync_api import Page
from pathlib import Path
import re


# ----------------------------------------------------------
# Abrir la discusión
# ----------------------------------------------------------

def abrir_discusion(page: Page, nombre_discusion: str):

    print(f"\n📄 Buscando discusión: {nombre_discusion}")

    links = page.get_by_role("link")

    for i in range(links.count()):

        try:

            link = links.nth(i)

            texto = link.inner_text().strip()

            if nombre_discusion.lower() in texto.lower():

                print(f"✅ Discusión encontrada: {texto}")

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

    print("\n🔎 Buscando tu publicación...")

    menubars = page.get_by_role("menubar")

    total = menubars.count()

    print(f"Menubars encontrados: {total}")

    for i in range(total):

        menu = menubars.nth(i)

        try:

            aria = menu.get_attribute("aria-label") or ""

            print(f"   {i+1}. {aria}")

            # Ignorar respuestas
            if aria.startswith("Re:"):
                continue

            esperado = f"Miradas Sistémicas por {nombre_usuario}"

            if aria.strip() == esperado:

                print("✅ Publicación encontrada.")

                boton = menu.get_by_role(
                    "menuitem",
                    name="Responder"
                )

                boton.scroll_into_view_if_needed()

                boton.click(force=True)

                page.wait_for_load_state("domcontentloaded")

                page.wait_for_timeout(1500)

                print("✅ Editor abierto.")

                return

        except Exception:
            continue

    raise Exception("No se encontró la publicación inicial del usuario.")


# ----------------------------------------------------------
# Editor avanzado
# ----------------------------------------------------------

def abrir_editor_avanzado(page: Page):

    print("📝 Abriendo editor avanzado...")

    page.get_by_role(
        "button",
        name=re.compile("Avanzada", re.I)
    ).click(force=True)

    page.wait_for_timeout(2000)

    print("✅ Editor avanzado abierto.")


# ----------------------------------------------------------
# Cargar HTML desde archivo
# ----------------------------------------------------------

def escribir_respuesta(page: Page, ruta_html: str):

    print("📄 Leyendo plantilla HTML...")

    html = Path(ruta_html).read_text(
        encoding="utf-8"
    )

    print("📝 Abriendo editor HTML...")

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

    print("💾 Guardando HTML...")

    dialogo.get_by_role(
        "button",
        name="Guardar"
    ).click()

    page.wait_for_timeout(1500)

    print("✅ HTML cargado correctamente.")


# ----------------------------------------------------------
# Enviar publicación
# ----------------------------------------------------------

def enviar_respuesta(page: Page):

    print("📤 Enviando publicación...")

    page.get_by_role(
        "button",
        name="Enviar al foro"
    ).click(force=True)

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(3000)

    print("✅ Publicación enviada.")


# ----------------------------------------------------------
# Volver al foro
# ----------------------------------------------------------

def volver_al_foro(page: Page):

    print("↩ Regresando al foro...")

    page.go_back()

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(2000)

    print("✅ Regresó al foro.")