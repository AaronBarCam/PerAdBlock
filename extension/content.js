function limpiarPantalla() {
    const adSelectors = ['ins', 'iframe[src*="ads"]', '.ad-unit', '[id*="google_ads"]', '.ad-container'];
    adSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.display = 'none';
        });
    });
}
setInterval(limpiarPantalla, 1000);