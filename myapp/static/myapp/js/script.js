function addToCart(name) {
    console.log("Add to Cart Clicked:", name);
    createPopup(`${name} added to cart`);
}

function removeFromCart(name) {
    console.log("Remove from Cart Clicked:", name);
    createPopup(`${name} removed from cart`);
}

function createPopup(text) {
    console.log("Popup Triggered:", text);

    const container = document.getElementById("popup-container");
    if (!container) {
        console.log("Popup container NOT found");
        return;
    }

    const popup = document.createElement("div");
    popup.classList.add("popup");
    popup.innerText = text;

    container.appendChild(popup);

    setTimeout(() => {
        popup.classList.add("show");
    }, 50);

    setTimeout(() => {
        popup.classList.remove("show");
        setTimeout(() => popup.remove(), 500);
    }, 2500);
}
