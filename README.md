# Product_info
Demonstrates how to dynamically populate entries for Flask-WTF/WTForms fieldlists 

## Getting Started
People might use WTForms when they build web apps in Python. It provides a type of field called "fieldlist" where multiple instances of the same field type are kept as a list. There is another type of field called "formfield" where a form can be used as a field of another form. It is common to couple these 2 together, i.e. a form has a field composed of a list of sub-forms. 

However, there is few example showing how to populate the objects with data from the database or vise versa when both "fieldlist" and "formlist" are used. Here is a solution I figured out myself. In the view.py, I write 2 functions: populate_from_database and populate_to_database, both of which handle populating recursively for every entry in the form and its sub-forms. This is not ideal. Ideally, functions dealing with populating should be seperated from the view.py and be grouped with the objects either in forms.py or models.py. But it works. Hope there will be better solutions coming out soon.

I illustrate the solution with a tiny web app in Flask. Here I defined a simple schema as shown below. 


When you get into the web app, you can first search for a specific 'category', say 'Shoes'. 


It exist! You can select the one that you think is most relevant to your search.

You will find a multi-layers form with information retrieved from the database. You can just a take a look or make changes as you like. Don't forget to click 'Submit'. 

### Prerequisites

Before you install, it is suggested to set up a virtual environment for your Python for better management. You can get this done by either virtualenv(https://virtualenv.pypa.io/en/stable/) or conda(https://github.com/conda/conda). 

Then, you should install all dependent packages by typing:
pip install -r requirements.txt

### Installing 

* Fork the repo.

* Create a new branch.

* Connect to a database. I used PostgreSQL and if you choose to go for other ones. Please modify the lines in config.py to set up the connection with the database. 

* Create the tables in the database. I use SQLAlchemy so you can simply type the following in your command line:
    
python manage.py shell  
from manage.py import db
db.create_all()  
quit()  

* Run the app. In your command line, type:
python manae.py runserver 

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used, with many 
* [PostgreSQL](https://www.postgresql.org/) - Database
* [jQuery](https://jquery.com/) - Front-end dynamic display 

## Todo

### Fix front-end
The front-end can(should) be seperated into 3 files (.html, .css and .js). I didn't make it happen on my own laptop. So currently all things are just messed up together in the .html. 

## Comments
Very welcome! 
Please feel free to say whatever you want to make about the solution or the shitty looking front-end. 
 
## Contributing
Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to me.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Credits
I used the folder structure and followed some practice as suggestd by Mr.Grinberg. You can find the source code of his project along with license information below. I am very grateful for his contributions to open source.

Project: Flasky  https://github.com/miguelgrinberg/flasky
Copyright (c) 2013 Miguel Grinberg
License (MIT) https://github.com/miguelgrinberg/flasky/blob/master/LICENSE
