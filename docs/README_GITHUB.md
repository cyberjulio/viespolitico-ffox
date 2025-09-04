# ViésPolítico - Extensão Firefox

Análise automática de viés político no Instagram baseada em perfis seguidos.

## 🚀 Instalação

### Método 1: XPI (Recomendado)
1. Baixe: [viespolitico-firefox-v1.3.1.xpi](viespolitico-firefox-v1.3.1.xpi)
2. Arraste para o Firefox ou use `about:addons` > "Install Add-on From File"

### Método 2: Desenvolvimento
1. Clone o repositório
2. Firefox: `about:debugging` > "Load Temporary Add-on"
3. Selecione `manifest.json`

## 📊 Como Funciona

1. **Acesse qualquer perfil** do Instagram
2. **Clique em "Analisar Perfil"** (botão azul que aparece)
3. **Aguarde a análise** (30-60 segundos)
4. **Veja o resultado** com distribuição detalhada

## 🎯 Algoritmo v1.3.1

- **Análise por distribuição**: Considera predominância, não apenas média
- **100 perfis políticos** brasileiros na base de dados
- **5 categorias**: Extrema Esquerda, Esquerda, Centro, Direita, Extrema Direita
- **Detecção inteligente**: Aguarda resultado da busca, detecta "No results found"

## 📋 Exemplo de Resultado

```
Viés Político
Análise de @usuario:

Seguindo (11/100):
• @jairmessiasbolsonaro
• @nikolasferreiradm
• @carla.zambelli
• @tarcisiogdf
• @astropontes
• @tabataamaralsp
• @lulaoficial
• @brasilparalelo
• @revistaoeste
• @folhadespaulo
• @cnnbrasil

Distribuição:
• Extrema Direita: 5
• Direita: 2
• Centro: 3
• Esquerda: 1
• Extrema Esquerda: 0

Resultado:
Inclinação: Extrema Direita
```

## 🔧 Desenvolvimento

### Estrutura
- `manifest.json` - Configuração da extensão
- `content.js` - Script principal de análise
- `popup.html/js` - Interface do popup
- `background.js` - Script de background
- `options.html/js` - Página de configurações
- `seed_profiles.json` - Base de 100 perfis políticos

### Build
```bash
# Instalar web-ext
npm install -g web-ext

# Criar XPI
web-ext build --overwrite-dest
```

## 📈 Changelog

### v1.3.1 (03/09/2025)
- ✅ Correção de timing na verificação de perfis
- ✅ Detecção de "No results found" para conexões lentas
- ✅ Aguarda até 5 segundos por resultado da busca

### v1.3.0 (03/09/2025)
- ✅ Algoritmo corrigido baseado em distribuição
- ✅ Classificação mais precisa (predominância vs média simples)
- ✅ Resultado detalhado com contagem por categoria

### v1.2.1 (03/09/2025)
- ✅ XPI funcional criado (correção de arquivos faltando)
- ✅ Manifest v2 para melhor compatibilidade Firefox
- ✅ Todos os componentes incluídos (popup, background, options)

## 🔒 Privacidade

- ✅ **Processamento local** - nenhum dado enviado para servidores
- ✅ **Sem coleta de dados** pessoais
- ✅ **Código aberto** e auditável
- ✅ **Permissões mínimas** necessárias

## 📞 Contato

**Desenvolvedor**: @cyberjulio  
**Licença**: MIT  
**Repositório**: https://github.com/cyberjulio/viespolitico-ffox
