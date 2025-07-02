#!/bin/bash
# Script para instalar as dependências Python a partir do requirements.txt
#
# Execute este script com o ambiente virtual já ativado.

if [ ! -f "requirements.txt" ]; then
  echo "Arquivo requirements.txt não encontrado!"
  exit 1
fi

echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

echo "Dependências instaladas."
