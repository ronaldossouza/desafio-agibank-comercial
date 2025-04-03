# Desafio Agibank - Automação de Testes

[![Testes Automatizados](https://github.com/SEU-USUARIO/desafio-agibank-comercial/actions/workflows/test.yml/badge.svg)](https://github.com/SEU-USUARIO/desafio-agibank-comercial/actions/workflows/test.yml)

Este projeto contém testes automatizados para o Blog do Agi, utilizando Python, Behave e Selenium.

## 🧪 Cenários de Teste

O projeto implementa dois cenários de teste:

1. **Pesquisar artigo por texto exato e validar resultado** - Verifica se ao pesquisar por um texto específico são exibidos resultados relacionados.
2. **Pesquisar por termo inexistente e validar mensagem de aviso** - Verifica se ao pesquisar por um termo improvável é exibida uma mensagem de ausência de resultados.

## 🛠️ Tecnologias

- Python 3.x
- Behave (BDD - Behavior Driven Development)
- Selenium WebDriver
- GitHub Actions (CI/CD)

## 📋 Pré-requisitos

- Python 3.x
- Google Chrome
- ChromeDriver compatível com a versão do Chrome

## 🚀 Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com/SEU-USUARIO/desafio-agibank-comercial.git
   cd desafio-agibank-comercial
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Executando os Testes

Para executar todos os testes:
```bash
behave
```

Para executar um cenário específico:
```bash
behave -n "Pesquisar artigo por texto exato e validar resultado"
```

## 🔄 CI/CD

Este projeto utiliza GitHub Actions para execução automatizada dos testes em ambiente Linux. A cada push ou pull request para a branch main, os testes são executados automaticamente.

Você também pode executar os testes manualmente pela interface do GitHub na aba "Actions".

## 📂 Estrutura do Projeto

```
project/
├── .github/
│   └── workflows/
│       └── test.yml         # Configuração do GitHub Actions
├── features/
│   ├── environment.py       # Configuração do ambiente de teste
│   ├── search.feature       # Definição dos cenários em Gherkin
│   └── steps/
│       └── steps_search.py  # Implementação dos passos de teste
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação do projeto
```

## 📝 Notas

- Os testes foram desenvolvidos para o site https://blogdoagi.com.br/
- A automação utiliza seletores específicos para localizar elementos na página
- A execução é compatível com diferentes sistemas operacionais (Windows, macOS, Linux)