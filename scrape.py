from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup as bs

def scrape(website):
    print("Ejecutando Chrome...")

    chrome_driver_path = "/usr/local/bin/chromedriver"
    browser_path = "/usr/bin/google-chrome"

    options = uc.ChromeOptions()
    options.binary_location = browser_path
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = uc.Chrome(
        service=Service(chrome_driver_path),
        options=options,
        browser_executable_path=browser_path  # <--- este parámetro es CLAVE
    )

    try:
        driver.get(website)
        print("Página cargada...")
        time.sleep(3)
        html = driver.page_source
        return html
    finally:
        driver.quit()



def extraer_body(contenido_html):
    soup = bs(contenido_html, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return ""


def limpiar_body(body_content):
    soup = bs(body_content, "html.parser")

    # Eliminar etiquetas irrelevantes
    for tag in soup(['script', 'style', 'meta', 'link', 'noscript']):
        tag.decompose()

    # Eliminar nodos con clases o ids relacionadas a cookies o tracking
    for tag in soup.find_all(True):
        try:
            tag_id = tag.get("id", "")
            tag_class = " ".join(tag.get("class", [])) if tag.has_attr("class") else ""
            tag_id = tag_id.lower() if isinstance(tag_id, str) else ""
            tag_class = tag_class.lower()

            if any(x in tag_id for x in ["cookie", "consent", "tracking", "banner", "analytics"]) or \
               any(x in tag_class for x in ["cookie", "consent", "tracking", "banner", "analytics"]):
                tag.decompose()

        except Exception as e:
            print(f"Error procesando etiqueta: {e}")
            continue

    clean_content = soup.get_text(separator="\n")
    clean_content = "\n".join(
        line.strip() for line in clean_content.splitlines() if len(line.strip()) > 5
    )

    return clean_content



def porcionador(dom_content, max_lenght=6000):
    return [
        dom_content[i: i + max_lenght] for i in range(0, len(dom_content), max_lenght)
    ]
