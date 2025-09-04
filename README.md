# ViesPolítico Firefox Extension

Uma extensão para Firefox que analisa o viés político de perfis do Instagram baseado nos políticos e veículos de mídia que seguem.

## 🎯 Funcionalidades

- ✅ **Análise automática** de perfis do Instagram
- ✅ **100+ perfis políticos** brasileiros na base de dados
- ✅ **Classificação política** em 5 categorias
- ✅ **Interface simples** - apenas um clique
- ✅ **Zero detecção** pelo Instagram
- ✅ **Funciona direto da página** do perfil
- ✅ **Logs automáticos** para debug
- ✅ **Timing otimizado** - análise rápida e precisa

## 🚀 Instalação

### Instalação Método 1 (XPI - Usuários)

1. **Baixe o arquivo XPI**:
   - [📦 viespolitico-firefox.xpi](https://github.com/cyberjulio/viespolitico-ffox/releases/latest/download/viespolitico-firefox.xpi)

2. **Instale no Firefox**:
   - Vá em `about:debugging` > "This Firefox" > "Load Temporary Add-on"
   - Selecione o arquivo baixado
   - ⚠️ **Não arraste** - use "Load Temporary Add-on"

3. **Confirme a instalação** quando solicitado

4. **Pronto!** A extensão está instalada

### Método 2: Instalação Manual (Desenvolvedores)

1. **Baixe o projeto**:
   ```bash
   git clone https://github.com/cyberjulio/viespolitico-ffox.git
   cd viespolitico-ffox
   ```

2. **Abra o Firefox** e digite na barra de endereços:
   ```
   about:debugging
   ```

3. **Clique em "This Firefox"** no menu lateral

4. **Clique em "Load Temporary Add-on"**

5. **Selecione o arquivo** `src/extension/manifest.json`

6. **Pronto!** A extensão está instalada

## 📱 Como Usar

### Passo a Passo

1. **Vá para o Instagram** e faça login normalmente

2. **Navegue para qualquer perfil** que deseja analisar
   ```
   https://instagram.com/usuario_exemplo
   ```

3. **Clique no botão azul** "Analisar Perfil" no canto superior direito

4. **⚠️ IMPORTANTE - Durante a análise**:
   - **NÃO feche a aba** do navegador
   - **Pode usar outra janela** do navegador normalmente
   - **Se quiser usar outra aba**: ANTES de iniciar, arraste esta aba para fora do navegador, separando em duas janelas
   - **Aguarde 30-60 segundos** para análise completa

5. **Veja o resultado** no popup final

### ⚙️ Customizar Lista de Perfis

1. **Clique no botão de configurações** (⚙️) no Instagram

2. **Ou acesse**: `about:addons` > ViesPolítico > "Preferências"

3. **Na página de opções você pode**:
   - ➕ **Adicionar** novos perfis políticos
   - ✏️ **Editar** scores e categorias
   - 🗑️ **Remover** perfis existentes
   - 📤 **Exportar** sua lista personalizada
   - 📥 **Importar** listas de outros usuários
   - 🔄 **Resetar** para a lista padrão

### Exemplo de Resultado

**Exemplo A - Perfil de Direita:**
```
Viés Político
Análise de @joaosilva:

Seguindo (3/100):
• @tarcisiogdf
• @sergiomoro_oficial
• @romeuzemaoficial

Resultado:
Média final: 1.00
Inclinação: Direita
```

**Exemplo B - Perfil de Esquerda:**
```
Viés Político
Análise de @mariasantos:

Seguindo (3/100):
• @lulaoficial
• @guilhermeboulos.oficial
• @haddad_fernando

Resultado:
Média final: -1.00
Inclinação: Esquerda
```

## 🔧 Estrutura do Projeto

```
viespolitico-ffox/
├── README.md              # Esta documentação
├── CHANGELOG.md           # Histórico de versões
├── LICENSE               # Licença do projeto
├── src/                  # Código fonte
│   └── extension/        # Arquivos da extensão Firefox
│       ├── manifest.json # Configuração da extensão
│       ├── content.js    # Script principal
│       ├── popup.html    # Interface do popup
│       ├── options.html  # Página de configurações
│       ├── seed_profiles.json # Base de 100 perfis políticos
│       └── icons/        # Ícones da extensão
├── builds/               # Builds compilados
├── scripts/              # Scripts de automação
└── docs/                 # Documentação adicional
```

## 📋 Base de Dados

A extensão analisa **100 perfis** divididos em:

- **80 Políticos**: Deputados, senadores, governadores, ministros
- **20 Veículos de Mídia**: Jornais, revistas, canais de notícias

### Exemplos por Categoria

**Extrema Direita**: Jair Bolsonaro, Nikolas Ferreira, Carla Zambelli  
**Direita**: Tarcísio de Freitas, Sérgio Moro, Romeu Zema  
**Centro**: Simone Tebet, Arthur Lira, Eduardo Paes  
**Esquerda**: Lula, Guilherme Boulos, Fernando Haddad  
**Extrema Esquerda**: Sâmia Bomfim, Erika Hilton, Ivan Valente  

## ⚙️ Configuração Avançada

### Personalizando a Lista de Perfis

Edite o arquivo `seed_profiles.json` para adicionar/remover perfis:

```json
[
  {
    "username": "nome_do_perfil",
    "score": 1,
    "category": "Direita"
  }
]
```

### Scores Personalizados

- `-2`: Extrema Esquerda
- `-1`: Esquerda  
- `0`: Centro
- `1`: Direita
- `2`: Extrema Direita

## 🛠️ Desenvolvimento

### Requisitos

- Firefox 88+
- Conhecimento básico de JavaScript
- Acesso ao Instagram

### Testando Localmente

1. Clone o repositório
2. Faça suas modificações
3. Recarregue a extensão em `about:debugging`
4. Teste em perfis do Instagram

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 🔧 Personalização

Os perfis incluídos são sugestões baseadas em metodologia documentada ([ver METODOLOGIA.md](METODOLOGIA.md)). Customize a lista editando `seed_profiles.json` respeitando a formatação existente.

## 🔒 Privacidade

- ✅ **Não coleta dados** pessoais
- ✅ **Não armazena** informações dos usuários
- ✅ **Funciona localmente** no seu navegador
- ✅ **Não envia dados** para servidores externos

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

- **Issues**: Reporte bugs ou sugestões nas [Issues](https://github.com/cyberjulio/viespolitico-ffox/issues)
- **Discussões**: Participe das [Discussions](https://github.com/cyberjulio/viespolitico-ffox/discussions)

## 📄 Licença

Este projeto é licenciado sob **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**.

### ✅ Permitido:
- **Uso pessoal** e educacional gratuito
- **Modificações** e adaptações
- **Compartilhamento** com atribuição
- **Pesquisa** e fins acadêmicos

### ❌ Proibido:
- **Uso comercial** de qualquer tipo
- **Venda** da ferramenta ou versões modificadas
- **Uso empresarial** para lucro
- **Remoção** de créditos do autor

### 📋 Condições:
- **Atribuição**: Deve creditar o autor original
- **Mesma licença**: Modificações devem usar a mesma licença
- **Indicar mudanças**: Se modificar, deve indicar as alterações

**Esta ferramenta será sempre gratuita e não pode ser comercializada.**

---

**Desenvolvido por [@cyberjulio](https://github.com/cyberjulio)**
