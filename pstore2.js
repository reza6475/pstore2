
loadproducts();
loadcart();
const main = document.querySelector("main");
const allproduct = document.querySelector(".all-product");
const newproduct = document.querySelector(".new-product");
const offerproduct = document.querySelector(".offer-product");


for (let product of products) {
    let article = createProductCard(product);
    allproduct.appendChild(article);

    if (product.isnew) {
        let article = createProductCard(product);
        newproduct.appendChild(article);
    }

    if (product.isoffer) {
        let article = createProductCard(product);
        offerproduct.appendChild(article);
    }

}
main.addEventListener("click", function (event) {
    if (event.target.closest("BUTTON")) {
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








function createProductCard(product) {
    let article = document.createElement("article");
    article.className="product-card";
    let imageproduct = document.createElement("img");
    imageproduct.src = product.image;
    imageproduct.alt=product.name;
    let productlink = document.createElement("a");
    productlink.href = `product.html?id=${product.id}`;
    productlink.appendChild(imageproduct)
    article.appendChild(productlink);
    let h3 = document.createElement("h3");
    h3.textContent = product.name;
    let namelink=document.createElement("a");
    namelink.className="namelink";
    namelink.href=`product.html?id=${product.id}`;
    namelink.appendChild(h3);
    article.appendChild(namelink);
    let priceproduct = document.createElement("p");
    priceproduct.textContent = product.price.toLocaleString() + "    تومان";
    article.appendChild(priceproduct);
    let spanstock = document.createElement("span");
    spanstock.textContent = "موجودی" + product.stock;
    article.appendChild(spanstock);
    let buybutton = document.createElement("button");
    buybutton.textContent = "افزودن به سبد خرید";
    if (product.stock === 0) {
        buybutton.textContent = "ناموجود";
        buybutton.disabled = true;
    }
    article.appendChild(buybutton);
    article.dataset.id = product.id;
    return article;
}