#!/bin/bash
# Script para executar o scraper com o ambiente virtual ativado

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instala/atualiza dependências
echo "Instalando dependências..."
pip install -r requirements.txt -q

# Executa o scraper
echo "Iniciando scraper..."
python3 app.py

# Desativa o ambiente virtual ao sair
deactivate
