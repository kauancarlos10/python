(() => {
    const root = document.documentElement;
    const THEME_KEY = "organiza-theme";
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === "dark" || stored === "light") root.dataset.theme = stored;

    const themeButton = document.getElementById("themeToggle");
    const refreshThemeIcon = () => {
        if (!themeButton) return;
        const dark = root.dataset.theme === "dark";
        themeButton.innerHTML = dark ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon-stars"></i>';
        themeButton.title = dark ? "Usar tema claro" : "Usar tema escuro";
    };

    themeButton?.addEventListener("click", () => {
        const next = root.dataset.theme === "dark" ? "light" : "dark";
        root.dataset.theme = next;
        localStorage.setItem(THEME_KEY, next);
        refreshThemeIcon();
    });
    refreshThemeIcon();

    const mobileButton = document.getElementById("mobileMenu");
    mobileButton?.addEventListener("click", () => document.getElementById("sidebar")?.classList.toggle("open"));

    const quote = document.getElementById("fraseMotivacional");
    const quoteButton = document.getElementById("novaFrase");
    async function atualizarFrase() {
        if (!quote) return;
        quote.textContent = "Buscando uma ideia...";
        try {
            const response = await fetch("/api/frase");
            if (!response.ok) throw new Error("request");
            const data = await response.json();
            quote.textContent = `“${data.frase}”`;
        } catch {
            quote.textContent = "“Um passo de cada vez também é progresso.”";
        }
    }
    if (quoteButton) {
        quoteButton.addEventListener("click", atualizarFrase);
        atualizarFrase();
    }
})();
