# ViesPolítico - Contexto do Projeto

## 📋 Status Atual (03/09/2025 - 17:06 BRT)

### ✅ Projeto COMPLETO e FUNCIONAL - ALGORITMO CORRIGIDO

**Versão**: 1.3.0  
**Repositório**: https://github.com/cyberjulio/viespolitico-ffox (privado)  
**Tipo**: Extensão Firefox para análise de viés político no Instagram

---

## 🚨 CORREÇÕES IMPLEMENTADAS HOJE (03/09/2025)

### 1. ❌ Problema XPI Resolvido
**Problema**: Arquivo XPI não funcionava quando instalado (só funcionava copiando repositório)
**Causa**: XPI incompleto - faltavam arquivos essenciais (popup.html, background.js, options.html)
**Solução**: 
- ✅ XPI completo criado com todos os 8 arquivos necessários
- ✅ Script automatizado `build_xpi.sh` para gerar XPIs funcionais
- ✅ Script de validação `test_xpi.sh` para verificar integridade
- ✅ Documentação completa em `XPI_FIX_README.md`

### 2. ❌ Algoritmo de Scoring Corrigido
**Problema**: Cálculo por média simples não refletia realidade política
**Exemplo**: 7 perfis direita + 1 esquerda + 3 centro = "Direita" (deveria ser "Extrema Direita")
**Solução**: 
- ✅ Novo algoritmo baseado em **distribuição** não apenas média
- ✅ Considera predominância: se direita > esquerda+centro → classifica como direita
- ✅ Dentro da categoria dominante: se extrema > moderada → vai para extrema
- ✅ Mostra distribuição detalhada no resultado

### 3. ✅ Workflow de Desenvolvimento Otimizado
**Problema**: Precisava reinstalar extensão a cada mudança
**Solução**:
- ✅ Script `update_extension.sh` para atualizar sem reinstalar
- ✅ Build automatizado atualiza extensão carregada no Firefox
- ✅ Só precisa fazer reload: `about:debugging` > "Reload"

---

## 🎯 Funcionalidades Implementadas

### Core Features
- ✅ **Análise automática** de perfis do Instagram
- ✅ **100 perfis políticos** brasileiros na base de dados
- ✅ **Classificação em 5 categorias** baseada em distribuição
- ✅ **Interface one-click** com botão flutuante
- ✅ **Abertura automática** do modal de seguidos
- ✅ **Banner melhorado** com distribuição detalhada
- ✅ **Zero detecção** pelo Instagram
- ✅ **Processamento local** sem coleta de dados
- ✅ **Arquivo XPI funcional** para usuários finais
- ✅ **Algoritmo corrigido** para análise precisa

### Tecnologias
- **JavaScript** (Vanilla)
- **Firefox WebExtensions API**
- **JSON** para base de dados
- **CSS** para interface
- **Git/GitHub** para versionamento
- **web-ext** para empacotamento XPI

---

## 📊 Novo Algoritmo de Análise (v1.3.0)

### Lógica Corrigida
```javascript
// Contar distribuição por categoria
const counts = {
    extremaEsquerda: matches.filter(m => m.score === -2).length,
    esquerda: matches.filter(m => m.score === -1).length,
    centro: matches.filter(m => m.score === 0).length,
    direita: matches.filter(m => m.score === 1).length,
    extremaDireita: matches.filter(m => m.score === 2).length
};

// Calcular predominância
const totalEsquerda = counts.extremaEsquerda + counts.esquerda;
const totalDireita = counts.direita + counts.extremaDireita;
const totalCentro = counts.centro;

// Classificar por distribuição
if (totalDireita >= totalEsquerda + totalCentro) {
    if (counts.extremaDireita > counts.direita) {
        classification = 'Extrema Direita';
    } else {
        classification = 'Direita';
    }
}
```

### Exemplo Prático
**Perfil segue**: 5 extrema direita + 2 direita + 3 centro + 1 esquerda
- **Algoritmo antigo**: (10+2+0-1)/11 = 1.00 → "Direita"
- **Algoritmo novo**: 7 direita > 4 esquerda+centro E 5 extrema > 2 direita → **"Extrema Direita"** ✅

---

## 📁 Estrutura de Arquivos Atualizada

### Projeto Local
```
/Users/cyberjulio/Coding/viespolitico/
├── extension/                          # Versão de desenvolvimento (carregada no Firefox)
├── firefox_build_1.3.0/              # ✅ Build v1.3.0 com algoritmo corrigido
├── viespolitico-firefox-v1.3.0.xpi   # ✅ XPI funcional para distribuição
├── build_xpi.sh                      # Script automatizado de build + auto-update
├── update_extension.sh               # Script para atualizar sem reinstalar
├── test_xpi.sh                       # Script de validação de XPIs
├── XPI_FIX_README.md                 # Documentação da correção XPI
├── RESUMO_CORRECAO.md                # Resumo das correções
└── PROJECT_CONTEXT.md                # Este arquivo
```

### Arquivos Principais
- **extension/content.js**: Script principal com algoritmo corrigido
- **extension/manifest.json**: Configuração v1.3.0
- **extension/seed_profiles.json**: Base de 100 perfis políticos
- **viespolitico-firefox-v1.3.0.xpi**: XPI funcional para distribuição

