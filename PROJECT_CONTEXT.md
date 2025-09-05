# ViésPolítico - Contexto do Projeto

## Visão Geral
Extensão para Firefox que analisa o viés político de perfis do Instagram baseado nos políticos que seguem.

## Status Atual - v1.4.6
- ✅ Histórico Git limpo (sem credenciais)
- ✅ Fechamento automático do modal após análise
- ✅ Sistema de desenvolvimento otimizado
- ✅ Release v1.4.5 público disponível
- 🔄 v1.4.6 em desenvolvimento (correções de UX)

## Estrutura do Projeto
- `viespolitico/` - Repositório principal conectado ao GitHub
- `viespolitico-dev/` - Ambiente de build para gerar XPIs
- `viespolitico-backup/` - Backup local (sem remote GitHub)

## Fluxo de Desenvolvimento
1. Código fonte em `/src/extension/`
2. Commits e pushes direto do `/viespolitico/` para GitHub
3. Build de XPIs usando `viespolitico-dev/scripts/build_xpi.sh`
4. XPI fixo para desenvolvimento: `viespolitico-dev.xpi`

## Melhorias Recentes
- **v1.4.5:** Remoção de logs automáticos, histórico Git limpo
- **v1.4.6:** Fechamento automático do modal de seguidos após análise
- **Sistema Dev:** XPI fixo para desenvolvimento (`viespolitico-dev.xpi`)
- **Segurança:** Credenciais removidas do histórico, backup isolado

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
