#!/bin/bash

# Script para atualizar extensão sem reinstalar
# Uso: ./update_extension.sh

echo "🔄 Atualizando extensão carregada no Firefox..."

# Copiar arquivos modificados para o diretório da extensão
cp firefox_build_*/content.js extension/ 2>/dev/null || echo "content.js não encontrado"
cp firefox_build_*/manifest.json extension/ 2>/dev/null || echo "manifest.json não encontrado"

echo "✅ Arquivos atualizados!"
echo "🔄 Agora faça reload no Firefox:"
echo "   about:debugging > This Firefox > Reload"
echo
