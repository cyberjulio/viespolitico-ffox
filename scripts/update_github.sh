#!/bin/bash

# Script para atualizar GitHub usando token do arquivo de credenciais

echo "🔄 Atualizando repositório GitHub..."

cd "$(dirname "$0")/.."

# Ler token do arquivo de credenciais
if [ ! -f ".github_token" ]; then
    echo "❌ Arquivo .github_token não encontrado!"
    echo "Crie o arquivo e adicione o token GitHub 'qcli'"
    exit 1
fi

TOKEN=$(grep -v '^#' .github_token | head -n1 | tr -d ' \n')

if [ -z "$TOKEN" ]; then
    echo "❌ Token não encontrado no arquivo .github_token"
    echo "Adicione o token GitHub 'qcli' no arquivo"
    exit 1
fi

# Configurar URL com token
git remote set-url origin https://${TOKEN}@github.com/cyberjulio/viespolitico-ffox.git

# Adicionar arquivos principais
git add extension/manifest.json
git add extension/content.js  
git add extension/popup.html
git add extension/popup.js
git add extension/background.js
git add extension/options.html
git add extension/options.js
git add extension/seed_profiles.json

# Adicionar XPI
git add viespolitico-firefox-v1.3.1.xpi

# Adicionar documentação
git add README_GITHUB.md
git add PROJECT_CONTEXT.md

# Commit
git commit -m "feat: v1.3.1 - Correção de timing e algoritmo de distribuição

- Algoritmo baseado em distribuição vs média simples
- Correção de timing para conexões lentas  
- Detecção de 'No results found'
- XPI funcional completo
- Documentação atualizada"

# Push
git push origin main

echo "✅ GitHub atualizado com v1.3.1!"
