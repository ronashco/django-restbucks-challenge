Every single order contains one or more product(s). for submit order, clients must add products to cart.

**Cart api**
----
* **url** `/api/orders/cart/` *
* **Methods** 
    * **GET** List of cart item
    * **POST** Add product to cart
    * **DELETE** remove product from cart
* **Data Params (GET)**
    None
* **Data Params (POST)**
    * product 
    * customization (an item from product's item list)
* **Data Params (DELETE)**
    * product
* **Success response‌ (GET)**
    * **Status code** 200 OK
    * **Content** Card information and list of products. see following example:
```rest
    {
      "count": "2",                       -> count of items
      "total_price": "5",                 -> count of 
      "products": [                       ->‌ products list
          {
            "title": "Latte",
            "price": 5,
            "option": "Milk",
            "selected_item": "skim",
            "id": 1
          },
          {
            "title": "Tea",
            "price": 2,
            "option": null, 
            "selected_item": null,
            "id": 4
          }, 
          ...
    }

```
* **Success response‌ (POST)**
    * **Status code** 201 CREATED
    * **Content** None

* **Error response (POST)**
    Every bad request (invalid data parameters) will raise validation error with 400 status code and associated error message.
    * **Status code** 400 BAD REQUEST

* **Success response‌ (DELETE)**
    * **Status code** 204 NO CONTENT
    * **Content** None

* **Error response (DELETE)**
    * **Status code** 404 NOT FOUND
    * **Content** `{"detail": "Not found."}`
