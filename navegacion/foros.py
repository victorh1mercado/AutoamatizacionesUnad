import re
from playwright.sync_api import Page

from foros.responder import (
    abrir_discusion,
    abrir_editor_respuesta,
    abrir_editor_avanzado,
    escribir_respuesta,
    volver_al_foro,
    enviar_respuesta
)

from reportes.excelForos import (
    crear_reporte,
    registrar_grupo
)
from config import (
    MODO
)
from herramientas.logger import log



def abrir_enlace_foro(page: Page, fase: int):


    links = page.get_by_role("link")

    total = links.count()


    for i in range(total):

        try:

            link = links.nth(i)

            texto = link.inner_text().strip()

            if (
                "Foro de discusión" in texto
                and f"Fase {fase}" in texto
            ):


                link.scroll_into_view_if_needed()

                page.wait_for_timeout(500)


                link.click(force=True)

                page.wait_for_load_state(
                    "domcontentloaded"
                )

                page.wait_for_timeout(2000)


                page.locator(
                    "select[name='group']"
                ).wait_for(
                    state="visible",
                    timeout=30000
                )


                return

        except Exception:
            continue

    raise Exception(
        f"No se encontró el foro de la Fase {fase}"
    )


def abrir_foro(page: Page, fase: int) -> Page:

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

        log(
            "ℹ Momento intermedio ya estaba expandido."
        )

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

        log(
            f"ℹ Fase {fase} ya estaba expandida."
        )

    abrir_enlace_foro(
        page,
        fase
    )

    return page


def listar_grupos(page: Page):

    log("\n📋 Obteniendo grupos...")

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


    for i in range(total):

        opcion = opciones.nth(i)

        grupos.append({
            "id": opcion.get_attribute("value"),
            "nombre": opcion.inner_text().strip()
        })

    log(
        f"✅ {len(grupos)} grupos encontrados."
    )

    return grupos


def cambiar_grupo(page: Page, grupo):

    

    selector = page.locator(
        "select[name='group']"
    )

    selector.wait_for(
        state="visible",
        timeout=30000
    )


    selector.select_option(
        grupo["id"],
        timeout=15000
    )

    
    selector.dispatch_event("change")

    # Enviar únicamente el formulario del selector de grupos
    page.locator("#selectgroup").evaluate("f => f.submit()")

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)


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

   

    if actual != grupo["nombre"]:

        raise Exception(
            f"El grupo seleccionado no coincide. "
            f"Esperado: {grupo['nombre']} | "
            f"Actual: {actual}"
        )

    

    
def recorrer_grupos_respondiendo(
    page: Page,
    nombre_discusion: str,
    nombre_usuario: str,
    mensaje: str
):

    grupos = listar_grupos(page)

    crear_reporte()

    print("\n===================================")
    print("INICIANDO RECORRIDO DE GRUPOS")
    print("===================================")

    total_ok = 0
    total_error = 0
    if MODO == 0:
        log("📝 MODO: SIMULACIÓN (no se publicarán respuestas)")
    else:
        log("🚀 MODO: PRODUCCIÓN")

    for indice, grupo in enumerate(
        grupos,
        start=1
    ):

        log(f"\n[{indice}/{len(grupos)}] 📂 {grupo['nombre']}")

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

            url_publicacion = ""

            if MODO == 1:
               url_publicacion = enviar_respuesta(page)

            volver_al_foro(
                page
            )

            abrir_enlace_foro(
                page,
                fase=2
            )

            registrar_grupo(
                grupo=grupo["nombre"],
                discusion=nombre_discusion,
                estado="PUBLICADO" if MODO == 1 else "SIMULADO",
                observacion="Publicado correctamente" if MODO == 1 else "HTML cargado correctamente",
                url=url_publicacion if MODO == 1 else ""
            )

            print("✔ Grupo completado")

            total_ok += 1

        except Exception as e:

            print(f"❌ {grupo['nombre']}")
            print(f"   {e}")    

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
