# <img src="viespoliticologo.png" width="32" height="32" style="vertical-align: middle;"> ViesPolítico Firefox Extension

Extensão para Firefox que analisa o viés político de perfis do Instagram baseado nos políticos que seguem.

## 🚀 Instalação

1. **Baixe a extensão**: Clique com botão direito em [viespolitico-firefox.xpi](https://github.com/cyberjulio/viespolitico-ffox/releases/latest/download/viespolitico-firefox.xpi) e selecione "Salvar Link Como..."

2. **Instale no Firefox**:
   - Abra o Firefox
   - Digite `about:debugging` na barra de endereços
   - Clique em "This Firefox" > "Load Temporary Add-on"
   - Selecione o arquivo baixado

## 📱 Como Usar

1. **Vá para o Instagram** e faça login
2. **Navegue para um perfil público** ou que você já segue (perfis privados não funcionam)
3. **Clique no botão "Analisar Perfil"** no canto superior direito
4. **Aguarde a análise** (4-5 minutos)
5. **Veja o resultado** no popup

## 🔧 Funcionalidades

- ✅ Análise automática de perfis do Instagram
- ✅ 100+ perfis políticos brasileiros na base de dados
- ✅ Classificação em 5 categorias políticas
- ✅ Interface simples - apenas um clique
- ✅ Zero detecção pelo Instagram
- ✅ Funciona direto da página do perfil

## 🔒 Privacidade

- ✅ Não coleta dados pessoais
- ✅ Funciona localmente no seu navegador
- ✅ Não envia dados para servidores externos

## 📊 Base de Dados

A extensão utiliza uma [lista sugerida de perfis](src/extension/seed_profiles.json) com 80 políticos e 20 veículos de notícias brasileiros para análise. Esta lista foi gerada com auxílio de IA, buscando o máximo balanceamento entre os diferentes espectros políticos brasileiros.

A lista é apenas uma sugestão inicial e pode ser personalizada pelo usuário após a instalação do add-on através das configurações da extensão. Os perfis incluídos foram categorizados com base em posicionamentos públicos e não representam necessariamente a opinião do desenvolvedor sobre os políticos listados.

## 📄 Licença

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

**Esta ferramenta é gratuita e não pode ser comercializada.**

## ⚠️ Disclaimer

Esta ferramenta é fornecida "como está", sem garantias de qualquer tipo, expressas ou implícitas. O desenvolvedor não se responsabiliza por:

- Precisão das análises ou categorizações
- Uso inadequado da ferramenta
- Consequências decorrentes do uso da extensão
- Danos diretos ou indiretos relacionados ao uso

A ferramenta tem fins educacionais e de entretenimento. As análises são baseadas em dados públicos e algoritmos automatizados, podendo não refletir com precisão as preferências políticas reais dos usuários analisados.

O usuário assume total responsabilidade pelo uso da ferramenta e suas consequências.

---

**Desenvolvido por [@cyberjulio](https://instagram.com/cyberjulio)**
