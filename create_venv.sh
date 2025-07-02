#!/bin/bash
# Script para criar e ativar um ambiente virtual Python
#
# IMPORTANTE: Para ativar o ambiente virtual no shell atual, execute este script com:
#   source create_venv.sh
# ou
#   . create_venv.sh
#
# Se rodar com 'bash create_venv.sh', a ativação só vale para o subshell.

# Nome do ambiente virtual (padrão: venv)
VENV_DIR="venv"

# Cria o ambiente virtual se não existir
echo "Criando ambiente virtual em $VENV_DIR..."
python3 -m venv "$VENV_DIR"

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

echo "Ambiente virtual ativado. Para sair, use: deactivate"
