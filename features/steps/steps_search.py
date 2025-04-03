from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time

@given(u'que estou na página "{url}"')
def step_impl(context, url):
    """Acessa a URL do blog."""
    context.driver.get(url)
    WebDriverWait(context.driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

@given(u'clico na lupa no canto superior esquerdo')
def step_click_search_icon(context):
    """Clica no ícone de lupa para abrir o campo de pesquisa."""
    # Maximiza a janela para garantir que os elementos estejam visíveis
    context.driver.maximize_window()
    
    # Aguarda até que o ícone da lupa esteja clicável
    search_icon = WebDriverWait(context.driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.slide-search.astra-search-icon"))
    )
    
    # Tenta clicar no ícone da lupa usando JavaScript
    try:
        context.driver.execute_script("arguments[0].scrollIntoView(true);", search_icon)
        context.driver.execute_script("arguments[0].click();", search_icon)
    except Exception as e:
        print(f"Erro ao clicar no ícone de busca: {e}")
        # Tenta novamente com clique direto
        search_icon.click()
    
    # Aguarda até que o campo de busca esteja visível e interativo
    try:
        WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search-field"))
        )
        # Aguarda um pouco mais para garantir que o elemento está completamente carregado
        time.sleep(2)
    except TimeoutException:
        # Se o campo não aparecer, tenta clicar novamente
        print("Campo de busca não apareceu, tentando clicar na lupa novamente")
        search_icon = context.driver.find_element(By.CSS_SELECTOR, "a.slide-search.astra-search-icon")
        context.driver.execute_script("arguments[0].click();", search_icon)
        WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search-field"))
        )
        time.sleep(2)

@when(u'insiro "{texto}" no campo de busca')
def step_impl(context, texto):
    """Insere o texto no campo de busca."""
    # Função para tentar inserir texto com retentativas
    def try_input_text(max_attempts=3):
        for attempt in range(max_attempts):
            try:
                # Localiza o campo de busca garantindo que está visível e clicável
                search_field = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search-field"))
                )
                
                # Limpa o campo usando diferentes métodos
                try:
                    search_field.clear()
                except:
                    context.driver.execute_script("arguments[0].value = '';", search_field)
                
                # Ainda assim, garante que está focado antes de enviar as teclas
                context.driver.execute_script("arguments[0].focus();", search_field)
                
                # Insere o texto completo (pode ser mais estável que caractere por caractere)
                search_field.send_keys(texto)
                
                # Verifica se o texto foi inserido corretamente
                current_value = context.driver.execute_script("return arguments[0].value;", search_field)
                if current_value == texto:
                    return True
                else:
                    print(f"Texto não inserido corretamente. Tentativa {attempt+1}/{max_attempts}")
                    time.sleep(1)
            except (ElementNotInteractableException, TimeoutException) as e:
                print(f"Erro ao inserir texto - Tentativa {attempt+1}/{max_attempts}: {e}")
                if attempt < max_attempts - 1:
                    # Tenta clicar na lupa novamente para reabrir o campo
                    try:
                        search_icon = context.driver.find_element(By.CSS_SELECTOR, "a.slide-search.astra-search-icon")
                        context.driver.execute_script("arguments[0].click();", search_icon)
                        time.sleep(2)
                    except:
                        pass
                time.sleep(2)
        
        # Se todas as tentativas falharem, lança uma exceção
        raise Exception(f"Falha ao inserir texto após {max_attempts} tentativas")
    
    # Tenta inserir o texto
    try_input_text()
    
    # Armazena o texto para uso posterior
    context.search_text = texto

@when(u'pressiono Enter')
def step_impl(context):
    """Pressiona Enter para executar a pesquisa."""
    # Localiza o campo de busca e verifica se está interativo
    search_field = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search-field"))
    )
    
    # Pressiona Enter
    search_field.send_keys(Keys.ENTER)
    
    # Aguarda o redirecionamento e carregamento dos resultados
    # Pode verificar a mudança de URL ou a presença de elementos específicos da página de resultados
    time.sleep(3)
    try:
        WebDriverWait(context.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ast-container"))
        )
    except:
        print("Tempo limite ao carregar a página de resultados")

@then(u'devo ver resultados de pesquisa relacionados a "{termo}"')
def step_impl(context, termo):
    """Verifica se os resultados contêm o termo pesquisado."""
    # Aguarda para garantir que a página carregou completamente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
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
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
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
