**Menu(List of products) api**
-----
* **url**```/api/products/```
* **methods** ```GET```
* **Success Response**

    * **code:** 200
    * **content:** 
```
[
    {
        "title": "Cappuccino",
        "price": 6,
        "option": "Size",
        "items": [
            "small",
            "medium",
            "large"
        ],
        "id": 1
    },
    {
        "title": "Tea",
        "price": 2,
        "option": null,
        "items": null,
        "id": 4
    },
    {
        "title": "Cookie",
        "price": 6,
        "option": "Kind",
        "items": [
            "chocolate",
            "chip",
            "ginger"
        ],
        "id": 2
    },
      ...
  
]
```
The purpose of option/item fields is customize the orders.

Note that if option is null, items will be null.
