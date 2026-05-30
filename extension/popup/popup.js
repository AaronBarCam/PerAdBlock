// popup.js
const countDisplay = document.getElementById('count');

// 1. Cargar el número actual nada más abrir el popup
chrome.storage.local.get(['blockedCount'], (res) => {
    countDisplay.textContent = res.blockedCount || 0;
});

// 2. Escuchar si el background.js suma nuevos bloqueos mientras el popup está abierto
chrome.storage.onChanged.addListener((changes) => {
    if (changes.blockedCount) {
        countDisplay.textContent = changes.blockedCount.newValue;
    }
    
document.getElementById('reset').addEventListener('click', () => {
    chrome.storage.local.set({ blockedCount: 0 });
    countDisplay.textContent = 0;
});
});