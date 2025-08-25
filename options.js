// ViesPolítico - Options Script
let profiles = [];
let defaultProfiles = [];

// Carregar perfis padrão
async function loadDefaultProfiles() {
    try {
        const response = await fetch(browser.runtime.getURL('seed_profiles.json'));
        defaultProfiles = await response.json();
        return defaultProfiles;
    } catch (error) {
        console.error('Erro ao carregar perfis padrão:', error);
        return [];
    }
}

// Carregar perfis customizados ou padrão
async function loadProfiles() {
    try {
        const result = await browser.storage.local.get('customProfiles');
        if (result.customProfiles && result.customProfiles.length > 0) {
            profiles = result.customProfiles;
        } else {
            profiles = await loadDefaultProfiles();
        }
        updateUI();
    } catch (error) {
        console.error('Erro ao carregar perfis:', error);
        showMessage('Erro ao carregar perfis', 'error');
    }
}

// Salvar perfis customizados
async function saveProfiles() {
    try {
        await browser.storage.local.set({ customProfiles: profiles });
        showMessage('Perfis salvos com sucesso!', 'success');
        updateUI();
    } catch (error) {
        console.error('Erro ao salvar perfis:', error);
        showMessage('Erro ao salvar perfis', 'error');
    }
}

// Atualizar interface
function updateUI() {
    updateStats();
    renderProfileList();
}

// Atualizar estatísticas
function updateStats() {
    const politicians = profiles.filter(p => p.type === 'politico').length;
    const media = profiles.filter(p => p.type === 'veiculo').length;
    
    document.getElementById('totalProfiles').textContent = profiles.length;
    document.getElementById('politicianCount').textContent = politicians;
    document.getElementById('mediaCount').textContent = media;
}

// Renderizar lista de perfis
function renderProfileList() {
    const container = document.getElementById('profileList');
    const filter = document.getElementById('filterCategory').value;
    
    let filteredProfiles = profiles;
    if (filter) {
        filteredProfiles = profiles.filter(p => p.category === filter);
    }
    
    container.innerHTML = '';
    
    filteredProfiles.forEach((profile, index) => {
        const item = document.createElement('div');
        item.className = 'profile-item';
        
        const categoryColor = getCategoryColor(profile.category);
        
        item.innerHTML = `
            <div class="profile-info">
                <strong>@${profile.username}</strong>
                <span style="color: ${categoryColor}; margin-left: 10px;">
                    ${profile.category} (${profile.score > 0 ? '+' : ''}${profile.score})
                </span>
                <span style="color: #666; margin-left: 10px;">[${profile.type}]</span>
            </div>
            <div class="profile-actions">
                <button onclick="editProfile(${index})">✏️</button>
                <button onclick="removeProfile(${index})" class="danger">🗑️</button>
            </div>
        `;
        
        container.appendChild(item);
    });
}

// Obter cor da categoria
function getCategoryColor(category) {
    const colors = {
        'Extrema Direita': '#dc3545',
        'Direita': '#fd7e14',
        'Centro': '#6c757d',
        'Esquerda': '#20c997',
        'Extrema Esquerda': '#198754'
    };
    return colors[category] || '#6c757d';
}

// Adicionar perfil
function addProfile() {
    const username = document.getElementById('newUsername').value.trim();
    const score = parseInt(document.getElementById('newScore').value);
    const type = document.getElementById('newType').value;
    
    if (!username) {
        showMessage('Username é obrigatório', 'error');
        return;
    }
    
    // Verificar se já existe
    if (profiles.find(p => p.username.toLowerCase() === username.toLowerCase())) {
        showMessage('Perfil já existe na lista', 'error');
        return;
    }
    
    const category = getCategory(score);
    
    const newProfile = {
        username: username,
        score: score,
        category: category,
        type: type
    };
    
    profiles.push(newProfile);
    saveProfiles();
    
    // Limpar formulário
    document.getElementById('newUsername').value = '';
    document.getElementById('newScore').value = '0';
    document.getElementById('newType').value = 'politico';
    
    showMessage(`Perfil @${username} adicionado com sucesso!`, 'success');
}

// Obter categoria pelo score
function getCategory(score) {
    const categories = {
        2: 'Extrema Direita',
        1: 'Direita',
        0: 'Centro',
        '-1': 'Esquerda',
        '-2': 'Extrema Esquerda'
    };
    return categories[score.toString()] || 'Centro';
}

// Editar perfil
function editProfile(index) {
    const profile = profiles[index];
    const newUsername = prompt('Username:', profile.username);
    
    if (newUsername === null) return; // Cancelado
    
    if (!newUsername.trim()) {
        showMessage('Username não pode estar vazio', 'error');
        return;
    }
    
    // Verificar duplicata (exceto o próprio)
    const existing = profiles.find((p, i) => i !== index && p.username.toLowerCase() === newUsername.toLowerCase());
    if (existing) {
        showMessage('Username já existe', 'error');
        return;
    }
    
    const newScore = prompt('Score (-2 a +2):', profile.score);
    if (newScore === null) return;
    
    const scoreNum = parseInt(newScore);
    if (isNaN(scoreNum) || scoreNum < -2 || scoreNum > 2) {
        showMessage('Score deve ser entre -2 e +2', 'error');
        return;
    }
    
    profiles[index].username = newUsername.trim();
    profiles[index].score = scoreNum;
    profiles[index].category = getCategory(scoreNum);
    
    saveProfiles();
    showMessage('Perfil atualizado com sucesso!', 'success');
}

// Remover perfil
function removeProfile(index) {
    const profile = profiles[index];
    if (confirm(`Remover @${profile.username}?`)) {
        profiles.splice(index, 1);
        saveProfiles();
        showMessage('Perfil removido com sucesso!', 'success');
    }
}

// Filtrar perfis
function filterProfiles() {
    renderProfileList();
}

// Exportar perfis
function exportProfiles() {
    const dataStr = JSON.stringify(profiles, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'viespolitico-profiles.json';
    link.click();
    
    showMessage('Lista exportada com sucesso!', 'success');
}

// Importar perfis
function importProfiles(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const importedProfiles = JSON.parse(e.target.result);
            
            // Validar formato
            if (!Array.isArray(importedProfiles)) {
                throw new Error('Formato inválido');
            }
            
            // Validar cada perfil
            for (const profile of importedProfiles) {
                if (!profile.username || typeof profile.score !== 'number' || !profile.category || !profile.type) {
                    throw new Error('Perfil com formato inválido encontrado');
                }
            }
            
            profiles = importedProfiles;
            saveProfiles();
            showMessage(`${profiles.length} perfis importados com sucesso!`, 'success');
            
        } catch (error) {
            console.error('Erro ao importar:', error);
            showMessage('Erro ao importar arquivo. Verifique o formato.', 'error');
        }
    };
    
    reader.readAsText(file);
    event.target.value = ''; // Limpar input
}

// Resetar para padrão
async function resetToDefault() {
    if (confirm('Isso irá remover todas as customizações e voltar para a lista padrão. Continuar?')) {
        try {
            await browser.storage.local.remove('customProfiles');
            profiles = await loadDefaultProfiles();
            updateUI();
            showMessage('Lista resetada para o padrão!', 'success');
        } catch (error) {
            console.error('Erro ao resetar:', error);
            showMessage('Erro ao resetar lista', 'error');
        }
    }
}

// Mostrar mensagem
function showMessage(text, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', loadProfiles);
