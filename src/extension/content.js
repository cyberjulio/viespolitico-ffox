/*
 * ViésPolítico - Análise Política Automática do Instagram
 * Desenvolvido por @cyberjulio
 * GitHub: https://github.com/cyberjulio
 * 
 * Licença: CC BY-NC-SA 4.0 (Não Comercial)
 * Este software é gratuito para sempre e não pode ser usado comercialmente.
 */

// ViesPolítico - Content Script

// Sistema de logs automático
let debugLogs = [];
function log(message) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${message}`;
    console.log(logEntry);
    debugLogs.push(logEntry);
}

function saveLogs() {
    const logContent = debugLogs.join('\n');
    const blob = new Blob([logContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `viespolitico-debug-${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.log`;
    a.click();
    URL.revokeObjectURL(url);
}
log('ViesPolítico extension loaded');

let seedProfiles = [];

// Carregar perfis do storage ou arquivo JSON
async function carregarPerfis() {
    try {
        // Tentar carregar perfis customizados primeiro
        const result = await browser.storage.local.get('customProfiles');
        if (result.customProfiles && result.customProfiles.length > 0) {
            seedProfiles = result.customProfiles;
            log(`Carregados ${seedProfiles.length} perfis customizados`);
            return true;
        }
        
        // Se não houver customizados, carregar padrão
        const response = await fetch(chrome.runtime.getURL('seed_profiles.json'));
        seedProfiles = await response.json();
        log(`Carregados ${seedProfiles.length} perfis padrão`);
        return true;
    } catch (error) {
        console.error('Erro ao carregar perfis:', error);
        return false;
    }
}

async function analisarPerfil() {
    log('Iniciando análise completa...');
    
    // Extrair nome do perfil da URL ou página
    let profileName = '';
    const urlMatch = window.location.pathname.match(/\/([^\/]+)\/?$/);
    if (urlMatch) {
        profileName = urlMatch[1];
    }
    
    // Se não conseguiu da URL, tentar pegar do título da página
    if (!profileName) {
        const titleMatch = document.title.match(/^([^(]+)/);
        if (titleMatch) {
            profileName = titleMatch[1].trim();
        }
    }
    
    log(`Analisando perfil: ${profileName}`);
    
    // Carregar perfis se necessário
    if (seedProfiles.length === 0) {
        const loaded = await carregarPerfis();
        if (!loaded) {
            alert('Erro ao carregar lista de políticos');
            return;
        }
    }
    
    // Verificar se modal já está aberto
    let modal = document.querySelector('[role="dialog"]');
    
    if (!modal) {
        log('Abrindo modal de seguidos...');
        
        // Procurar link de "following/seguindo"
        const followingSelectors = [
            'a[href*="/following/"]',
            'a[href*="following"]'
        ];
        
        let followingLink = null;
        for (let selector of followingSelectors) {
            const links = document.querySelectorAll(selector);
            for (let link of links) {
                if (link.offsetParent !== null) {
                    followingLink = link;
                    break;
                }
            }
            if (followingLink) break;
        }
        
        // Se não encontrou por href, procurar por texto
        if (!followingLink) {
            const allLinks = document.querySelectorAll('a');
            for (let link of allLinks) {
                const text = link.textContent.toLowerCase();
                if ((text.includes('following') || text.includes('seguindo')) && 
                    link.offsetParent !== null) {
                    followingLink = link;
                    break;
                }
            }
        }
        
        if (!followingLink) {
            alert('Link de "seguindo" não encontrado. Certifique-se que está em um perfil do Instagram.');
            return;
        }
        
        // Clicar no link
        followingLink.click();
        
        // Aguardar modal abrir
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        modal = document.querySelector('[role="dialog"]');
        if (!modal) {
            alert('Modal não abriu. Tente clicar manualmente em "seguindo".');
            return;
        }
    }
    
    const searchBox = modal.querySelector('input[placeholder="Search"]');
    if (!searchBox) {
        alert('Caixa de pesquisa não encontrada');
        return;
    }
    
    log(`Iniciando análise com ${seedProfiles.length} perfis...`);
    const matches = [];
    
    for (let i = 0; i < seedProfiles.length; i++) {
        const profile = seedProfiles[i];
        
        // Atualizar botão
        const btn = document.getElementById('viespolitico-btn');
        if (btn) btn.textContent = `${i+1}/${seedProfiles.length}: @${profile.username}`;
        
        log(`[${i+1}/${seedProfiles.length}] Testando @${profile.username}...`);
        
        // Limpar e digitar
        searchBox.value = '';
        searchBox.focus();
        searchBox.value = profile.username;
        searchBox.dispatchEvent(new Event('input', { bubbles: true }));
        
        log(`Digitado: "${profile.username}" - Aguardando resultado...`);
        
        // Aguardar resultado aparecer (máximo 10 segundos)
        let found = false;
        let attempts = 0;
        const maxAttempts = 15; // 3 segundos (15 x 200ms)
        
        while (attempts < maxAttempts && !found) {
            await new Promise(resolve => setTimeout(resolve, 200));
            attempts++;
            
            const allElements = Array.from(modal.querySelectorAll('*'));
            
            // Debug: contar elementos visíveis
            const visibleElements = allElements.filter(el => el.offsetParent !== null);
            log(`Tentativa ${attempts}: ${visibleElements.length} elementos visíveis`);
            
            // Verificar se encontrou o perfil com métodos mais rigorosos
            for (let element of allElements) {
                // Método 1: Link direto (mais confiável)
                if (element.href && 
                    element.href.includes(`instagram.com/${profile.username}`) && 
                    element.offsetParent !== null) {
                    found = true;
                    log(`✅ FOUND via href: @${profile.username} - ${element.href}`);
                    break;
                }
                
                // Método 2: Texto exato do username em elementos pequenos
                if (element.textContent && element.offsetParent !== null) {
                    const text = element.textContent.trim();
                    
                    // Deve ser exatamente o username ou @username, em elemento pequeno
                    if ((text === profile.username || text === '@' + profile.username) && 
                        text.length < 50) {
                        found = true;
                        log(`✅ FOUND via exact text: @${profile.username} - "${text}"`);
                        break;
                    }
                }
                
                // Método 3: Alt text de imagem de perfil
                if (element.tagName === 'IMG' && 
                    element.alt && 
                    element.alt.toLowerCase().includes(profile.username.toLowerCase()) &&
                    element.alt.includes('profile picture')) {
                    found = true;
                    log(`✅ FOUND via profile image: @${profile.username} - ${element.alt}`);
                    break;
                }
            }
        }
        
        if (found) {
            matches.push(profile);
            log(`MATCH: @${profile.username} (score: ${profile.score})`);
        } else {
            log(`NO MATCH: @${profile.username} - Não encontrado após ${maxAttempts} tentativas`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Resultados
    log(`\nTotal de matches: ${matches.length}`);
    
    if (matches.length > 0) {
        // Contar distribuição por categoria
        const counts = {
            extremaEsquerda: matches.filter(m => m.score === -2).length,
            esquerda: matches.filter(m => m.score === -1).length,
            centro: matches.filter(m => m.score === 0).length,
            direita: matches.filter(m => m.score === 1).length,
            extremaDireita: matches.filter(m => m.score === 2).length
        };
        
        // Calcular score ponderado pela distribuição
        const totalEsquerda = counts.extremaEsquerda + counts.esquerda;
        const totalDireita = counts.direita + counts.extremaDireita;
        const totalCentro = counts.centro;
        
        let classification;
        let finalScore;
        
        // Se há predominância clara de um lado
        if (totalDireita >= totalEsquerda + totalCentro) {
            // Mais direita que esquerda+centro
            if (counts.extremaDireita > counts.direita) {
                classification = 'Extrema Direita';
                finalScore = 2.0;
            } else {
                classification = 'Direita';
                finalScore = 1.5;
            }
        } else if (totalEsquerda >= totalDireita + totalCentro) {
            // Mais esquerda que direita+centro
            if (counts.extremaEsquerda > counts.esquerda) {
                classification = 'Extrema Esquerda';
                finalScore = -2.0;
            } else {
                classification = 'Esquerda';
                finalScore = -1.5;
            }
        } else {
            // Usar média tradicional para casos balanceados
            // Usar média tradicional para casos balanceados
            finalScore = matches.reduce((sum, m) => sum + m.score, 0) / matches.length;
            if (finalScore <= -1.5) classification = 'Extrema Esquerda';
            else if (finalScore <= -0.5) classification = 'Esquerda';
            else if (finalScore <= 0.5) classification = 'Centro';
            else if (finalScore <= 1.5) classification = 'Direita';
            else classification = 'Extrema Direita';
        }
        
        alert(`Viés Político\nAnálise de @${profileName}:\n\nSeguindo (${matches.length}/100):\n${matches.map(m => `• @${m.username}`).join('\n')}\n\nDistribuição:\n• Extrema Direita: ${counts.extremaDireita}\n• Direita: ${counts.direita}\n• Centro: ${counts.centro}\n• Esquerda: ${counts.esquerda}\n• Extrema Esquerda: ${counts.extremaEsquerda}\n\nResultado:\nInclinação: ${classification}\n\nVersão: 1.4.5`);
        
    } else {
        alert(`Viés Político\nAnálise de @${profileName}:\n\nSeguindo (0/100):\nNenhum político encontrado\n\nResultado:\nPerfil apolítico ou privado`);
    }
    
    // Restaurar botão
    const btn = document.getElementById('viespolitico-btn');
    if (btn) btn.textContent = 'Analisar Perfil';
}

// Disponibilizar função globalmente
window.analisarPerfil = analisarPerfil;

// Adicionar botão na página
function adicionarBotao() {
    if (document.getElementById('viespolitico-btn')) return;
    
    const btn = document.createElement('button');
    btn.id = 'viespolitico-btn';
    btn.textContent = 'Analisar Perfil';
    btn.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
        background: #007acc;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    `;
    btn.onclick = analisarPerfil;
    
    // Adicionar botão de configurações
    const configBtn = document.createElement('button');
    configBtn.textContent = '⚙️';
    configBtn.style.cssText = `
        position: fixed;
        top: 55px;
        right: 10px;
        z-index: 9999;
        background: #6c757d;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        width: 40px;
    `;
    configBtn.onclick = () => {
        // Enviar mensagem para background script abrir opções
        if (typeof browser !== 'undefined' && browser.runtime) {
            browser.runtime.sendMessage({ action: 'openOptions' });
        } else if (typeof chrome !== 'undefined' && chrome.runtime) {
            chrome.runtime.sendMessage({ action: 'openOptions' });
        }
    };
    configBtn.title = 'Configurar ViésPolítico';
    
    document.body.appendChild(btn);
    document.body.appendChild(configBtn);
    
    // Adicionar tooltip detalhado ao botão principal
    btn.title = 'Clique para iniciar a automação que identifica o viés político. Não feche a aba do navegador. Você pode usar outra janela. Caso queira usar outra aba de navegador, ANTES, arraste esta aba para fora do navegador, separando em duas janelas. Assim a análise funcionará sem problemas.';
}

// Carregar perfis e adicionar botão
carregarPerfis().then(() => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', adicionarBotao);
    } else {
        adicionarBotao();
    }
});
