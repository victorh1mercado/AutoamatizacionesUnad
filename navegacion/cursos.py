from playwright.sync_api import Page


def ir_a_curso(page: Page, nombre_curso: str) -> Page:
    """
    Navega desde el Campus hasta el curso seleccionado.

    Args:
        page: Página del Campus (después del login)
        nombre_curso: Ejemplo "AulaA"

    Returns:
        Page: Página del curso.
    """

    print("📚 Abriendo Mis Cursos...")

    with page.expect_popup() as popup_cursos:
        page.get_by_role(
            "link",
            name="Abrir Mis cursos virtuales en"
        ).click()

    pagina_cursos = popup_cursos.value
    pagina_cursos.wait_for_load_state()

    print("✅ Página Mis Cursos abierta.")

    # Obtener todos los cursos disponibles

    cursos = pagina_cursos.locator("#div_f1708detalle a")

    total = cursos.count()

    print(f"📋 Cursos encontrados: {total}")

    for i in range(total):

        titulo = cursos.nth(i).get_attribute("title")

        print(f"   - {titulo}")

    print(f"\n📖 Abriendo curso: {nombre_curso}")

    with pagina_cursos.expect_popup() as popup_curso:

        pagina_cursos.locator(
            f'#div_f1708detalle a[title="{nombre_curso}"]'
        ).click()

    pagina_curso = popup_curso.value

    pagina_curso.wait_for_load_state()

    print("✅ Curso abierto correctamente.")

    return pagina_curso