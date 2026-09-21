
 export function totalproduct(product) {
    return product.price * product.count;
}


 export function totalpricecart(cart) {
    let sum = 0;
    for (let item of cart) {
        sum += item.count * item.price;
    }
    return sum;
}


 export function totalcounter(cart) {
    let count = 0;
    for (let item of cart) {
        count += item.count
    }
    return count;
}