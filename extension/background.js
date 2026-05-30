chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
        const url = details.url;
        // Filtros básicos para no colapsar el servidor
        if (url.includes("localhost") || url.startsWith("chrome") || url.includes("favicon")) return;

        fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_ad) {
                chrome.storage.local.get(['blockedCount'], (result) => {
                    let total = (result.blockedCount || 0) + 1;
                    chrome.storage.local.set({ blockedCount: total });
                    console.log(`[PerAdBlock] Bloqueo #${total}: ${url}`);
                });
            }
        })
        .catch(() => { /* Silenciar errores de conexión */ });
    },
    { urls: ["<all_urls>"] }
);