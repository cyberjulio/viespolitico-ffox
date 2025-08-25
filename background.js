// Background script para ViesPolítico
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'openOptions') {
        browser.runtime.openOptionsPage();
    }
});
