from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    service = Service(ChromeDriverManager().install())
    
    # Configura opções do Chrome
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Ativar modo headless em ambientes de CI pode evitar problemas gráficos
    options.add_argument("--headless")
    
    # Não especificamos o argumento --user-data-dir para evitar conflitos
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    if hasattr(context, 'driver'):
        context.driver.quit()
