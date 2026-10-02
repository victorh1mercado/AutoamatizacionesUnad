from playwright.sync_api import sync_playwright, TimeoutError
from config import URL_CAMPUS, USUARIO_UNAD, CLAVE_UNAD


def pasar_bienvenida(page):
    """
    Presiona todas las pantallas de 'Continuar'
    que aparezcan antes del login.
    """

    print("🔎 Verificando pantallas de bienvenida...")

    while True:

        try:

            boton = page.get_by_role(
                "button",
                name="Continuar"
            )

            boton.wait_for(timeout=2500)

            print("➡ Pulsando Continuar...")

            boton.click()

            page.wait_for_timeout(1500)

        except TimeoutError:

            print("✅ No hay más pantallas de bienvenida.")

            break


def iniciar_sesion(headless=False):
    """
    Inicia sesión en Campus Virtual.

    Retorna:
        playwright, browser, context, page
    """

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless,
        slow_mo=300
    )

    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={
            "latitude": 4.570868,
            "longitude": -74.297333
        }
    )

    page = context.new_page()

    print("🌐 Abriendo Campus Virtual...")

    page.goto(
        URL_CAMPUS,
        wait_until="domcontentloaded"
    )

    # Esperar que cargue un poco
    page.wait_for_timeout(2000)

    # Pasar todas las pantallas de bienvenida
    pasar_bienvenida(page)

    print("🔎 Buscando formulario de login...")

    usuario = page.get_by_role(
        "textbox",
        name="Digite su número de documento"
    )

    usuario.wait_for(timeout=20000)

    print("👤 Ingresando usuario...")

    usuario.fill(USUARIO_UNAD)

    print("🔑 Ingresando contraseña...")

    password = page.get_by_role(
        "textbox",
        name="Digite su contraseña"
    )

    password.wait_for(timeout=10000)

    password.fill(CLAVE_UNAD)

    print("🚀 Iniciando sesión...")

    page.get_by_role(
        "button",
        name="Ingresar a Campus Virtual"
    ).click()

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(3000)

    print("✅ Login realizado correctamente.")

    return playwright, browser, context, page