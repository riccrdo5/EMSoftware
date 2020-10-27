if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    checkScreenSize();
    var removeCartItemButtons = document.getElementsByClassName('btn-danger')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i];
        button.addEventListener('click', removeCartItem)
    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i];
        checkMinusButonDisabledState(input);
        input.addEventListener('change', quantityChanged)
    }

    var minusCartItemsButtons  = document.getElementsByClassName('btn-minus');
    for (var i = 0 ; i< minusCartItemsButtons.length; i++) {
        var button = minusCartItemsButtons[i];    
        button.addEventListener('click',decreaseQuantity);
    }

    var addCartItemsButtons  = document.getElementsByClassName('btn-add');
    for (var i = 0 ; i< addCartItemsButtons.length; i++) {
        var button = addCartItemsButtons[i];    
        button.addEventListener('click',increaseQuantity);
    }

    document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked)
}

function purchaseClicked() {
    alert('Thank you for your purchase')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    while (cartItems.hasChildNodes()) {
        cartItems.removeChild(cartItems.firstChild)
    }
    updateCartTotal()
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}

function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function checkScreenSize() {
    var element = document.getElementById('desktopView');
    if (window.getComputedStyle(element).display === "none") {
        element.remove();
    }
    updateCartTotal();
}

function checkMinusButonDisabledState(input) {
    if(input.value <= 1) {
        var minusBtn = input.parentElement.getElementsByClassName('btn-minus')[0];
        minusBtn.disabled = true;
    }
}


function decreaseQuantity(event) {
    var buttonClicked = event.target;
    var parentDiv = buttonClicked.parentElement.parentElement;
    parentDiv.getElementsByClassName('cart-quantity-input')[0].value = Number(parentDiv.getElementsByClassName('cart-quantity-input')[0].value) - 1;
    updateCartTotal();
    checkMinusButonDisabledState(parentDiv.getElementsByClassName('cart-quantity-input')[0]);
}


function increaseQuantity(event) {
    var buttonClicked = event.target;
    var parentDiv = buttonClicked.parentElement.parentElement;
    parentDiv.getElementsByClassName('cart-quantity-input')[0].value = Number(parentDiv.getElementsByClassName('cart-quantity-input')[0].value) + 1;
    updateCartTotal();
    if(Number(parentDiv.getElementsByClassName('cart-quantity-input')[0].value > 1)) {
        var minusBtn = parentDiv.getElementsByClassName('btn-minus')[0];
        if(minusBtn.disabled) {
            minusBtn.disabled = false;
        }
    }
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100;
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
    if(cartRows.length == 0){
        document.getElementById('empty').innerHTML = "Your Cart is Empty."
        document.getElementById('empty').setAttribute('class', 'empty')
        document.getElementById('total').remove()
        document.getElementById('pr-btn').remove()
        // document.getElementsByClassName('btn-purchase')[0].disabled = true
    }
}