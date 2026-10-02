from core.login import iniciar_sesion
from navegacion.cursos import ir_a_curso
from navegacion.foros import (
    abrir_foro,
    recorrer_grupos_respondiendo
)
from config import CURSO


# Ruta de la plantilla HTML
PLANTILLA_HTML = "PlantillasMensajeForos/PublicacionOvaFase2.html"
# Si tu archivo realmente se llama diferente, coloca aquí el nombre exacto.


def main():

    playwright, browser, context, page = iniciar_sesion()

    try:

        print("\n===================================")
        print(" ROBOT RESPONDEDOR DE FOROS UNAD ")
        print("===================================\n")

        # 1. Abrir el curso
        page = ir_a_curso(
            page,
            CURSO
        )

        # 2. Abrir el foro de la Fase 2
        page = abrir_foro(
            page,
            fase=2
        )

        # 3. Recorrer TODOS los grupos
        recorrer_grupos_respondiendo(
            page=page,
            nombre_discusion="Miradas Sistémicas",
            nombre_usuario="VICTOR HUGO MERCADO RAMOS",
            mensaje=PLANTILLA_HTML
        )

        print("\n===================================")
        print("✅ Finalizó el recorrido de todos los grupos.")
        print("⚠ No se publicó ningún mensaje.")
        print("===================================")

        input("\nPresione ENTER para cerrar...")

    except Exception as e:

        print("\n❌ ERROR:")
        print(e)

        input("\nPresione ENTER para cerrar...")

    finally:

        context.close()
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()