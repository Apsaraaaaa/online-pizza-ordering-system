console.log("Pizza Ordering System Loaded");

function createPopup(text) {
    const container = document.getElementById('popup-container');
    if (!container) return;

    const popup = document.createElement('div');
    popup.classList.add('popup', 'success');
    popup.innerText = text;

    container.appendChild(popup);

    setTimeout(() => {
        popup.style.opacity = '1';
        popup.style.transform = 'translateX(0)';
    }, 50);

    setTimeout(() => {
        popup.style.opacity = '0';
        popup.style.transform = 'translateX(100%)';
        setTimeout(() => popup.remove(), 500);
    }, 3000);
}
