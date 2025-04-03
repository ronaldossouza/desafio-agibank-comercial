from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    service = Service(ChromeDriverManager().install())
    
    # Configura opções do Chrome
    options = Options()
    # Removido o argumento --user-data-dir para evitar conflitos
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Se desejar executar em modo headless (comum em CI), descomente a linha abaixo:
    # options.add_argument("--headless")
    
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    context.driver.quit()
