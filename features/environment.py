# features/environment.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """Executa ANTES de cada cenário."""
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Executa DEPOIS de cada cenário."""
    #context.driver.quit()
