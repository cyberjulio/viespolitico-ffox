// Simulações do algoritmo de classificação política

function testAlgorithm(matches, testName) {
    console.log(`\n=== ${testName} ===`);
    
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
        finalScore = matches.reduce((sum, m) => sum + m.score, 0) / matches.length;
        if (finalScore <= -1.5) classification = 'Extrema Esquerda';
        else if (finalScore <= -0.5) classification = 'Esquerda';
        else if (finalScore <= 0.5) classification = 'Centro';
        else if (finalScore <= 1.5) classification = 'Direita';
        else classification = 'Extrema Direita';
    }
    
    console.log(`Perfis seguidos: ${matches.length}`);
    console.log(`Distribuição:`);
    console.log(`• Extrema Direita: ${counts.extremaDireita}`);
    console.log(`• Direita: ${counts.direita}`);
    console.log(`• Centro: ${counts.centro}`);
    console.log(`• Esquerda: ${counts.esquerda}`);
    console.log(`• Extrema Esquerda: ${counts.extremaEsquerda}`);
    console.log(`Totais: Direita=${totalDireita}, Esquerda=${totalEsquerda}, Centro=${totalCentro}`);
    console.log(`Resultado: ${classification}`);
    
    return classification;
}

// Simulação 1: Perfil claramente de extrema direita
const sim1 = [
    {score: 2}, {score: 2}, {score: 2}, {score: 2}, {score: 2}, // 5 extrema direita
    {score: 1}, {score: 1}, // 2 direita
    {score: 0}, {score: 0}, // 2 centro
    {score: -1} // 1 esquerda
];

// Simulação 2: Perfil claramente de extrema esquerda
const sim2 = [
    {score: -2}, {score: -2}, {score: -2}, {score: -2}, // 4 extrema esquerda
    {score: -1}, {score: -1}, {score: -1}, // 3 esquerda
    {score: 0}, {score: 0}, // 2 centro
    {score: 1} // 1 direita
];

// Simulação 3: Perfil balanceado (deve usar média)
const sim3 = [
    {score: 2}, {score: 2}, // 2 extrema direita
    {score: 1}, {score: 1}, // 2 direita
    {score: 0}, {score: 0}, {score: 0}, // 3 centro
    {score: -1}, {score: -1}, // 2 esquerda
    {score: -2} // 1 extrema esquerda
];

// Simulação 4: Perfil direita moderada
const sim4 = [
    {score: 1}, {score: 1}, {score: 1}, {score: 1}, {score: 1}, // 5 direita
    {score: 2}, {score: 2}, // 2 extrema direita
    {score: 0}, {score: 0}, // 2 centro
    {score: -1} // 1 esquerda
];

// Simulação 5: Perfil esquerda moderada
const sim5 = [
    {score: -1}, {score: -1}, {score: -1}, {score: -1}, // 4 esquerda
    {score: -2}, {score: -2}, // 2 extrema esquerda
    {score: 0}, {score: 0}, {score: 0}, // 3 centro
    {score: 1} // 1 direita
];

// Executar testes
testAlgorithm(sim1, "Simulação 1: Extrema Direita Dominante");
testAlgorithm(sim2, "Simulação 2: Extrema Esquerda Dominante");
testAlgorithm(sim3, "Simulação 3: Perfil Balanceado");
testAlgorithm(sim4, "Simulação 4: Direita Moderada");
testAlgorithm(sim5, "Simulação 5: Esquerda Moderada");

console.log("\n=== RESUMO DOS TESTES ===");
console.log("Sim1: Extrema Direita (5+2=7 direita vs 2+1=3 outros, 5>2 extrema)");
console.log("Sim2: Extrema Esquerda (4+3=7 esquerda vs 2+1=3 outros, 4>3 extrema)");
console.log("Sim3: Balanceado (4 direita vs 5 esquerda+centro, usa média)");
console.log("Sim4: Direita (7 direita vs 3 outros, 5>2 moderada)");
console.log("Sim5: Esquerda (6 esquerda vs 4 outros, 4>2 moderada)");
