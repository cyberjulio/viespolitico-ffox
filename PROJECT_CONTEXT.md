# ViésPolítico - Contexto do Projeto

## Visão Geral
Extensão para Firefox que analisa o viés político de perfis do Instagram baseado nos políticos que seguem.

## Estrutura do Projeto
- `viespolitico/` - Repositório principal conectado ao GitHub
- `viespolitico-dev/` - Ambiente de build para gerar XPIs

## Fluxo de Desenvolvimento
1. Código fonte em `/src/extension/`
2. Commits e pushes direto do `/viespolitico/` para GitHub
3. Build de XPIs usando `viespolitico-dev/scripts/build_xpi.sh`

## Funcionalidades Principais
- Análise automática de perfis públicos do Instagram
- Base de dados com 100+ perfis políticos brasileiros (80 políticos + 20 veículos de notícias)
- Classificação em 5 categorias políticas
- Interface simples - um clique para analisar
- Funciona localmente no navegador (sem envio de dados externos)

## Como Funciona
1. Usuário vai ao Instagram e navega para um perfil público
2. Clica no botão "Analisar Perfil" 
3. Aguarda 4-5 minutos para análise
4. Vê resultado no popup da extensão

## Características Técnicas
- Zero detecção pelo Instagram
- Não coleta dados pessoais
- Base de dados personalizável pelo usuário
- Lista inicial gerada com IA para balanceamento político

## Status Legal
- Licença Creative Commons (não comercial)
- Fins educacionais/entretenimento
- Desenvolvido por @cyberjulio
