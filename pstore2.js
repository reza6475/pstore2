
loadproducts();
const productgrid = document.querySelector(".product-grid");
for (let product of products) {
    let article = document.createElement("article");
    let imageproduct = document.createElement("img");
    imageproduct.src = product.image;
    article.appendChild(imageproduct);
    let h3 = document.createElement("h3");
    h3.textContent = product.name;
    article.appendChild(h3);
    let priceproduct = document.createElement("p");
    priceproduct.textContent = product.price.toLocaleString() + "    تومان";
    article.appendChild(priceproduct);
    let spanstock = document.createElement("span");
    spanstock.textContent = "موجودی" + product.stock;
    article.appendChild(spanstock);
    let buybutton = document.createElement("button");
    buybutton.textContent = "افزودن به سبد خرید";
    if(product.stock===0){
        buybutton.textContent="ناموجود";
        buybutton.disabled=true;
    }
    article.appendChild(buybutton);
    article.dataset.id = product.id;
    productgrid.appendChild(article);
}


productgrid.addEventListener("click", function (event) {
    if (event.target.matches("BUTTON")){
let article = event.target.closest("article");
    let product=products.find(item=>item.id===Number(article.dataset.id));
    let selectproduct=cart.find(productitem=>product.id===productitem.id);
    if(selectproduct){
        // ++selectproduct.count;
        window.location.href = "pstorecart2.html";
        // alert("در سبد خرید وجود دارد جهت افزایش به سبد خرید مراجعه نمایید");
        return;
    }
    let productcart={
        ...product,
        count:1
    }
    alert(product.name +"   به سبد خرید شما اضافه شد");
    cart.push(productcart);
    savecart();
    }
    
})