# ViesPolítico Firefox Extension

Uma extensão para Firefox que analisa o viés político de perfis do Instagram baseado nos políticos e veículos de mídia que seguem.

## 🎯 Funcionalidades

- ✅ **Análise automática** de perfis do Instagram
- ✅ **100+ perfis políticos** brasileiros na base de dados
- ✅ **Classificação política** em 5 categorias
- ✅ **Interface simples** - apenas um clique
- ✅ **Zero detecção** pelo Instagram
- ✅ **Funciona direto da página** do perfil

## 📊 Categorias de Classificação

| Score | Categoria | Descrição |
|-------|-----------|-----------|
| -2 | Extrema Esquerda | PSOL, PCdoB, movimentos sociais |
| -1 | Esquerda | PT, PSB, políticos progressistas |
| 0 | Centro | PSDB, MDB, políticos moderados |
| +1 | Direita | NOVO, DEM, liberais conservadores |
| +2 | Extrema Direita | PL, Bolsonarismo, conservadores |

## 🚀 Instalação

### Método 1: Arquivo Instalável (Recomendado)

1. **Baixe o arquivo XPI**:
   - [📦 viespolitico-firefox-v1.1.1.xpi](https://github.com/cyberjulio/viespolitico-ffox/raw/main/viespolitico-firefox-v1.1.1.xpi)

2. **Instale no Firefox**:
   - Arraste o arquivo `.xpi` para o Firefox
   - OU vá em `about:addons` > ⚙️ > "Install Add-on From File"
   - Selecione o arquivo baixado

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

5. **Selecione o arquivo** `manifest.json` na pasta do projeto

6. **Pronto!** A extensão está instalada

## 📱 Como Usar

### Passo a Passo

1. **Vá para o Instagram** e faça login normalmente

2. **Navegue para qualquer perfil** que deseja analisar
   ```
   https://instagram.com/usuario_exemplo
   ```

3. **Clique no botão azul** "Analisar Perfil" no canto superior direito

4. **Aguarde a análise** (30-60 segundos para 100 perfis)

5. **Veja o resultado** no popup final

### Exemplo de Resultado

```
Viés Político
Análise de @usuario_exemplo:

Seguindo (7/100):
• @jairmessiasbolsonaro
• @tarcisiogdf
• @simonetebet
• @lula
• @guilhermeboulos
• @cartacapital
• @revistaforum

Resultado:
Média final: -0.14
Inclinação: Centro
```

## 🔧 Estrutura do Projeto

```
viespolitico-ffox/
├── manifest.json           # Configuração da extensão
├── content.js             # Script principal
├── popup.html             # Interface do popup
├── seed_profiles.json     # Base de 100 perfis políticos
├── icons/                 # Ícones da extensão
└── README.md             # Esta documentação
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

## 📊 Limitações

- **Perfis privados**: Não é possível analisar
- **Rate limiting**: Instagram pode limitar buscas muito rápidas
- **Precisão**: Baseada apenas nos perfis seguidos publicamente
- **Contexto**: Não considera posts ou interações

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

## 📈 Roadmap

- [ ] Publicação na Mozilla Add-ons Store
- [ ] Análise de posts além de perfis seguidos
- [ ] Interface gráfica melhorada
- [ ] Exportação de relatórios
- [ ] Suporte para Chrome/Edge
- [ ] API para desenvolvedores

---

**Desenvolvido por [@cyberjulio](https://github.com/cyberjulio)**
