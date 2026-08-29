let products = [
    {
        id: 101,
        name: "موبایل",
        price: 25000000,
        stock: 10,
        image: "img/1.png",
        isnew: false,
        isoffer: true,
        description: `
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
`    },

    {
        id: 102,
        name: "لپ تاپ",
        price: 45000000,
        stock: 10,
        image: "img/2.jpg",
        isnew: false,
        description: `
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
`

    },
    {
        id: 103,
        name: "هدفون",
        price: 3500000,
        stock: 15,
        image: "img/3.jpg",
        isnew: true,
        isoffer: false,
        description: `
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
`


    },
    {
        id: 104,
        name: "تلویزیون ال سی دی",
        price: 8500000,
        stock: 10,
        image: "img/4.jpg",
        isnew: false,
        isoffer: true,
        description: `
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
`
    },
    {
        id: 105,
        name: " تلویزیون منحنی ال ای دی 52 اینچ ال جی پلاس تلویزیون ال ای دی سامسونگ منحنی",
        price: 75000000,
        stock: 8,
        image: "img/5.jpg",
        isnew: true,
        isoffer: true,
        description: `
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
`
    }
];

let cart = [];


function savecart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}


function loadcart() {
    let savecart = localStorage.getItem("cart");
    if (savecart != null) {
        cart = JSON.parse(savecart);
    }
}


// این تابع برای بررسی موجودی از تابع اصلی می باشد متغیر اول محصول موردنظر است که در برنامه با تابع فایند از آزایه اصلی پیدا کرده ایم و پارامتر دوم تعداد درخواستی مشتری که در سبد خرید به دست آورده ایم

function checkstock(product, requestcount) {
    return product.stock >= requestcount
}



function saveproducts() {
    localStorage.setItem("products", JSON.stringify(products));
}



function loadproducts() {
    let saveproduct = localStorage.getItem("products");
    if (saveproduct != null) {
        products = JSON.parse(saveproduct);
    }
}


