from playwright.sync_api import Page

from herramientas.logger import log

from navegacion.foros import (
    listar_grupos,
    cambiar_grupo,
    abrir_enlace_foro
)

from foros.responder import (
    abrir_discusion,
    volver_al_foro
)

from foros.parser import obtener_publicaciones

# IMPORTANTE:
from foros.analizador import analizar_publicaciones

from reportes.excelSeguimiento import (
    crear_reporte_seguimiento,
    registrar_publicaciones
)


def recorrer_grupos_analizando(
    page: Page,
    nombre_discusion: str,
    nombre_usuario: str,
    fase: int = 2
):

    grupos = listar_grupos(page)

    crear_reporte_seguimiento()

    print("\n===================================")
    print(" INICIANDO ANÁLISIS DE FOROS ")
    print("===================================")

    total_ok = 0
    total_error = 0

    for indice, grupo in enumerate(grupos, start=1):

        log(f"\n[{indice}/{len(grupos)}] 📂 {grupo['nombre']}")

        try:

            # Cambiar grupo
            cambiar_grupo(page, grupo)

            # Abrir discusión
            abrir_discusion(page, nombre_discusion)

            # Leer publicaciones
            publicaciones = obtener_publicaciones(page)

            # Analizar publicaciones
            resultado = analizar_publicaciones(
                publicaciones,
                nombre_usuario
            )

            # Guardar Excel
            registrar_publicaciones(
                grupo=grupo["nombre"],
                publicaciones=resultado
            )

            # Regresar
            volver_al_foro(page)

            abrir_enlace_foro(
                page,
                fase
            )

            log("✔ Grupo analizado")

            total_ok += 1

        except Exception as e:

            log(f"❌ {grupo['nombre']}")
            log(str(e))

            total_error += 1

            try:

                while "discuss.php" in page.url:

                    page.go_back()

                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(1500)

                abrir_enlace_foro(
                    page,
                    fase
                )

            except Exception:
                pass

    print("\n===================================")
    print(" ANÁLISIS FINALIZADO ")
    print("===================================")

    print(f"Grupos analizados : {len(grupos)}")
    print(f"Correctos         : {total_ok}")
    print(f"Con errores       : {total_error}")
    print("===================================")