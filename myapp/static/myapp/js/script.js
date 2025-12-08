console.log("ORDER JS LOADED");

// --- Real-time action handler ---
function handleAction(url, method = 'POST', data = {}) {
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                createPopup(data.message, data.status || 'success');
            }
            if (data.reload) {
                window.location.reload(); // optional
            }
        })
        .catch(err => {
            createPopup("Something went wrong", "error");
            console.error(err);
        });
}

// Helper to get CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// --- DOMContentLoaded for page setup ---
document.addEventListener("DOMContentLoaded", () => {

    // Show Django messages from page load
    if (window.DJANGO_MESSAGES) {
        window.DJANGO_MESSAGES.forEach(msg => {
            createPopup(msg.text, 'popup');
        });
    }

    // Show cart messages from session
    if (window.CART_MESSAGE) {
        createPopup(window.CART_MESSAGE, 'popup');
    }

    // Pizza order price calculation
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

    if (sizeSelect) {
        sizeSelect.addEventListener("change", calculateTotal);
    }
    toppingCheckboxes.forEach(t => t.addEventListener("change", calculateTotal));

    calculateTotal();
});
