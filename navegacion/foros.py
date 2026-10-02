import re
from playwright.sync_api import Page

from foros.responder import (
    abrir_discusion,
    abrir_editor_respuesta,
    abrir_editor_avanzado,
    escribir_respuesta,
    volver_al_foro
)


def abrir_enlace_foro(page: Page, fase: int):

    print("🔎 Buscando el foro...")

    links = page.get_by_role("link")

    total = links.count()

    print(f"Links encontrados: {total}")

    for i in range(total):

        try:

            link = links.nth(i)

            texto = link.inner_text().strip()

            if (
                "Foro de discusión" in texto
                and f"Fase {fase}" in texto
            ):

                print(f"✅ Encontrado: {texto}")

                link.scroll_into_view_if_needed()

                page.wait_for_timeout(500)

                print("➡ Haciendo clic en el foro...")

                link.click(force=True)

                page.wait_for_load_state(
                    "domcontentloaded"
                )

                page.wait_for_timeout(2000)

                print("🔎 Esperando combo de grupos...")

                page.locator(
                    "select[name='group']"
                ).wait_for(
                    state="visible",
                    timeout=30000
                )

                print("✅ Foro abierto correctamente.")

                return

        except Exception:
            continue

    raise Exception(
        f"No se encontró el foro de la Fase {fase}"
    )


def abrir_foro(page: Page, fase: int) -> Page:

    print("\n📂 Abriendo Momento intermedio...")

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

        print(
            "ℹ Momento intermedio ya estaba expandido."
        )

    print(f"\n📂 Abriendo Fase {fase}...")

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

        print(
            f"ℹ Fase {fase} ya estaba expandida."
        )

    abrir_enlace_foro(
        page,
        fase
    )

    return page


def listar_grupos(page: Page):

    print("\n📋 Obteniendo grupos...")

    selector = page.locator(
        "select[name='group']"
    )

    selector.wait_for(
        state="visible",
        timeout=15000
    )

    opciones = selector.locator("option")

    grupos = []

    total = opciones.count()

    print(f"Total grupos: {total}")

    for i in range(total):

        opcion = opciones.nth(i)

        grupos.append({
            "id": opcion.get_attribute("value"),
            "nombre": opcion.inner_text().strip()
        })

    print(
        f"✅ {len(grupos)} grupos encontrados."
    )

    return grupos


def cambiar_grupo(page: Page, grupo):

    print(
        f"\n➡ Cambiando a {grupo['nombre']}"
    )

    selector = page.locator(
        "select[name='group']"
    )

    selector.wait_for(
        state="visible",
        timeout=30000
    )

    print("✅ Combo de grupos disponible.")

    selector.select_option(
        grupo["id"],
        timeout=15000
    )

    page.wait_for_load_state(
        "domcontentloaded"
    )

    page.wait_for_timeout(2000)

    selector = page.locator(
        "select[name='group']"
    )

    selector.wait_for(
        state="visible",
        timeout=15000
    )

    actual = selector.locator(
        "option:checked"
    ).inner_text().strip()

    print(
        f"Grupo actual: {actual}"
    )

    if actual != grupo["nombre"]:

        raise Exception(
            f"El grupo seleccionado no coincide. "
            f"Esperado: {grupo['nombre']} | "
            f"Actual: {actual}"
        )

    print(
        f"✅ Grupo cargado correctamente: {actual}"
    )


def recorrer_grupos_respondiendo(
    page: Page,
    nombre_discusion: str,
    nombre_usuario: str,
    mensaje: str
):

    grupos = listar_grupos(page)

    print("\n===================================")
    print("INICIANDO RECORRIDO DE GRUPOS")
    print("===================================")

    total_ok = 0
    total_error = 0

    for indice, grupo in enumerate(
        grupos,
        start=1
    ):

        print("\n-----------------------------------")
        print(
            f"Grupo {indice}/{len(grupos)}"
        )
        print("-----------------------------------")

        try:

            cambiar_grupo(
                page,
                grupo
            )

            abrir_discusion(
                page,
                nombre_discusion
            )

            abrir_editor_respuesta(
                page,
                nombre_usuario
            )

            abrir_editor_avanzado(
                page
            )

            escribir_respuesta(
                page,
                mensaje
            )

            print(
                "⚠ MODO SEGURO: "
                "no se publicará el mensaje."
            )

            input(
                "\nENTER para regresar al foro..."
            )

            volver_al_foro(
                page
            )

            abrir_enlace_foro(
                page,
                fase=2
            )

            print(
                "✅ Foro listo para el siguiente grupo."
            )

            total_ok += 1

        except Exception as e:

            print(
                f"❌ Error en {grupo['nombre']}"
            )

            print(e)

            total_error += 1

    print("\n===================================")
    print("RECORRIDO FINALIZADO")
    print("===================================")

    print(
        f"Grupos procesados : {len(grupos)}"
    )

    print(
        f"Correctos         : {total_ok}"
    )

    print(
        f"Con errores       : {total_error}"
    )

    print("===================================")