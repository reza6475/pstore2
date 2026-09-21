import {getproducts, cart, loadcart, savecart, checkstock} from "./pstoredata2.js";

const products = await getproducts();

// loadproducts();
loadcart();
const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;

const cartitem = document.querySelector(".cartitem");
const registerbutton = document.querySelector(".registerorder");

checkemptycart();
let totalcart = document.querySelector(".totalcart");
let totalcount = document.querySelector(".totalcount");

for (let product of cart) {
    let li = document.createElement("li");
    let imagebox = document.createElement("div");
    let imagecart = document.createElement("img");
    imagecart.src = product.image;
    imagebox.appendChild(imagecart);
    li.appendChild(imagebox);
    let infobox = document.createElement("div");
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

    } else {
        decrease.style.display = "block";
        deletebutton.style.display = "none";
    }

    infobox.appendChild(p);
    infobox.appendChild(price);
    infobox.appendChild(totalprice);
    divbutton.appendChild(increase);
    divbutton.appendChild(spancount);
    divbutton.appendChild(decrease);
    divbutton.appendChild(deletebutton);
    infobox.appendChild(divbutton);
    li.dataset.id = product.id;
    li.appendChild(infobox);
    cartitem.appendChild(li);
    imagebox.className = "imagebox";
    infobox.className = "infobox";
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
        } else if (event.target.classList.contains("decrease")) {
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
        } else if (event.target.classList.contains("delete")) {
            let index = cart.findIndex(item => item.id === Number(li.dataset.id));
            if (index != -1) {
                li.remove();
                cart.splice(index, 1);
            }
            savecart();
            showtotalpricecart();
            checkemptycart();

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


registerbutton.addEventListener("click", async function () {
    console.log("دکمه ثبت سفارش کلیک شد");
    const cartdata = cart.map(item => {
        return {
            product_id: item.id,
            quantity: item.count,
        };
    });

    try {
        const response = await fetch('/api/cart/', {
            method: "POST",
            headers: {
                "content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(cartdata)
        });
        const result = await response.json();
        if (response.status === 201) {
            console.log(result.message);
            cart.length = 0;
            localStorage.removeItem("cart");
            cartitem.innerHTML = "";
            checkemptycart();
            showtotalpricecart();
            alert("سفارش شما با شماره سفارش" + "     " + result.order_id + "با موفقیت ثبت گردید" + "   " + result.total_price.toLocaleString());
        } else {
            alert(result.message);
        }

    } catch (error) {
        // console.log("عدم ارتباط با سرور");
        console.error(error);
        alert("عدم ارتباط با سرور");

    }
});


    function checkemptycart() {
        if (cart.length === 0) {
            let li = document.createElement("li");
            li.className = "empty";
            let emptymessage = document.createElement("p");
            emptymessage.textContent = "سبد خرید شما خالی است";
            li.appendChild(emptymessage);
            let store = document.createElement("a");
            store.href = "/";
            store.textContent = "صفحه محصولات";
            li.appendChild(store);
            cartitem.appendChild(li);
            registerbutton.disabled = true;

        }
    }

