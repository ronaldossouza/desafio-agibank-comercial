from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Adicionado
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile  # Adicionado

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    service = Service(ChromeDriverManager().install())
    
    # Configura opções do Chrome
    options = Options()
    # Cria um diretório temporário único para user-data-dir
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    # Opções adicionais para ambientes de CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Se desejar executar em modo headless, descomente a linha abaixo:
    # options.add_argument("--headless")
    
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    #context.driver.quit()
