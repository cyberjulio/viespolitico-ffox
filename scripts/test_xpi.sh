#!/bin/bash

echo "=== Teste de Validação dos XPIs ==="
echo

# Função para testar um XPI
test_xpi() {
    local xpi_file="$1"
    local name="$2"
    
    echo "Testando: $name"
    echo "Arquivo: $xpi_file"
    
    if [ ! -f "$xpi_file" ]; then
        echo "❌ Arquivo não encontrado!"
        return 1
    fi
    
    echo "📦 Conteúdo do XPI:"
    unzip -l "$xpi_file" | grep -E '\.(js|json|html)$' | awk '{print "   " $4}'
    
    echo "🔍 Verificando arquivos essenciais:"
    
    # Verificar manifest.json
    if unzip -l "$xpi_file" | grep -q "manifest.json"; then
        echo "   ✅ manifest.json"
    else
        echo "   ❌ manifest.json FALTANDO"
    fi
    
    # Verificar content.js
    if unzip -l "$xpi_file" | grep -q "content.js"; then
        echo "   ✅ content.js"
    else
        echo "   ❌ content.js FALTANDO"
    fi
    
    # Verificar popup.html
    if unzip -l "$xpi_file" | grep -q "popup.html"; then
        echo "   ✅ popup.html"
    else
        echo "   ❌ popup.html FALTANDO"
    fi
    
    # Verificar seed_profiles.json
    if unzip -l "$xpi_file" | grep -q "seed_profiles.json"; then
        echo "   ✅ seed_profiles.json"
    else
        echo "   ❌ seed_profiles.json FALTANDO"
    fi
    
    echo "📊 Tamanho: $(ls -lh "$xpi_file" | awk '{print $5}')"
    echo
}

# Testar XPIs
cd "$(dirname "$0")/.."

echo "1. XPI Original (problemático):"
test_xpi "xpi_build/viespolitico-final.xpi" "XPI Original"

echo "2. XPI Corrigido (Manifest v2):"
test_xpi "firefox_build/viespolitico-firefox-v1.2.1-webext.xpi" "XPI Manifest v2"

echo "3. XPI Manifest v3:"
test_xpi "firefox_build_v3/viespolitico-firefox-v1.2.1-mv3.xpi" "XPI Manifest v3"

echo "=== Resumo ==="
echo "✅ XPI Recomendado para Firefox: firefox_build/viespolitico-firefox-v1.2.1-webext.xpi"
echo "🔧 Para instalar: Arraste o arquivo para Firefox ou use about:addons > Install Add-on From File"
echo
