(function () {
    const STORAGE_KEY = 'archive-accessibility-mode';
    const body = document.body;
    const buttons = [
        document.getElementById('accessibility-toggle'),
        ...document.querySelectorAll('[data-accessibility-toggle]')
    ].filter(Boolean);

    function setMode(enabled) {
        body.classList.toggle('accessibility-mode', enabled);
        buttons.forEach(button => button.setAttribute('aria-pressed', String(enabled)));
        localStorage.setItem(STORAGE_KEY, enabled ? '1' : '0');
    }

    setMode(localStorage.getItem(STORAGE_KEY) === '1');
    buttons.forEach(button => button.addEventListener('click', () => {
        setMode(!body.classList.contains('accessibility-mode'));
    }));
})();
