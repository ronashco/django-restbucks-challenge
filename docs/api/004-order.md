To submit order clients must have been added product(s) to their cart.

**Submit order/Orders list**
----
* **url** `/api/orders/` *
* **Methods**
    * **GET** List of submitted orders
    * **POST** Submit order.
* **Data Params (GET)**
    None
* **Data Params (POST)**
    * **location** `(optional)`. Choices are **i** (means In-Shop) and **a** (means Away). 
* **Success response‌ (GET)**
    * **Status code** 200 OK
    * **Content** Orders information. see following example:
```rest
[
    {
        "id": 1,
        "status": "w",
        "date": "25 Feb 2018-09:08",
        "location": "i",
        "total_price": 7,
        "url": "http://localhost:8000/api/orders/1/"
    },
    {
        "id": 2,
        "status": "w",
        "date": "25 Feb 2018-09:08",
        "location": "a",
        "total_price": 5,
        "url": "http://localhost:8000/api/orders/2/"
    },
    ...
]
```
* **Success response‌ (POST)**
    * **Status code** 201 CREATED
    * **Content**
 ```rest
{
    "id": 1,
    "status": "w",
    "date": "04 Mar 2018-12:44",
    "location": "i",
    "total_price": 7,
    "url": "http://localhost:8000/api/orders/1/"
}
```
* **Error response**
    (If the cart is empty):
    * **Status code** 400 BAD ‌REQUEST
    * **Content** `{
    "non_field_errors": ["Cart is empty."]}`

    OR (If location is invalid e.g. **w**):

    * **Status code** 400 BAD ‌REQUEST
    * **Content** `{"location": ["\"w\" is not a valid choice."]}`


**Single order api**
----
Clients can view order details, cancel and/or modify waiting orders.

* **url** `/api/orders/:order_id/` *
* **Methods**
    * **GET** Order detail (total_price/products/date/location/...)
    * **PATCH** Modify a waiting order.
    * **DELETE** Cancel a waiting order.

* **URL Params**
    * **order_id** id field in order data. (clients can use **url** in orders list data too).

* **Data Params(GET)** None

* **Data Params(PATCH)**
    * **location** (choices are **i**, **a**)

* **Data Params(DELETE)** None

* **Success response (GET)**
    * **Status code** 200
    * **Content**
```rest
{
    "total_price": 7,
    "status": "w",
    "location": "i",
    "date": "04 Mar 2018-12:44",
    "products": [
        {
            "title": "Tea",
            "price": 2,
            "option": null,
            "item": null,
            "id": 4
        },
        {
            "title": "Latte",
            "price": 5,
            "option": "Milk",
            "item": "skim",
            "id": 1
        }
    ]
}
```
* **Success response (PATCH)**
    * **Status code** 200 OK
    * **Content** 
```rest
{
    "total_price": 7,
    "status": "w",
    "location": "a",
    "date": "25 Feb 2018-09:08"
}
```

* **Success response (DELETE)**
    * **Status code** 204 NO CONTENT
    * **Content** None

* **Error response (GET/PATCH/DELETE)**
    * **Status code** 404 NOT FOUND
    * **Content** `{"detail": "Not found."}`

* **Error response (PATCH)**
    
    If client is trying ti modify non waiting order.
    * **Status code** 400 BA‌D REQUEST
    * **Content** `{"non_field_errors": ["You can only change waiting orders"]}`

    OR
    
    If client enters an invalid location, say **w**:
    * **Status code** 400 BA‌D REQUEST
    * **Content** `{"location": ["\"w\" is not a valid choice."]}`


**Modify/Delete order's product**
----
Clients can modify/delete product(s) of an waiting order.

* **url** `/api/orders/:order_id/product/:product_id/`

* **Methods**
    * **PATCH** Change product's customization.
    * **DELETE** Remove product from the order.

* **URL Params**
    * **order_id** id field in order data.
    * **product_id** product's id field in orders details api (/api/orders/:order_id/).

* **Data Params(PATCH)** 
    * **customization** An item if **items** field in product's data (if **items** field is not **null**).

* **Data Params(DELETE)**
    * **product** product's id.

* **Success response(PATCH)**
    
    imagine we send `{"customization": "whole"}`.
    
    *‌ **Status code** 200 OK
    *‌ **Content code** `{"customization": "whole"}`
    
* **Success response(DELETE)**

    *‌ **Status code** 204 NO CONTENT
    *‌ **Content code** None

* **Error response(PATCH/DELETE)**

    * **Status code** 404 NOT FOUND

    * **Content** `{"detail": "Not found."}`

        This response will show because of following reasons:
        - client entered invalid :order_id.
        - client entered invalid :product_id.
        - client is modifying a non waiting order.

* **Error response(PATCH)**
    
    If client tries to modify a product with **null** option field.
    * **Status code** 400 BAD REQUEST
    * **Content** `{"product": "The product does not support customization"}`
    
    OR
    
    If client doesnt send customization for customizable product.
    * **Status code** 400 BAD REQUEST
    * **Content** `{"product": "The product supports customization. The customization is required"}`
