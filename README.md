# FourGuys
A web application for food ordering and delivery system for 
a fictional restaurant called __*Four Guys*__. This web app 
is developed for the Software Engineering (CSc 322) class.

## Getting Started
1. Fork from the master repository and clone it to your computer:
    
    `$ git clone https://github.com/<your username>/FourGuys.git`

2. Get inside the directory and create a virtual environment:
   
    ```
    $ cd FourGuys
    $ virtualenv venv --python=python3
    ```
    
    __IMPORTANT__: The web app is written in Python3 and as such the interpreter for the
    virtual environment __*must*__ be of that version.
   
3. Activate your virtual environment:
    
    `$ source venv/bin/activate`
    
4. Install packages from `requirements.txt` that are needed to run the web app:

    `$ pip install -r requirements.txt`
    
5. Create the required database, its tables and preload them with dummy data:

    `$ python manage.py rebuild_database`
    
    __IMPORTANT__: This command must be executed before the next step or otherwise
    Python interpreter will throw an error.

6. Run the application:

    `$ python manage.py runserver`

## Contributors
The contributors to this awesome (and laborious) project are: 
- Sunny Mei
- Adam Ibrahim
- Miguel Dominguez
- Ichwan Palongengi