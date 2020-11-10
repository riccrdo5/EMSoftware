var items = [];
//console.log('in js file');
function handleaddcart (name, price, id){
    document.getElementById("addcart"+id).style.display = "none";
    var tb = document.getElementById("trycart");
    var row = tb.insertRow();
    var cell1 = row.insertCell();
    var cell2 = row.insertCell();
    var cell3 = row.insertCell();
    var cell4 = row.insertCell();
    cell1.innerHTML = name;
    cell2.innerHTML = price;
    cell3.innerHTML = 1;
    cell4.innerHTML = price;
}
