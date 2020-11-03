var items = [];
//console.log('in js file');
function handleaddcart (name, price, id){
    items.push([name, price]);
//    var element = $("#addcart"+id);
//    element.setAttribute("style", "display: none;");
    console.log(' bfore');
    console.log("#addcart"+id);
    console.log('abc');
    document.getElementById("addcart"+id).style.display = "none";
    sessionStorage.setItem('items', items);
    console.log('in handle add cart');
    console.log(items);
}
