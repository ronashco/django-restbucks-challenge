**Fields**
----
* **product**: id field in product data - see [menu](https://github.com/mohammadh73/django-restbucks-challenge/blob/master/docs/api/002-menu.md) api)  
* **customization**: one of **items** in product data - see [menu](https://github.com/mohammadh73/django-restbucks-challenge/blob/master/docs/api/002-menu.md) api)  

**Authentication**
----
For every protected url, clients must send auth token with request headers. Protected urls marked with star (*) in documentation.
See following example:

A protected urls:

* **url** `/api/orders/cart/` *

A normal url:

* **url** `/api/orders/cart/`

Clients must set a **Authorization** header key. The value is `Token CLIENT_AUTH_TOKEN`. A client with *ABCDEFGH* token, must send following request header:

```rest
Authorization: Token ABCDEFGH
```
If the client doesnt send request headers for protected urls, the response will be:
* **Status code** 401
* **Content** `{"detail": "Authentication credentials were not provided."}`
 
To fetch client's token see [authentication](https://github.com/mohammadh73/django-restbucks-challenge/blob/master/docs/api/001-authentication.md) document.

**Orders**
----

* **Waiting order** is an order with **w** status.
