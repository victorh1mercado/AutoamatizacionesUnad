from core.login import iniciar_sesion

from navegacion.cursos import ir_a_curso
from navegacion.foros import abrir_foro

from foros.seguimiento import recorrer_grupos_analizando

from config import CURSO


def main():

    playwright, browser, context, page = iniciar_sesion()

    try:

        print("\n===================================")
        print(" ROBOT ANALIZADOR DE FOROS UNAD ")
        print("===================================\n")

        # Abrir curso
        page = ir_a_curso(
            page,
            CURSO
        )

        # Abrir foro
        page = abrir_foro(
            page,
            fase=2
        )

        # Analizar todos los grupos
        recorrer_grupos_analizando(
            page=page,
            nombre_discusion="Miradas Sistémicas",
            nombre_usuario="VICTOR HUGO MERCADO RAMOS",
            fase=2
        )

        print("\n===================================")
        print("✅ Finalizó el análisis de todos los grupos.")
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