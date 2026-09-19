

// فراخوانی فایل جیسون از viewsوقتی می خواهیم در همین فایل از پایگاه داده استفاده نماییم
// fetch('/api/products/');
// .then(response=>response.json);
// .then(products=>{
//
// })

// در صورتی که بخواهیم از فایل json در فایل های دیگر استفاده نماییم
export async function getproducts(){
    const response=await fetch('/api/products/');
    return response.json();
}

 export let cart = [];






 export function savecart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}


export function loadcart() {
    let savecart = localStorage.getItem("cart");
    if (savecart != null) {
        cart = JSON.parse(savecart);
    }
}


// این تابع برای بررسی موجودی از تابع اصلی می باشد متغیر اول محصول موردنظر است که در برنامه با تابع فایند از آزایه اصلی پیدا کرده ایم و پارامتر دوم تعداد درخواستی مشتری که در سبد خرید به دست آورده ایم

 export function checkstock(product, requestcount) {
    return product.stock >= requestcount
}
