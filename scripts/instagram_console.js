// ViesPolítico - Script para Console do Navegador
// 1. Abra Instagram e faça login
// 2. Vá para o perfil alvo (ex: instagram.com/barbarastudart)
// 3. Clique em "seguindo" para abrir o modal
// 4. Cole este script no console (F12 > Console)

async function analisarViespolitico() {
    console.log('🎯 ViesPolítico - Iniciando análise...');
    
    // Perfis semente (primeiros 20 para teste)
    const seedProfiles = [
        {username: 'jairmessiasbolsonaro', score: 2, category: 'Extrema Direita'},
        {username: 'nikolas_dm', score: 2, category: 'Extrema Direita'},
        {username: 'eduardobolsonaro', score: 2, category: 'Extrema Direita'},
        {username: 'carlosjordy', score: 2, category: 'Extrema Direita'},
        {username: 'marcelofreixo', score: -1, category: 'Esquerda'},
        {username: 'lula', score: -1, category: 'Esquerda'},
        {username: 'guilhermeboulos', score: -1, category: 'Esquerda'},
        {username: 'fernandohaddad_', score: -1, category: 'Esquerda'},
        {username: 'tarcisiogdf', score: 1, category: 'Direita'},
        {username: 'sergio_moro', score: 1, category: 'Direita'},
        {username: 'romeuzema', score: 1, category: 'Direita'},
        {username: 'simonetebet', score: 0, category: 'Centro'},
        {username: 'marinasilva.oficial', score: 0, category: 'Centro'},
        {username: 'lucianohuck', score: 0, category: 'Centro'},
        {username: 'cironogueira', score: 1, category: 'Direita'},
        {username: 'arthurliraneto', score: 1, category: 'Direita'},
        {username: 'rodrigopachieco', score: 0, category: 'Centro'},
        {username: 'gleisi.hoffmann', score: -1, category: 'Esquerda'},
        {username: 'randolfeap', score: -1, category: 'Esquerda'},
        {username: 'flaviobolsonaro', score: 2, category: 'Extrema Direita'}
    ];
    
    // Encontrar caixa de pesquisa
    const searchSelectors = [
        'input[placeholder*="Search"]',
        'input[placeholder*="Pesquisar"]',
        'input[placeholder*="search"]',
        'input[placeholder*="pesquisar"]',
        'input[type="text"]'
    ];
    
    let searchBox = null;
    for (let selector of searchSelectors) {
        searchBox = document.querySelector(selector);
        if (searchBox && searchBox.offsetParent !== null) {
            console.log('✅ Caixa de pesquisa encontrada:', selector);
            break;
        }
    }
    
    if (!searchBox) {
        console.error('❌ Caixa de pesquisa não encontrada. Certifique-se que o modal de seguidos está aberto.');
        return;
    }
    
    const matches = [];
    console.log(`🔍 Testando ${seedProfiles.length} perfis...`);
    
    for (let i = 0; i < seedProfiles.length; i++) {
        const profile = seedProfiles[i];
        const username = profile.username;
        
        console.log(`[${i+1}/${seedProfiles.length}] Testando @${username}...`);
        
        try {
            // Limpar e digitar
            searchBox.value = '';
            searchBox.focus();
            
            // Simular digitação
            for (let char of username) {
                searchBox.value += char;
                searchBox.dispatchEvent(new Event('input', { bubbles: true }));
                await new Promise(resolve => setTimeout(resolve, 30));
            }
            
            // Aguardar resultados
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Verificar se aparece nos resultados
            const resultSelectors = [
                `a[href*="/${username}/"]`,
                `a[href*="${username}"]`,
                `*[href*="${username}"]`
            ];
            
            let found = false;
            for (let selector of resultSelectors) {
                const elements = document.querySelectorAll(selector);
                for (let element of elements) {
                    if (element.href && 
                        element.href.includes(username) && 
                        element.offsetParent !== null) {
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
            
            if (found) {
                matches.push(profile);
                console.log(`✅ MATCH: @${username} (score: ${profile.score})`);
            }
            
            // Delay entre buscas
            await new Promise(resolve => setTimeout(resolve, 200));
            
        } catch (e) {
            console.warn(`⚠️ Erro ao testar @${username}:`, e);
        }
    }
    
    // Resultados finais
    console.log('\n' + '='.repeat(50));
    console.log('🎯 RESULTADOS FINAIS:');
    console.log('='.repeat(50));
    
    if (matches.length === 0) {
        console.log('❌ Nenhum match encontrado');
        console.log('💡 Possíveis causas:');
        console.log('   • Perfil não segue políticos da base');
        console.log('   • Perfil privado');
        console.log('   • Modal não está aberto corretamente');
        return;
    }
    
    console.log(`📊 Total de matches: ${matches.length}`);
    console.log('\n📋 Matches encontrados:');
    
    matches.forEach(match => {
        console.log(`   @${match.username} - Score: ${match.score} (${match.category})`);
    });
    
    const finalScore = matches.reduce((sum, match) => sum + match.score, 0) / matches.length;
    console.log(`\n🎯 Score final: ${finalScore.toFixed(2)}`);
    
    // Classificação
    let classification;
    if (finalScore <= -1.5) classification = 'Extrema Esquerda';
    else if (finalScore <= -0.5) classification = 'Esquerda';
    else if (finalScore <= 0.5) classification = 'Centro';
    else if (finalScore <= 1.5) classification = 'Direita';
    else classification = 'Extrema Direita';
    
    console.log(`🏷️ Classificação: ${classification}`);
    console.log('='.repeat(50));
    
    return {
        matches: matches,
        finalScore: finalScore,
        classification: classification,
        totalMatches: matches.length
    };
}

// Executar análise
console.log('🚀 Para iniciar a análise, execute: analisarViespolitico()');
console.log('📋 Certifique-se que:');
console.log('   1. Está logado no Instagram');
console.log('   2. Está no perfil alvo');
console.log('   3. Modal de "seguindo" está aberto');
console.log('   4. Digite: analisarViespolitico()');
