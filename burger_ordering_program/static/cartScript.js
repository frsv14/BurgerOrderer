// Javascript for cart function
document.addEventListener('DOMContentLoaded', function() {
    const cartItems = [];
    const cartTotal = document.getElementById('cart-total');

    document.getElementById('add-to-cart').addEventListener('click', function() {
        const burgerSelect = document.getElementById('burger_id');
        const quantityInput = document.getElementById('quantity');
        const burger = burgerSelect.options[burgerSelect.selectedIndex].text;
        const price = parseFloat(burger.match(/- (\d+\.\d+) kr/)[1]);
        const quantity = parseInt(quantityInput.value);
        const total = price * quantity;
        
        cartItems.push({ burger: burger, quantity: quantity, total: total });
        updateCart();
    });

    function updateCart() {
        const cartList = document.getElementById('cart-items');
        cartList.innerHTML = '';

        let total = 0;
        cartItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.burger} x ${item.quantity} = ${item.total.toFixed(2)} kr`;
            cartList.appendChild(listItem);
            total += item.total;
        });

        cartTotal.textContent = `Total: ${total.toFixed(2)} kr`;
    }
});
