# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.2.0] - 2025-01-25

### 🎯 Funcionalidade Principal: Customização de Perfis

#### ✨ Nova Página de Opções
- **Interface completa** para gerenciar perfis políticos
- **Adicionar/remover** perfis personalizados
- **Editar** scores e categorias existentes
- **Filtros** por categoria política
- **Estatísticas** em tempo real

#### 🔧 Funcionalidades de Customização
- **Backup/Restore**: Exportar e importar listas personalizadas
- **Reset**: Voltar para lista padrão a qualquer momento
- **Validação**: Verificação automática de duplicatas e formatos
- **Persistência**: Configurações salvas entre sessões

#### 🎨 Interface Melhorada
- **Botão de configurações** (⚙️) no Instagram
- **Cores por categoria** para melhor visualização
- **Mensagens de feedback** para todas as ações
- **Design responsivo** e intuitivo

#### 🔄 Compatibilidade
- **Funciona no XPI**: Usuários podem customizar mesmo na instalação via arquivo
- **Funciona na instalação manual**: Mantém compatibilidade total
- **Storage local**: Dados salvos no navegador do usuário

### 🛠️ Melhorias Técnicas
- Adicionada permissão `storage` no manifest
- Sistema de fallback: perfis customizados → perfis padrão
- Validação robusta de dados importados
- Interface de opções em aba separada

## [1.1.1] - 2025-01-25

### Adicionado
- 📦 Arquivo XPI instalável (viespolitico-firefox-v1.1.0.xpi)
- 🚀 Instalação simplificada via download direto
- 📝 Documentação atualizada com duas opções de instalação

### Melhorado
- 📋 README com instruções de instalação via XPI
- 🔄 Processo de distribuição simplificado

## [1.1.0] - 2025-01-25

### Atualizado
- 📊 Lista de perfis políticos atualizada (final_profiles_v2.json)
- 📝 Documentação corrigida: Arthur Lira substituindo Marina Silva nos exemplos do Centro
- 🔄 Base de dados refinada com perfis mais precisos

## [1.0.0] - 2025-01-25

### Adicionado
- ✨ Análise automática de viés político no Instagram
- 📊 Base de dados com 100 perfis políticos brasileiros
- 🎯 Classificação em 5 categorias políticas
- 🚀 Interface simples com um clique
- 🔒 Funcionamento local sem coleta de dados
- 📱 Abertura automática do modal de seguidos
- 🎨 Banner de resultado melhorado
- 📋 Carregamento de perfis via arquivo JSON

### Funcionalidades
- Detecção automática de perfis políticos seguidos
- Cálculo de score médio baseado nos perfis encontrados
- Classificação política de Extrema Esquerda a Extrema Direita
- Suporte a 80 políticos + 20 veículos de mídia
- Interface não intrusiva com botão flutuante
- Análise completa em 30-60 segundos

### Perfis Incluídos
- **Extrema Direita**: Jair Bolsonaro, Nikolas Ferreira, Carla Zambelli
- **Direita**: Tarcísio de Freitas, Sérgio Moro, Romeu Zema  
- **Centro**: Simone Tebet, Arthur Lira, Eduardo Paes
- **Esquerda**: Lula, Guilherme Boulos, Fernando Haddad
- **Extrema Esquerda**: Sâmia Bomfim, Erika Hilton, Ivan Valente

### Veículos de Mídia
- **Direita**: Jovem Pan, Brasil Paralelo, Revista Oeste
- **Centro**: Globo, Folha, CNN Brasil
- **Esquerda**: Carta Capital, Revista Fórum, Brasil de Fato
