#!/bin/bash

# Script para criar XPI funcional do ViésPolítico
# Uso: ./build_xpi.sh [versao]

VERSION=${1:-"1.2.1"}
BUILD_DIR="firefox_build_${VERSION}"
XPI_NAME="viespolitico-firefox-v${VERSION}.xpi"

echo "🔧 Construindo XPI v${VERSION}..."

# Limpar build anterior
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📁 Copiando arquivos..."

# Copiar arquivos da extensão
cp extension/content.js "$BUILD_DIR/"
cp extension/background.js "$BUILD_DIR/"
cp extension/popup.html "$BUILD_DIR/"
cp extension/popup.js "$BUILD_DIR/"
cp extension/options.html "$BUILD_DIR/"
cp extension/options.js "$BUILD_DIR/"
cp extension/seed_profiles.json "$BUILD_DIR/"

echo "📝 Criando manifest.json v${VERSION}..."

# Criar manifest.json atualizado
cat > "$BUILD_DIR/manifest.json" << EOF
{
  "manifest_version": 2,
  "name": "ViésPolítico",
  "version": "${VERSION}",
  "description": "Análise política automática do Instagram - Desenvolvido por @cyberjulio",
  
  "background": {
    "scripts": ["background.js"],
    "persistent": false
  },
  
  "browser_action": {
    "default_popup": "popup.html",
    "default_title": "ViésPolítico"
  },
  
  "options_ui": {
    "page": "options.html",
    "open_in_tab": true
  },
  
  "permissions": [
    "activeTab",
    "storage",
    "tabs",
    "https://www.instagram.com/*"
  ],
  
  "content_scripts": [
    {
      "matches": ["https://www.instagram.com/*"],
      "js": ["content.js"]
    }
  ],
  
  "web_accessible_resources": [
    "seed_profiles.json"
  ]
}
EOF

echo "📦 Criando XPI com web-ext..."

cd "$BUILD_DIR"

# Verificar se web-ext está disponível
if ! command -v web-ext &> /dev/null; then
    echo "⚠️  web-ext não encontrado, usando zip manual..."
    zip -r "../${XPI_NAME}" ./*
    cd ..
else
    web-ext build --overwrite-dest
    mv web-ext-artifacts/*.zip "../${XPI_NAME}"
    cd ..
fi

echo "✅ XPI criado: ${XPI_NAME}"

# Validar XPI
echo "🔍 Validando XPI..."
echo "📦 Conteúdo:"
unzip -l "$XPI_NAME" | grep -E '\.(js|json|html)$' | awk '{print "   " $4}'

echo
echo "📊 Tamanho: $(ls -lh "$XPI_NAME" | awk '{print $5}')"

# Verificar arquivos essenciais
echo "🔍 Arquivos essenciais:"
for file in manifest.json content.js popup.html seed_profiles.json; do
    if unzip -l "$XPI_NAME" | grep -q "$file"; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file FALTANDO"
    fi
done

echo
echo "🚀 Para instalar:"
echo "   1. Arraste $XPI_NAME para o Firefox"
echo "   2. Ou use about:addons > Install Add-on From File"
echo

# Auto-atualizar extensão carregada no Firefox
echo "🔄 Atualizando extensão no Firefox..."
cp "$BUILD_DIR/content.js" extension/
cp "$BUILD_DIR/manifest.json" extension/

# Criar XPI fixo para desenvolvimento
cp "$XPI_FILE" viespolitico-dev.xpi
echo "🔄 XPI de desenvolvimento atualizado: viespolitico-dev.xpi"

echo "✅ Extensão atualizada!"
echo "🔄 Faça reload no Firefox: about:debugging > This Firefox > Reload"
echo
echo "✨ Build concluído com sucesso!"
