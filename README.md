# Personal Kitchiner
#### Video Demo:  <URL HERE>
#### Description:
This simple hybrid of shopping list and kitchen inventory system. 
You can enter all products and beverage that you have. 
Then you can enter favorite recipes. 
When you decide to prepare some recipe, application will generate shopping list, keeping in mind 
what ingredients you already have. 
After shopping you can select add product from shopping list to your stored products.
You can also cook some recipe, and ingredients will be removed from you storage.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to install some required package

```
pip install -r requirements.txt
```
## Running the application

You have several option to run application
1. Got ot folder **personalKitchiner** and run 
```
python run.py
```
2. Or you can run command
```
flask run
```
## Running the tests

To run test need to setup environment variable **FLASK_ENV** to _**testing**_
```
python -m unittest -v
```
## Structure of application
I decided to use **App Based Structure**, which means things are grouped bp application
For instance:
```
personalKitchiner/
    app/
        auth/
            __init__.py
            views.py
            models.py
        products/
            __init__.py
            views.py
            models.py
        recipe/
            __init__.py
            views.py
            models.py
        shoppoing_list/
            __init__.py
            views.py
            models.py
        static/
            ...
        templates/
            ...
        __init__.py
        helpers.py
    tests/
      __init__.py
    tests.db
    my_recipes.db
    config.py
    run.py
    requirements.txt
    README.MD
      
```
#### Folders auth/products/recipes/shopping_list
Structure of these folders are similar.
They contain models and views files
##### models.py
This is Domain models, that contain functions to run sql query in db
#####  views.py
This is controller.
I start out by creating a blueprint. Then I then map my 
view to routes using the normal decorator syntax.
 I have added comments around some of the functionality.

**auth** - login, logout and registration functionality

**products** - create, edit, delete product functionality

**recipes** - create, show, delete recipe functionality. Also adding ingredients
from recipes to shopping list. And also cook recipe for deleting ingredients from products

**shopping_list** - create shopping list and add ingredients to products. 

## To do functional

- Update recipe
- Save shopping list
- Repeat shopping list
- Find recipe to cook from existed products

## Built With

* [Flask](http://flask.pocoo.org/) - Python Microframework
* [Flask-testing](https://pythonhosted.org/Flask-Testing/) - Python framework based on unittest for testing Flask app

## Authors

* **Tetiana Voronenko** - [tvoronenko](https://github.com/tvoronenko/)