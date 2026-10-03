from playwright.sync_api import Page
print(">>> ANALIZADOR IMPORTADO <<<")

def analizar_grupo(page: Page):

    resultado = {
        "discusiones": 0,
        "interacciones": 0,
        "por_leer": 0,
        "requiere_revision": False,
        "detalle": []
    }

    print("   🔍 Analizando grupo...")

    # Buscar todas las filas de la tabla de discusiones
    print("URL:", page.url)
    print("Título:", page.locator("h1").inner_text())
    filas = page.locator("table tbody tr")

    total = filas.count()
    print(f"Filas encontradas: {total}")

    resultado["discusiones"] = total

    if total == 0:

        print("   📭 Sin discusiones.")

        return resultado

    print(f"   💬 {total} discusión(es) encontrada(s).")

    for i in range(total):

        fila = filas.nth(i)

        columnas = fila.locator("td")

        if columnas.count() < 5:
            continue

        try:

            titulo = columnas.nth(0).inner_text().strip()

        except:

            titulo = ""

        try:

            autor = columnas.nth(1).inner_text().strip()

        except:

            autor = ""

        try:

            respuestas = int(columnas.nth(3).inner_text().strip())

        except:

            respuestas = 0

        try:

            ultima = columnas.nth(4).inner_text().strip()

        except:

            ultima = ""

        # Buscar indicador "por leer"

        texto = fila.inner_text().lower()

        pendientes = 0

        if "por leer" in texto:

            import re

            m = re.search(r"(\d+)\s+por leer", texto)

            if m:

                pendientes = int(m.group(1))

        resultado["interacciones"] += respuestas

        resultado["por_leer"] += pendientes

        resultado["detalle"].append({

            "titulo": titulo,
            "autor": autor,
            "respuestas": respuestas,
            "por_leer": pendientes,
            "ultima_publicacion": ultima

        })

    resultado["requiere_revision"] = resultado["por_leer"] > 0

    return resultado