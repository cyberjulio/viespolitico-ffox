# Correção do Problema XPI - ViésPolítico Firefox Extension

## 🐛 Problema Identificado

O arquivo XPI original (`xpi_build/viespolitico-final.xpi`) não funcionava quando instalado no Firefox porque:

1. **Arquivos faltando**: Só continha `manifest.json`, `content.js` e `seed_profiles.json`
2. **Faltavam componentes essenciais**:
   - `popup.html` - Interface do popup
   - `popup.js` - Lógica do popup  
   - `background.js` - Script de background
   - `options.html` e `options.js` - Página de configurações

## ✅ Solução Implementada

### 1. XPI Corrigido (Manifest v2) - **RECOMENDADO**
**Arquivo**: `firefox_build/viespolitico-firefox-v1.2.1-webext.xpi`

- ✅ Todos os arquivos necessários incluídos
- ✅ Manifest v2 (melhor compatibilidade com Firefox atual)
- ✅ Criado com `web-ext` (ferramenta oficial Mozilla)
- ✅ Tamanho: 11KB (vs 4.5KB do original quebrado)

### 2. XPI Manifest v3 (Futuro)
**Arquivo**: `firefox_build_v3/viespolitico-firefox-v1.2.1-mv3.xpi`

- ✅ Preparado para futuras versões do Firefox
- ✅ Manifest v3 com sintaxe atualizada
- ⚠️ Pode não funcionar em versões antigas do Firefox

## 📦 Arquivos Incluídos no XPI Corrigido

```
viespolitico-firefox-v1.2.1-webext.xpi
├── manifest.json          # Configuração da extensão
├── content.js            # Script principal (análise)
├── background.js         # Script de background
├── popup.html           # Interface do popup
├── popup.js             # Lógica do popup
├── options.html         # Página de configurações
├── options.js           # Lógica das configurações
└── seed_profiles.json   # Base de dados (100 perfis)
```

## 🚀 Como Instalar

### Método 1: Arrastar e Soltar
1. Abra o Firefox
2. Arraste o arquivo `firefox_build/viespolitico-firefox-v1.2.1-webext.xpi` para a janela do Firefox
3. Clique em "Adicionar" quando solicitado

### Método 2: Menu de Add-ons
1. Firefox → `about:addons`
2. Clique no ícone de engrenagem ⚙️
3. "Install Add-on From File..."
4. Selecione `firefox_build/viespolitico-firefox-v1.2.1-webext.xpi`

### Método 3: Desenvolvimento (Temporário)
1. Firefox → `about:debugging`
2. "This Firefox" → "Load Temporary Add-on"
3. Selecione `firefox_build/manifest.json`

## 🔧 Diferenças Técnicas

### XPI Original (Quebrado)
```json
{
  "manifest_version": 3,
  "name": "ViésPolítico",
  "version": "1.2.1",
  // Apenas content_scripts, sem popup/background
}
```

### XPI Corrigido (Funcional)
```json
{
  "manifest_version": 2,
  "name": "ViésPolítico", 
  "version": "1.2.1",
  "background": { "scripts": ["background.js"] },
  "browser_action": { "default_popup": "popup.html" },
  "options_ui": { "page": "options.html" },
  // Todos os componentes incluídos
}
```

## 🧪 Teste de Validação

Execute o script de teste para verificar qualquer XPI:

```bash
cd /path/to/viespolitico
./test_xpi.sh
```

## 📋 Checklist de Funcionalidades

Após instalar o XPI corrigido, verifique:

- [ ] Ícone da extensão aparece na barra de ferramentas
- [ ] Clique no ícone abre o popup
- [ ] Vá para instagram.com/qualquer_perfil
- [ ] Botão "Analisar Perfil" aparece na página
- [ ] Clique no botão executa a análise
- [ ] Resultado aparece no popup

## 🔄 Próximos Passos

1. **Testar XPI corrigido** em diferentes versões do Firefox
2. **Atualizar repositório GitHub** com XPI funcional
3. **Documentar processo** de build para futuras versões
4. **Considerar migração** para Manifest v3 quando Firefox suportar totalmente

## 📁 Estrutura de Arquivos

```
viespolitico/
├── extension/                    # Versão de desenvolvimento
├── firefox_build/               # ✅ XPI Manifest v2 (FUNCIONAL)
├── firefox_build_v3/           # XPI Manifest v3 (futuro)
├── xpi_build/                  # ❌ XPI original (quebrado)
└── XPI_FIX_README.md          # Esta documentação
```

---

**Status**: ✅ **PROBLEMA RESOLVIDO**  
**XPI Funcional**: `firefox_build/viespolitico-firefox-v1.2.1-webext.xpi`  
**Data**: 03/09/2025  
**Desenvolvedor**: @cyberjulio
