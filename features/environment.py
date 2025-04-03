from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def before_all(context):
    """Executa ANTES de todos os testes."""
    # Configure timeouts gerais para HTTP
    import http.client
    http.client.HTTPConnection._http_vsn = 11
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.1'
    http.client._GLOBAL_DEFAULT_TIMEOUT = 300  # 5 minutos

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    # Configurações específicas para ambientes CI (GitHub Actions)
    print(f"Iniciando cenário: {scenario.name}")
    
    # Configura opções do Chrome
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    
    # Aumentar os timeouts do navegador
    options.add_argument("--browser-process-hint-timeout=600")
    
    try:
        # Usando try/except para tornar a instalação do driver mais robusta
        service = Service(ChromeDriverManager().install())
        print("ChromeDriver instalado com sucesso")
    except Exception as e:
        print(f"Erro ao instalar ChromeDriver via manager: {e}")
        # Fallback para Chrome padrão no sistema
        service = Service()
        print("Usando ChromeDriver do sistema")
    
    # Criar o driver com timeouts aumentados
    try:
        context.driver = webdriver.Chrome(service=service, options=options)
        print("Driver Chrome criado com sucesso")
        context.driver.set_page_load_timeout(180)  # 3 minutos
        context.driver.set_script_timeout(180)  # 3 minutos
        context.driver.implicitly_wait(20)  # 20 segundos
        context.driver.maximize_window()
        print("Driver Chrome configurado com timeouts aumentados")
    except Exception as e:
        print(f"Erro ao criar o driver Chrome: {e}")
        raise

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    # Se o cenário falhar, salvar um screenshot e o HTML da página
    if scenario.status == "failed":
        print(f"Cenário falhou: {scenario.name}")
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"failed_{timestamp}_{scenario.name.replace(' ', '_')}"
            
            # Criar diretório para screenshots se não existir
            os.makedirs("screenshots", exist_ok=True)
            
            # Salvar screenshot
            screenshot_path = f"screenshots/{filename}.png"
            context.driver.save_screenshot(screenshot_path)
            print(f"Screenshot salvo em: {screenshot_path}")
            
            # Salvar fonte HTML
            html_path = f"screenshots/{filename}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(context.driver.page_source)
            print(f"HTML da página salvo em: {html_path}")
        except Exception as e:
            print(f"Erro ao salvar diagnósticos de falha: {e}")
    
    # Fechar o driver com segurança
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            print("Driver Chrome fechado com sucesso")
        except Exception as e:
            print(f"Erro ao fechar o driver Chrome: {e}")
