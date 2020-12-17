$(document).ready(function(){
    console.log('Document ready')
    displayVenmoDropIn();
});

function displayVenmoDropIn(){
    var pur_button = document.querySelector('#purchase-button');
    var client_token = 'sandbox_ktffyjdn_vtj2pcb46ytpj78b';


  braintree.dropin.create({
    authorization: client_token,
    container: '#bt-dropin',
    venmo: {
      allowNewBrowserTab: true
    }
  }, function (createErr, instance) {
      pur_button.addEventListener('click', function(){
      instance.requestPaymentMethod(function (err, payload) {
        if (err) {
          console.log('Error', err);
          return;
        }

        // Add the nonce to the form and submit
        console.log('purchase clicked');
        var tbl_arr = $('#trycart').tableToJSON();
        var tbl_json = {nonce:payload.nonce, prods:tbl_arr};
        var json = JSON.stringify(tbl_json);
        $.ajax({
            type:"POST",
            url:"/purchase",
            contentType:"application/json; charset=utf-8",
            dataType:"json",
            data : json,
            headers : {
                payment_nonce:payload.nonce
            },
            success : function (data, status){
                var encoded = btoa(JSON.stringify(data.prods))
                var redirect_url = "/checkouts/" + data.transaction_id + '?data=' + encoded;
                window.location.replace(redirect_url);
            },
            error : function(response, status, error){
                console.log('error happened');
                window.location.replace("/fail");
            }
        });
      });
    });
  });
}



var cartshow = 0; //Variable to check if the cart contains items

function handleaddcart(name,price,id){
    cartshow = cartshow + 1;
    displaycart();
    document.getElementById("addcart"+id).style.display = "none"; //Hide the add to cart button
    //Displaying the quantity and remove buttons
    document.getElementById("quant"+id).style.display = "inline-block";
    document.getElementById("inc"+id).style.display = "inline-block";
    document.getElementById("dec"+id).style.display = "inline-block";
    document.getElementById("dec"+id).style.visibility = "hidden";
    document.getElementById("rem"+id).style.display = "inline-block";

    //Adds a row to cell and displays it

    var tbl = document.getElementById("trycart");
    var row = tbl.insertRow();
    var cell1 = row.insertCell();
    var cell2 = row.insertCell();
    cell2.id = "cart-price"+id;
    var cell3 = row.insertCell();
    cell3.id='cart-item-qty-'+id;
    var cell4 = row.insertCell();
    cell4.id = 'cart-item-total-'+id;
    row.id='cart-item-'+id;
    cell1.innerHTML = name;
    cell2.innerHTML = '$' + price;
    cell3.innerHTML = '1';
    document.getElementById("quant"+id).value = '1';
    cell4.innerHTML = '$' + price;
    updatecarttotal();
}

function increment(id,price,z){
    price.replace('$','')
    document.getElementById("quant"+id).stepUp(); //Increases the quantity
    var x = document.getElementById("quant"+id).value;
    document.getElementById("cart-item-qty-"+id).innerHTML= x;
    document.getElementById("cart-item-total-"+id).innerHTML = '$' + (x * price).toFixed(2); 

    //Decrement button is only visible if the increment button is clicked atleast once
    document.getElementById("dec"+id).style.visibility = "visible";

    //Increment button disappears when it reaches the max quantity obtained from the database
    if(x==z){
        document.getElementById("inc"+id).style.visibility="hidden"
    }
    updatecarttotal();
}

function decrement(id,price){
    incbutcheck(id);
    price.replace('$','')
    document.getElementById("quant"+id).stepDown(); //Decreases the quantity
    var x = document.getElementById("quant"+id).value;
    document.getElementById("cart-item-qty-"+id).innerHTML= x;
    document.getElementById("cart-item-total-"+id).innerHTML = '$' + (x * price).toFixed(2);

    //Decrement button disappears if the quantity come down to 1
    if(x==1){
        document.getElementById("dec"+id).style.visibility="hidden"
    }
    updatecarttotal();
}

function removebutton(id)
{
    document.getElementById("addcart"+id).style.display = "inline-block"; //Shows the add to cart button

    //Hides quantity and remove buttons
    document.getElementById("quant"+id).style.display = "none";
    document.getElementById("inc"+id).style.display = " none";
    document.getElementById("dec"+id).style.display = "none";
    document.getElementById("rem"+id).style.display = "none";

    //Removes the item from the cart table
    var row = document.getElementById('cart-item-'+id);
    row.parentNode.removeChild(row);
    updatecarttotal();
    cartshow = cartshow - 1;
    displaycart();
}
function updatecarttotal(){
    var table = document.getElementById("trycart"), sumVal = 0.0;
    for(var i = 1; i < table.rows.length; i++)
    {
        var price = table.rows[i].cells[3].innerHTML.replace('$','')
        sumVal = sumVal + parseFloat(price);
    }
    document.getElementById("val").innerHTML = "Total: $" + sumVal.toFixed(2);
}

function incbutcheck(id) {
    var z = document.getElementById("inc"+id);
    if (z.style.visibility === "hidden") {
      z.style.visibility = "visible";
    }
  }

function scrolltocart(){
    document.getElementById("scrollcart").scrollIntoView();
    window.location.hash = "scrollcart";
}
function displaycart(){

    //Cart and payment section will only be displayed only if cart contains atleast one item
    if(cartshow==0){
        document.getElementById("cartsection").style.display="none";
    }
    else{
        document.getElementById("cartsection").style.display="block";
        $('[data-braintree-id="choose-a-way-to-pay"]').hide();
    }
}
