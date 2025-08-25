/*
 * ViésPolítico - Background Script
 * Desenvolvido por @cyberjulio
 * GitHub: https://github.com/cyberjulio
 * 
 * Licença: CC BY-NC-SA 4.0 (Não Comercial)
 */

// Background script para ViesPolítico
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'openOptions') {
        browser.runtime.openOptionsPage();
    }
});
