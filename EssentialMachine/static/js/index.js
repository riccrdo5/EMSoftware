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
function handleaddcart(name,price,id){
document.getElementById("addcart"+id).style.display = "none";
document.getElementById("quant"+id).style.display = "inline-block";
document.getElementById("inc"+id).style.display = "inline-block";
document.getElementById("dec"+id).style.display = "inline-block";
document.getElementById("rem"+id).style.display = "inline-block";
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
cell2.innerHTML = price;
cell3.innerHTML = document.getElementById("quant"+id).value;
var x = document.getElementById("quant"+id).value;
cell4.innerHTML = price * x;
}

function increment(id,price){
document.getElementById("quant"+id).stepUp();
var x = document.getElementById("quant"+id).value;
document.getElementById("cart-item-qty-"+id).innerHTML= x;
document.getElementById("cart-item-total-"+id).innerHTML = x * price
}


function decrement(id,price){
document.getElementById("quant"+id).stepDown();
var x = document.getElementById("quant"+id).value;
document.getElementById("cart-item-qty-"+id).innerHTML= x;
document.getElementById("cart-item-total-"+id).innerHTML = x * price
}

function removebutton(id)
{
document.getElementById("addcart"+id).style.display = "inline-block";
document.getElementById("quant"+id).style.display = "none";
document.getElementById("inc"+id).style.display = " none";
document.getElementById("dec"+id).style.display = "none";
document.getElementById("rem"+id).style.display = "none";
var row = document.getElementById('cart-item-'+id);
row.parentNode.removeChild(row);
}