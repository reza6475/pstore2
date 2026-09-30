import {describe,test,expect,vi} from "vitest";
import {checkstock,getproducts} from "./pstoredata2.js";
describe("check stock",()=>{
    test("بررسی کافی بودن موجودی با تعداد درخواستی",()=>{
        const product={
            stock:20
        }
        const requestcount=2;
        const result=checkstock(product,requestcount);
        expect(result).toBe(true)
    });

    test("بررسی کافی نبودن موجودی با تعداد درخواستی",()=>{
        const product={
            stock:2
        }
        const requestcount=10;
        const result=checkstock(product,requestcount);
        expect(result).toBe(false)
    });


    test("بررسی صحیح بودن عملیاتfetch",async()=>{
        const mockfetch=vi.fn();
        const fakeresponse={
            json:  ()=>[
                {id:1, name:"موبایل"}
            ]
        };
        vi.stubGlobal("fetch",mockfetch);
        mockfetch.mockResolvedValue(fakeresponse);
        const result=await getproducts();
        expect(result).toEqual( [{id:1, name:"موبایل"}]);
        expect(mockfetch).toHaveBeenCalledWith("/api/products/");
});


});