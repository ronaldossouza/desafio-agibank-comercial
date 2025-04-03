from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Acrescentado
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile  # Acrescentado
import shutil     # Acrescentado

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    service = Service(ChromeDriverManager().install())
    
    # Acrescentando opções do Chrome para evitar conflito no user-data-dir
    options = Options()
    # Cria um diretório temporário único e armazena no contexto para posterior limpeza
    user_data_dir = tempfile.mkdtemp()
    context.user_data_dir = user_data_dir  # Armazena para usar no after_scenario
    options.add_argument(f"--user-data-dir={user_data_dir}")
    # Opções adicionais úteis para ambientes de CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Se desejar executar em modo headless, descomente a linha abaixo:
    # options.add_argument("--headless")
    
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    # Acrescentado: finaliza o driver e remove o diretório temporário criado
    if hasattr(context, 'driver'):
        context.driver.quit()
    if hasattr(context, 'user_data_dir'):
        shutil.rmtree(context.user_data_dir, ignore_errors=True)
    #context.driver.quit()
