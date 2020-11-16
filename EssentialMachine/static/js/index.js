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
        console.log();
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
totals=[]
function handleaddcart(name,price,id){
    document.getElementById("addcart"+id).style.display = "none";
    document.getElementById("quant"+id).style.display = "none";
    var tbl = document.getElementById("trycart");
    var row = tbl.insertRow();
    var cell1 = row.insertCell();
    var cell2 = row.insertCell();
    var cell3 = row.insertCell();
    var cell4 = row.insertCell();
    cell1.innerHTML = name;
    cell2.innerHTML = price;
    cell3.innerHTML = document.getElementById("quant"+id).value;
    var x = document.getElementById("quant"+id).value;
    var tot = price * x;
    totals.push(tot);
    cell4.innerHTML = tot;
    document.getElementById("inc"+id).style.display = "none";
    document.getElementById("dec"+id).style.display = "none";
}
function increment(id){
    document.getElementById("quant"+id).stepUp();
}
function decrement(id){
    document.getElementById("quant"+id).stepDown();
}
function calculateSum() {
    var sum = 0;
   for(i=0,i<totals.length(),i++){
        sum = sum+ totals[i]
   }
   $("#sum").html(sum.toFixed(2));
}

$("#trycart").on("keyup", function () {
    calculateSum();
});