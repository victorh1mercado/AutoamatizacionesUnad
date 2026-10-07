from playwright.sync_api import Page


def contar_entregas(page: Page):

    # Buscar únicamente las filas de estudiantes
    filas = page.locator("tr[id*='_r']")

    entregados = 0
    sin_entrega = 0

    for i in range(filas.count()):

        fila = filas.nth(i)

        columnas = fila.locator("td")

        # Solo analizar filas con suficientes columnas
        if columnas.count() < 4:
            continue

        try:
            estado = columnas.nth(3).inner_text().strip()
        except Exception:
            continue

        if "Enviado para calificar" in estado:

            entregados += 1

        elif "Sin entrega" in estado:

            sin_entrega += 1

    # El total real son únicamente los estudiantes con estado de entrega
    total = entregados + sin_entrega

    porcentaje = 0

    if total > 0:

        porcentaje = round(
            (entregados / total) * 100,
            2
        )

    return {

        "total": total,

        "entregados": entregados,

        "sin_entrega": sin_entrega,

        "porcentaje": porcentaje

    }