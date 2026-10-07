from playwright.sync_api import Page


def obtener_entregas(page: Page):

    """
    Lee la tabla de entregas del grupo seleccionado.

    Retorna una lista así:

    [
        {
            "estudiante": "...",
            "correo": "...",
            "estado": "...",
            "entrego": True
        }
    ]
    """

    filas = page.locator("table tbody tr")

    total = filas.count()

    entregas = []

    for i in range(total):

        fila = filas.nth(i)

        columnas = fila.locator("td")

        if columnas.count() < 4:
            continue

        # -----------------------------------
        # Nombre estudiante
        # -----------------------------------

        try:
            estudiante = (
                columnas
                .nth(0)
                .inner_text()
                .strip()
            )
        except Exception:
            estudiante = ""

        # -----------------------------------
        # Correo
        # -----------------------------------

        try:
            correo = (
                columnas
                .nth(1)
                .inner_text()
                .strip()
            )
        except Exception:
            correo = ""

        # -----------------------------------
        # Estado entrega
        # -----------------------------------

        try:
            estado = (
                columnas
                .nth(3)
                .inner_text()
                .strip()
            )
        except Exception:
            estado = ""

        # -----------------------------------
        # ¿Entregó?
        # -----------------------------------

        entrego = "Enviado para calificar" in estado

        entregas.append({

            "estudiante": estudiante,

            "correo": correo,

            "estado": estado,

            "entrego": entrego

        })

    return entregas