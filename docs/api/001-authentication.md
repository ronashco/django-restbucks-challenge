Users can register using api. in protected urls we need to know user. authentication implemented with auth tokens.
every user has an unique token to authenticate. in protected urls clients have to send auth tokens as request header.

**Registration (sign up)**
----
* **URL** ```/api/accounts/register/```
* **Methods** ```POST```
* **Data parameters**
    * email
    * password
* **Success response**
    * **code** 201 CREATED
    * **Content** `{"token": "CLIENT_AUTH_TOKEN"}`
* **Error response**
    * **Code** 400 BAD ‌REQUEST
    * **Content** {"email": ["This field is required."]}

    OR
    
    * **Code** 400 BAD ‌REQUEST
    * **Content** {"email": ["The email is taken."]}

    OR
    
    * **Code** 400 BAD ‌REQUEST
    * **Content** {"password": ["This field is required."]}

    OR
    
    * **Code** 400 BAD ‌REQUEST
    * **Content** {"password": ["Password must be at least 8 letters."]}


**Login**
----
If clients forget their tokens, They can fetch it using login api.
 * **url** ```/api/accounts/login/```
 * **data parameters**
    * email
    * password
* **Success response**
* **Code** 200 OK
* **Content** `{"token": "CLIENT_AUTH_TOKEN"}`
* **Error Response**
    * **code** 400 BAD ‌REQUEST
    * **content** `Invalid credentials.`
