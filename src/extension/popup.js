// ViésPolítico - Script do Popup
// Desenvolvido por @cyberjulio

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('analisar-btn');
    
    button.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.executeScript(tabs[0].id, {
                code: 'if (typeof analisarPerfil === "function") analisarPerfil(); else alert("Vá para um perfil do Instagram primeiro!");'
            });
        });
    });
});
