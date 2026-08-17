loadproducts();
loadcart();
const cartitem = document.querySelector(".cartitem");
const registerbutton = document.querySelector(".registerorder");

if (cart.length === 0) {
    let emptymessage = document.createElement("p");
    emptymessage.textContent = "سبد خرید شما خالی است";
    cartitem.appendChild(emptymessage);
    registerbutton.disabled=true;
}
let totalcart = document.querySelector(".totalcart");
let totalcount = document.querySelector(".totalcount");
for (let product of cart) {
    let li = document.createElement("li");
    let imagecart = document.createElement("img");
    imagecart.src = product.image;
    li.appendChild(imagecart);
    let p = document.createElement("p");
    p.textContent = product.name;
    let increase = document.createElement("button");
    let price = document.createElement("p");
    price.textContent = "قیمت واحد:     " + product.price.toLocaleString() + "تومان   ";
    let totalprice = document.createElement("span");
    // totalprice.textContent = 0 + "تومان";
    totalprice.className = "spantotal";
    increase.textContent = "+";
    increase.className = "increase";
    let spancount = document.createElement("span");
    spancount.textContent = product.count;
    spancount.className = "spancount"
    let decrease = document.createElement("button");
    let divbutton = document.createElement("div");
    divbutton.className = "divbutton";
    decrease.textContent = "-";
    decrease.className = "decrease";
    let deletebutton = document.createElement("button");
    deletebutton.textContent = "🗑️";
    deletebutton.className = "delete";

    if (product.count === 1) {
        decrease.style.display = "none";
        deletebutton.style.display = "block";

    }
    else {
        decrease.style.display = "block";
        deletebutton.style.display = "none";
    }

    li.appendChild(p);
    li.appendChild(price);
    li.appendChild(totalprice);
    divbutton.appendChild(increase);
    divbutton.appendChild(spancount);
    divbutton.appendChild(decrease);
    divbutton.appendChild(deletebutton);
    li.appendChild(divbutton);
    li.dataset.id = product.id;
    cartitem.appendChild(li);
    showtotalproduct(li, product);
}
showtotalpricecart();

cartitem.addEventListener("click", function (event) {
    if (event.target.matches("BUTTON")) {
        let li = event.target.closest("li");
        if (event.target.classList.contains("increase")) {
            let product = cart.find(item => item.id === Number(li.dataset.id));
            let productstock = products.find(item => item.id === Number(li.dataset.id));
            // if (productstock.stock <= product.count) {
            //     alert("عدم موجودی");
            //     return;
            // }
            if (!checkstock(productstock, product.count + 1)) {
                alert("عدم موجودی");
                return;
            }
            ++product.count;
            savecart();
            showtotalproduct(li, product);
            showtotalpricecart();
            if (product.count > 1) {
                let deletebutton = li.querySelector(".delete");
                let decrease = li.querySelector(".decrease");
                decrease.style.display = "block";
                deletebutton.style.display = "none";
            }

            let spancount = li.querySelector(".spancount");
            spancount.textContent = product.count;
        }
        else if (event.target.classList.contains("decrease")) {
            let product = cart.find(item => item.id === Number(li.dataset.id))
            --product.count;
            savecart();
            showtotalproduct(li, product);
            showtotalpricecart();
            if (product.count === 1) {
                let deletebutton = li.querySelector(".delete");
                let decrease = li.querySelector(".decrease");
                decrease.style.display = "none";
                deletebutton.style.display = "block";
            }
            let spancount = li.querySelector(".spancount");
            spancount.textContent = product.count;
        }
        else if (event.target.classList.contains("delete")) {
            let index = cart.findIndex(item => item.id === Number(li.dataset.id));
            if (index != -1) {
                li.remove();
                cart.splice(index, 1);
                if (cart.length === 0) {
                    let emptymessage = document.createElement("p");
                    emptymessage.textContent = "سبد خرید شما خالی است";
                    cartitem.appendChild(emptymessage);
                    registerbutton.disabled = true;

                }
            }
            savecart();
            showtotalpricecart();

        }
    }
})

function totalproduct(product) {
    return product.price * product.count;
}


function showtotalproduct(li, product) {
    let total = totalproduct(product);
    let newspan = li.querySelector(".spantotal");
    newspan.textContent = total.toLocaleString() + "     تومان"
}




function totalpricecart() {
    let sum = 0;
    for (let item of cart) {
        sum += item.count * item.price;
    }
    return sum;
}


function showtotalpricecart() {
    let total = totalpricecart();
    let count = totalcounter();
    totalcart.textContent = "مجموع سبد خرید" + total.toLocaleString() + "   تومان";
    totalcount.textContent = "تعداد اقلام" + count;
}


function totalcounter() {
    let count = 0;
    for (let item of cart) {
        count += item.count
    }
    return count;
}



registerbutton.addEventListener("click", function () {
    if (cart.length === 0) {
        // alert("سبد خرید شما خالی است");
        registerbutton.disabled = true;
        return;
    }
    for (let item of cart) {
        let product = products.find(productitem => productitem.id === item.id);
        if (!product) {
            alert("محصول مورد نظر پیدا نشد");
            return;
        }
        if (product.stock < item.count) {
            alert("عدم موجودی");
            return;
        }
    }

    for (let item of cart) {
        let product = products.find(productitem => productitem.id === item.id);
        product.stock -= item.count;
    }
    saveproducts();
    cartitem.innerHTML = "";
    cart.length = 0;
    savecart();
    showtotalpricecart();
    alert("ثبت سفارش با موفقیت انجام شد");
    if (cart.length === 0) {
        let emptymessage = document.createElement("p");
        emptymessage.textContent = "سبد خرید شما خالی است";
        cartitem.appendChild(emptymessage);
        registerbutton.disabled = true;
    }

})
