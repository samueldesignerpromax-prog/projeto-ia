#!/bin/bash
echo "Instalando dependências..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
echo "Build concluído!"
