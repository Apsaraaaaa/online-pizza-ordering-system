console.log("ORDER JS LOADED");


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

document.addEventListener("DOMContentLoaded", () => {
    const sizeSelect = document.querySelector(".pizza-size");
    const toppingCheckboxes = document.querySelectorAll(".topping");

    const basePriceElement = document.getElementById("base-price");
    const toppingsPriceElement = document.getElementById("toppings-price");
    const totalPriceElement = document.getElementById("total-price");

    function calculateTotal() {
        let basePrice = 0;
        let toppingsPrice = 0;

       
        const selectedSize = sizeSelect.options[sizeSelect.selectedIndex];
        if (selectedSize && selectedSize.dataset.price) {
            basePrice = parseFloat(selectedSize.dataset.price);
        }

        toppingCheckboxes.forEach(t => {
            if (t.checked) {
                toppingsPrice += parseFloat(t.dataset.price);
            }
        });

        const total = basePrice + toppingsPrice;

       
        basePriceElement.textContent = `Rs${basePrice.toFixed(2)}`;
        toppingsPriceElement.textContent = `Rs${toppingsPrice.toFixed(2)}`;
        totalPriceElement.textContent = `Rs${total.toFixed(2)}`;
    }

    sizeSelect.addEventListener("change", calculateTotal);
    toppingCheckboxes.forEach(t => t.addEventListener("change", calculateTotal));

    calculateTotal(); 
});
