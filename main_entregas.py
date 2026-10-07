from core.login import iniciar_sesion
from navegacion.cursos import ir_a_curso
from navegacion.entregas import (
    abrir_entregas,
    listar_grupos,
    cambiar_grupo
)
from entregas.analizador import contar_entregas
from config import CURSO


def main():

    playwright, browser, context, page = iniciar_sesion()

    try:

        print("\n===================================")
        print(" ROBOT ENTREGAS UNAD ")
        print("===================================\n")

        page = ir_a_curso(page, CURSO)

        page = abrir_entregas(page, fase=2)

        grupos = listar_grupos(page)

        total_estudiantes = 0
        total_entregados = 0
        total_sin_entrega = 0

        for indice, grupo in enumerate(grupos, start=1):

            print(f"\n[{indice}/{len(grupos)}] {grupo['nombre']}")

            cambiar_grupo(page, grupo)

            resultado = contar_entregas(page)

            print(f"   Total       : {resultado['total']}")
            print(f"   Entregaron  : {resultado['entregados']}")
            print(f"   Sin entrega : {resultado['sin_entrega']}")
            print(f"   % Entrega   : {resultado['porcentaje']}%")

            total_estudiantes += resultado["total"]
            total_entregados += resultado["entregados"]
            total_sin_entrega += resultado["sin_entrega"]

        porcentaje = 0

        if total_estudiantes > 0:

            porcentaje = round(
                total_entregados * 100 / total_estudiantes,
                2
            )

        print("\n===================================")
        print("RESUMEN GENERAL")
        print("===================================")
        print(f"Grupos            : {len(grupos)}")
        print(f"Estudiantes       : {total_estudiantes}")
        print(f"Entregaron        : {total_entregados}")
        print(f"Sin entrega       : {total_sin_entrega}")
        print(f"% Global entrega  : {porcentaje}%")
        print("===================================")

        input("\nENTER para cerrar...")

    except Exception as e:

        print("\n❌ ERROR")
        print(e)
        input()

    finally:

        context.close()
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()