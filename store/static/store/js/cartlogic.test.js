import { describe, test, expect } from "vitest";
import { totalproduct, totalpricecart, totalcounter } from "./cartlogic.js";

describe("totalproduct", () => {

    test("محاسبه قیمت کل یک محصول", () => {

        const product = {
            price: 100,
            count: 3
        };

        const result = totalproduct(product);

        expect(result).toBe(300);
    });



test("محاسبه مجموع قیمت سبد خرید", () => {

    const cart = [
        {
            price: 100,
            count: 2
        },
        {
            price: 50,
            count: 3
        }
    ];

    const result = totalpricecart(cart);

    expect(result).toBe(350);
   });



test("محاسبه مجموع قیمت سبد خرید خالی", () => {

    const cart = [ ];

    const result = totalpricecart(cart);

    expect(result).toBe(0);
   });


test("محاسبه مجموع اقلام سبد خرید", () => {

    const cart = [
        {
            price: 100,
            count: 2
        },
        {
            price: 50,
            count: 3
        }
    ];

    const result = totalcounter(cart);

    expect(result).toBe(5);
   });


test("محاسبه مجموع اقلام سبد خرید خالی", () => {

    const cart = [ ];

    const result = totalcounter(cart);

    expect(result).toBe(0);
   });



});