from playwright.sync_api import sync_playwright

def abrir_navegador(headless=False):
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless,
        slow_mo=300
    )

    page = browser.new_page()

    return playwright, browser, page