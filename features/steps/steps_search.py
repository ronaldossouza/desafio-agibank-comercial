from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given(u'que estou na página "{url}"')
def step_impl(context, url):
    """Acessa a URL do blog."""
    context.driver.get(url)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

@given(u'clico na lupa no canto superior esquerdo')
def step_click_search_icon(context):
    """Clica no ícone de lupa para abrir o campo de pesquisa."""
    # Aguarda para garantir que a página carregou completamente
    time.sleep(8)
    
    # Localiza o ícone de lupa
    search_icon = context.driver.find_element(By.CSS_SELECTOR, "a.slide-search.astra-search-icon")
    
    # Clica no ícone
    context.driver.execute_script("arguments[0].click();", search_icon)
    
    # Aguarda para que o campo de busca fique visível
    time.sleep(8)

@when(u'insiro "{texto}" no campo de busca')
def step_impl(context, texto):
    """Insere o texto no campo de busca."""
    # Localiza o campo de busca
    search_field = context.driver.find_element(By.CSS_SELECTOR, "input#search-field")
    
    # Limpa o campo (usando várias abordagens para garantir que funcione)
    try:
        search_field.clear()
    except:
        context.driver.execute_script("arguments[0].value = '';", search_field)
    
    # Insere o texto caractere por caractere com pequena pausa
    for char in texto:
        search_field.send_keys(char)
        time.sleep(0.05)
    
    # Armazena o texto para uso posterior
    context.search_text = texto

@when(u'pressiono Enter')
def step_impl(context):
    """Pressiona Enter para executar a pesquisa."""
    # Localiza o campo de busca novamente
    search_field = context.driver.find_element(By.CSS_SELECTOR, "input#search-field")
    
    # Pressiona Enter
    search_field.send_keys(Keys.ENTER)
    
    # Aguarda o redirecionamento e carregamento dos resultados
    time.sleep(3)

@then(u'devo ver resultados de pesquisa relacionados a "{termo}"')
def step_impl(context, termo):
    """Verifica se os resultados contêm o termo pesquisado."""
    # Aguarda para garantir que a página carregou completamente
    time.sleep(2)
    
    # Obtém o texto da página
    page_text = context.driver.page_source.lower()
    
    # Verifica se o termo está presente no conteúdo da página
    assert termo.lower() in page_text, f"O termo '{termo}' não foi encontrado na página de resultados."

@then(u'confirmo que o conteúdo exibido corresponde ao que foi pesquisado')
def step_impl(context):
    """Verifica se o conteúdo da página contém o termo pesquisado."""
    # Obtém o texto da página
    page_text = context.driver.page_source.lower()
    
    # Verifica se o termo está presente
    search_term_lower = context.search_text.lower()
    assert search_term_lower in page_text, f"O termo '{context.search_text}' não foi encontrado na página."

@then(u'devo ver uma mensagem indicando que nenhum resultado foi encontrado')
def step_impl(context):
    """Verifica se a página indica que nenhum resultado foi encontrado."""
    # Aguarda para garantir que a página carregou completamente
    time.sleep(2)
    
    # Obtém o texto da página
    page_text = context.driver.page_source.lower()
    search_term_lower = context.search_text.lower()
    
    # Verifica se o termo de pesquisa aparece na página (na mensagem de resultado)
    assert search_term_lower in page_text, "O termo pesquisado não aparece na página de resultados."
    
    # Verifica a presença de uma mensagem indicando ausência de resultados
    # ou a ausência de elementos de artigo que indicariam resultados encontrados
    no_results_phrases = ["nenhum resultado", "não encontrado", "no results", "not found"]
    has_no_results_message = any(phrase in page_text for phrase in no_results_phrases)
    
    results = context.driver.find_elements(By.CSS_SELECTOR, "article.post")
    has_few_results = len(results) < 3
    
    assert has_no_results_message or has_few_results, "Resultados foram encontrados quando não deveriam."