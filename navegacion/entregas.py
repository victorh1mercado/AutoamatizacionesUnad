import re
from playwright.sync_api import Page

from herramientas.logger import log


# ============================================================
# ABRIR ENTREGAS
# ============================================================

def abrir_enlace_entregas(page: Page, fase: int):

    links = page.get_by_role("link")

    total = links.count()

    for i in range(total):

        try:

            link = links.nth(i)

            texto = link.inner_text().strip()

            if (
                "Rúbrica de evaluación" in texto
                and f"Fase {fase}" in texto
            ):

                link.scroll_into_view_if_needed()

                page.wait_for_timeout(500)

                link.click(force=True)

                page.wait_for_load_state("domcontentloaded")

                page.wait_for_timeout(2000)

                break

        except Exception:
            continue

    page.get_by_role(
        "link",
        name="Entregas"
    ).click()

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(2500)

    return page


# ============================================================
# ABRIR FASE
# ============================================================

def abrir_entregas(page: Page, fase: int = 2):

    log("\n📂 Abriendo Momento intermedio...")

    try:

        page.get_by_role(
            "button",
            name=re.compile(
                "Momento intermedio",
                re.I
            )
        ).click()

        page.wait_for_timeout(1000)

    except Exception:

        log("ℹ Momento intermedio ya estaba expandido.")

    log(f"\n📂 Abriendo Fase {fase}...")

    try:

        boton = page.get_by_role(
            "button",
            name=re.compile(
                fr"Fase {fase}",
                re.I
            )
        )

        boton.scroll_into_view_if_needed()

        page.wait_for_timeout(500)

        boton.click(force=True)

        page.wait_for_timeout(1500)

    except Exception:

        log(f"ℹ Fase {fase} ya estaba expandida.")

    abrir_enlace_entregas(page, fase)

    return page


# ============================================================
# LISTAR GRUPOS
# ============================================================

def listar_grupos(page: Page):

    log("\n📋 Obteniendo grupos...")

    combo = page.get_by_role(
        "combobox",
        name=re.compile(
            "Seleccionar grupos",
            re.I
        )
    )

    combo.click()

    page.wait_for_timeout(1500)

    opciones = page.locator(
        "li[role='option'][data-value]"
    )

    grupos = []

    total = opciones.count()

    for i in range(total):

        try:

            opcion = opciones.nth(i)

            nombre = opcion.inner_text().strip()

            valor = opcion.get_attribute("data-value")

            if nombre.startswith("204016_"):

                grupos.append({

                    "id": valor,

                    "nombre": nombre

                })

        except Exception:
            continue

    combo.press("Escape")

    log(f"✅ {len(grupos)} grupos encontrados.")

    return grupos


# ============================================================
# CAMBIAR GRUPO
# ============================================================

def cambiar_grupo(page: Page, grupo):

    combo = page.get_by_role(
        "combobox",
        name=re.compile(
            "Seleccionar grupos",
            re.I
        )
    )

    combo.click()

    page.wait_for_timeout(800)

    opcion = page.locator(
        f"li[data-value='{grupo['id']}']"
    )

    opcion.click()

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(2500)

    actual = (
        combo
        .locator("[data-selected-option]")
        .first
        .inner_text()
        .strip()
    )

    if actual != grupo["nombre"]:

        raise Exception(

            f"Grupo incorrecto.\n"
            f"Esperado: {grupo['nombre']}\n"
            f"Actual: {actual}"

        )

    log(f"   ✔ {actual}")