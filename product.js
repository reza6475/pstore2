loadproducts();
loadcart();
const productdetail = document.querySelector(".product-detail");
const params = new URLSearchParams(window.location.search);
const productid = Number(params.get("id"));
let product = products.find(item => item.id === productid);
if (!product) {
    productdetail.textContent = "محصول پیدا نشد";
}
else {
    let article = document.createElement("article");
    article.className = "articlep";
    let imagebox = document.createElement("div");
    imagebox.className = "imageboxp";
    let imageproduct = document.createElement("img");
    imageproduct.src = product.image;
    imagebox.appendChild(imageproduct);
    article.appendChild(imagebox);
    let infobox = document.createElement("div");
    infobox.className = "infoboxp"
    let description = document.createElement("p");
    description.textContent = product.description;
    let h3 = document.createElement("h3");
    h3.textContent = product.name;
    infobox.appendChild(h3);
    infobox.appendChild(description);
    let priceproduct = document.createElement("p");
    priceproduct.textContent = product.price.toLocaleString() + "    تومان";
    infobox.appendChild(priceproduct);
    let spanstock = document.createElement("span");
    spanstock.textContent = "موجودی" + product.stock;
    infobox.appendChild(spanstock);
    let buybutton = document.createElement("button");
    buybutton.textContent = "افزودن به سبد خرید";
    if (product.stock === 0) {
        buybutton.textContent = "ناموجود";
        buybutton.disabled = true;
    }
    infobox.appendChild(buybutton);
    article.appendChild(infobox);
    article.dataset.id = product.id;
    productdetail.appendChild(article);

    productdetail.addEventListener("click", function (event) {
        if (event.target.matches("BUTTON")) {
            let article = event.target.closest("article");
            let product = products.find(item => item.id === Number(article.dataset.id));
            let selectproduct = cart.find(productitem => product.id === productitem.id);
            if (selectproduct) {
                // ++selectproduct.count;
                window.location.href = "pstorecart2.html";
                // alert("در سبد خرید وجود دارد جهت افزایش به سبد خرید مراجعه نمایید");
                return;
            }
            let productcart = {
                ...product,
                count: 1
            }
            alert(product.name + "   به سبد خرید شما اضافه شد");
            cart.push(productcart);
            savecart();
        }

    })
}








