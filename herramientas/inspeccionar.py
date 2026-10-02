from core.login import iniciar_sesion
from navegacion.cursos import ir_a_curso
from config import CURSO


def inspeccionar():

    playwright, browser, context, page = iniciar_sesion()

    page = ir_a_curso(page, CURSO)

    print("\n🛠 Inspector de Playwright iniciado.")
    print("Puedes seleccionar elementos, generar selectores y probar código.")
    print("Cuando cierres el inspector, el programa finalizará.\n")

    page.pause()

    context.close()
    browser.close()
    playwright.stop()


if __name__ == "__main__":
    inspeccionar()