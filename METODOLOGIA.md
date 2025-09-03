# Metodologia de Construção da Lista de Perfis

A lista de 100 perfis públicos brasileiros no Instagram foi elaborada a partir de critérios objetivos, garantindo diversidade ideológica e relevância no cenário político e midiático.

---

## 1. Escopo

Foram incluídos apenas:
- **Políticos e ex-políticos** com cargos eletivos (vereadores, deputados, senadores, governadores, prefeitos, presidentes, ministros ou ex-ministros).
- **Veículos de mídia** com atuação reconhecida no debate político nacional, classificados conforme sua linha editorial.

**Foram excluídos**: ativistas, jornalistas, escritores, influenciadores ou celebridades sem atuação institucional ou editorial política.

---

## 2. Critérios de Seleção

1. **Perfis válidos e ativos** no Instagram.
2. **Relevância política ou midiática**, considerando ocupação de cargos oficiais ou importância editorial.
3. **Popularidade**, priorizando contas com 500 mil seguidores ou mais, sempre que possível.
4. **Atualidade**, contemplando políticos em atividade ou com relevância até 2025.

---

## 3. Balanceamento Ideológico

A lista foi estruturada para assegurar equilíbrio entre os espectros políticos:
- **80 políticos** (20 Centro, 20 Direita, 20 Esquerda, 10 Extrema Direita, 10 Extrema Esquerda).
- **20 veículos de mídia** (4 por espectro: Centro, Direita, Esquerda, Extrema Direita, Extrema Esquerda).

A classificação levou em conta a atuação prática e o posicionamento ideológico dos perfis, evitando simplificações automáticas baseadas apenas em filiação partidária.

---

## 4. Estrutura de Dados

O resultado foi organizado em formato JSON estruturado, com os seguintes campos:
- **username**: identificador oficial no Instagram (@).
- **score**: valor numérico associado ao espectro (2 = Extrema Direita, 1 = Direita, 0 = Centro, -1 = Esquerda, -2 = Extrema Esquerda).
- **category**: rótulo textual do espectro.
- **type**: "politico" ou "veiculo".

---

## 5. Resultado Final

- **100 perfis oficiais e ativos**, representando diferentes espectros ideológicos.
- **Equilíbrio rigoroso** entre espectros, garantindo diversidade e representatividade.
- **Entrega final em JSON padronizado**, pronto para ser utilizado em análises, visualizações ou integrações.

---

## 📊 Distribuição Final

| Espectro | Políticos | Veículos | Total |
|----------|-----------|----------|-------|
| Extrema Esquerda (-2) | 10 | 4 | 14 |
| Esquerda (-1) | 20 | 4 | 24 |
| Centro (0) | 20 | 4 | 24 |
| Direita (1) | 20 | 4 | 24 |
| Extrema Direita (2) | 10 | 4 | 14 |
| **Total** | **80** | **20** | **100** |

---

*Esta metodologia garante que a ferramenta ViesPolítico ofereça análises equilibradas e representativas do espectro político brasileiro.*
