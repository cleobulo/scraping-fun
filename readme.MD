# Scraping Fun 🕷️

Um web crawler/scraper em Python que respeita `robots.txt`, limita profundidade de navegação e persiste dados em SQLite.

## 📋 Características

- ✅ Respeita regras de `robots.txt` por domínio
- ✅ Controle de profundidade máxima de navegação
- ✅ Extrai títulos e conteúdo de páginas
- ✅ Salva dados em banco de dados SQLite
- ✅ Persistência de estado entre execuções (TODO e DONE lists)
- ✅ Tratamento robusto de erros e exceções
- ✅ User-Agent customizável

## 🔧 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Como Executar (Linux)

### 1. Criar e Ativar Ambiente Virtual

```bash
source create_venv.sh
```

### 2. Instalar Dependências

```bash
bash install_requirements.sh
```

### 3. Configurar URL Inicial

Crie um arquivo `config.py` na raiz do projeto:

```python
def load_config():
    return "https://example.com"
```

### 4. Executar o Scraper

```bash
python3 app.py
```

### 5. Parar a Aplicação

Pressione `Ctrl+C` para parar e salvar o estado atual.

## 📁 Estrutura do Projeto

```
scraping-fun/
├── app.py                 # Script principal
├── database.py            # Configuração do banco de dados
├── config.py              # Configuração da URL inicial
├── args.py                # Parser de argumentos
├── create_venv.sh         # Script para criar ambiente virtual
├── install_requirements.sh # Script para instalar dependências
├── requirements.txt       # Dependências Python
├── database.db            # Banco de dados SQLite
├── todo_list.json         # Estado das URLs a processar
├── done_list.json         # URLs já processadas
└── readme.MD              # Este arquivo
```

## ⚙️ Configuração

### Profundidade Máxima

Edite `MAX_DEPTH` em `app.py` para controlar quantos "saltos" de link o crawler pode fazer:

```python
MAX_DEPTH = 2  # Padrão: 2
```

### User-Agent

Customize o User-Agent em `app.py`:

```python
USER_AGENT = 'MyScraperBotFun'
```

## 📊 Visualizar Dados Capturados

### Via Python Script

Execute o script `db_data.py`:

```bash
python3 db_data.py
```

### Via DBeaver

1. Abra o DBeaver
2. Crie uma conexão SQLite
3. Selecione o arquivo `database.db`
4. Navegue até a tabela `page`

## 📝 Notas

- O scraper respeita o arquivo `robots.txt` de cada domínio visitado
- As listas de TODO e DONE são salvas automaticamente ao interromper (Ctrl+C)
- Ao reiniciar, o scraper continua de onde parou