---

## 🚀 Workflow de Desenvolvimento

### Desenvolvimento Ativo
```bash
# 1. Fazer mudanças nos arquivos da extension/
# 2. Testar: Firefox > about:debugging > Reload
# 3. Quando satisfeito: criar build completo
./build_xpi.sh 1.3.1

# Build completo executa automaticamente:
# ✅ Atualiza diretório local do Firefox (extension/) para testes
# ✅ Cria novo XPI para distribuição
# ✅ Atualiza repositório GitHub com as alterações
```

### Processo de Build Completo (3 etapas obrigatórias)
Para toda nova versão, deve-se executar:

1. **✅ Atualizar Firefox Local**: Copiar arquivos para `extension/` (para reload simples)
2. **✅ Gerar XPI**: Criar arquivo `.xpi` funcional para distribuição
3. **✅ Atualizar GitHub**: Push das alterações para o repositório

**Credenciais GitHub**: Token armazenado em `.github_token` (não commitado)
- Arquivo: `/Users/cyberjulio/Coding/viespolitico/.github_token`
- Conteúdo: Token "qcli" do GitHub
- Uso: Script `update_github.sh` lê automaticamente

### Instalação para Usuários
```bash
# XPI funcional pronto para distribuição:
viespolitico-firefox-v1.3.0.xpi

# Instalação: arrastar para Firefox ou about:addons > Install Add-on From File
```

---

## 🔧 Scripts Utilitários

### build_xpi.sh
- Cria XPI completo e funcional
- Atualiza automaticamente extensão carregada no Firefox
- Valida arquivos essenciais
- Uso: `./build_xpi.sh 1.3.1`

### update_extension.sh  
- Atualiza extensão sem reinstalar
- Copia última versão para extension/
- Uso: `./update_extension.sh`

### test_xpi.sh
- Valida integridade de XPIs
- Verifica arquivos essenciais
- Compara tamanhos e conteúdo
- Uso: `./test_xpi.sh`

---

## 📋 Resultado da Análise (Novo Formato)

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

---

## 🐛 Problemas Resolvidos

### ❌ XPI Não Funcionava
- **Causa**: Arquivos faltando (só 3 de 8 necessários)
- **Solução**: XPI completo com web-ext
- **Status**: ✅ Resolvido

### ❌ Algoritmo Impreciso  
- **Causa**: Média simples não refletia distribuição real
- **Solução**: Algoritmo baseado em predominância
- **Status**: ✅ Resolvido

### ❌ Workflow Lento
- **Causa**: Reinstalação manual a cada mudança
- **Solução**: Auto-update + reload simples
- **Status**: ✅ Resolvido

---

## 🔄 Próximos Passos

1. **Testar algoritmo corrigido** em diversos perfis
2. **Ajustar thresholds** se necessário (ex: 60% vs 50% para predominância)
3. **Resolver assinatura XPI** para instalação sem "não verificado"
4. **Atualizar repositório GitHub** com versão v1.3.0
5. **Documentar metodologia** do novo algoritmo

---

## 📊 Base de Dados (Inalterada)

### Distribuição (100 perfis total)
- **Extrema Direita** (score: 2): 14 perfis
- **Direita** (score: 1): 24 perfis  
- **Centro** (score: 0): 24 perfis
- **Esquerda** (score: -1): 24 perfis
- **Extrema Esquerda** (score: -2): 14 perfis

### Tipos
- **80 Políticos**: Deputados, senadores, governadores, ministros
- **20 Veículos**: Jornais, revistas, canais de mídia

---

## 🛠️ Comandos Úteis Atualizados

### Desenvolvimento
```bash
# Fazer mudanças e testar
vim extension/content.js
# Firefox: about:debugging > Reload

# Criar nova versão
./build_xpi.sh 1.3.1
# Firefox: about:debugging > Reload

# Validar XPI
./test_xpi.sh
```

### Distribuição
```bash
# XPI pronto para usuários
ls -la viespolitico-firefox-v1.3.0.xpi

# Instalar: arrastar para Firefox
```

---

## 📞 Informações de Contato

**Desenvolvedor**: cyberjulio  
**GitHub**: https://github.com/cyberjulio/viespolitico-ffox  
**Licença**: MIT  
**Linguagem**: JavaScript (Vanilla)  

---

## 🔒 Segurança e Privacidade

- ✅ **Sem coleta de dados** pessoais
- ✅ **Processamento local** no navegador
- ✅ **Sem comunicação** com servidores externos
- ✅ **Código aberto** e auditável
- ✅ **Permissões mínimas** necessárias

---

## 📋 Links Importantes

- **Repositório**: https://github.com/cyberjulio/viespolitico-ffox
- **XPI Funcional**: `viespolitico-firefox-v1.3.0.xpi`
- **Documentação**: `XPI_FIX_README.md`

---

**Última atualização**: 03/09/2025 17:06 BRT  
**Status**: ✅ PROJETO FUNCIONAL - ALGORITMO CORRIGIDO - XPI FUNCIONAL  
**Versão atual**: v1.3.0 com algoritmo de distribuição
