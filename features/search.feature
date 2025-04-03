Feature: Busca de artigos no blog Agi
  Como usuário do blog
  Quero pesquisar por artigos
  Para encontrar conteúdos do meu interesse

  Scenario: Pesquisar artigo por texto exato e validar resultado
    Given que estou na página "https://blogdoagi.com.br/"
    And clico na lupa no canto superior esquerdo
    When insiro "Novas regras Pix: veja o que muda com as decisões do Banco Central" no campo de busca
    And pressiono Enter
    Then devo ver resultados de pesquisa relacionados a "Novas regras Pix"
    And confirmo que o conteúdo exibido corresponde ao que foi pesquisado

  Scenario: Pesquisar por termo inexistente e validar mensagem de aviso
    Given que estou na página "https://blogdoagi.com.br/"
    And clico na lupa no canto superior esquerdo
    When insiro "termoquenaodevevirnadanamaterial876543210" no campo de busca
    And pressiono Enter
    Then devo ver uma mensagem indicando que nenhum resultado foi encontrado