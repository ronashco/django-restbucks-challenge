Restbucks coffee shop
----
A simple rest api based on [Django framework](https://www.djangoproject.com). 
You can find the scenario of project [here](https://github.com/ronashco/django-restbucks-challenge).


Project layout
----
 We're not going to use django's default directory layout. 
 For the sake of better directory layout and modular code, we made some manipulations on django's default directory layout.
 See purpose of main directories: 

- **/config**
    * contains django's settings.
    * wsgi
    * basic urls

- **/core** contains django apps. `/core/api/` directory contains rest api source based on [Django rest framework](http://www.django-rest-framework.org/) 

- **/functional_tests** project's functional (acceptance) tests.

- **/requirements**  contains project requirements, you can install requirements based on environment:
