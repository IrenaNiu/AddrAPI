# AddrAPI

# Basic CRUD: Flask & PostgreSQL

1. Activate __PostgreSQL__ server:
    
    ```bash
    $ cd /Library/PostgreSQL/12/bin
    $ psql -U postgres
      Password for user postgres: 123456
    ```

#

2. Create a database on PostgreSQL, my database name is __"my_flask"__:
    
    ```bash
    postgres=#  CREATE DATABASE my_flask;
    postgres=#  \l 
    postgres=#  \c my_flask
    ``` 

#

3. Create an __"address"__ table on __"my_flask"__ database:
    
    ```bash
    my_flask=#  CREATE TABLE address(
                 adid SERIAL PRIMARY KEY,
                 country_lv VARCHAR(255),
                 state_lv VARCHAR(255),
                 city_lv VARCHAR(255),
                 subdiv_lv VARCHAR(255),
                 postcode VARCHAR(255),
                 street_lv VARCHAR(255)
                 ); 
    my_flask=#  \d
    ``` 

#

4. Clone this repo. Insert your database URI to __database.yaml__ file, then install all the packages needed. In this project I'm using __flask__, __flask_cors__, __flask_mysqldb__, __Flask-SQLAlchemy__ & __psycopg2__:
    ```bash
    $ git clone https://github.com/IrenaNiu/CPSC5200AddressAPI.git
    $ cd CRUD_Flask_PostgreSQL
    $ pip install flask flask_cors Flask-SQLAlchemy psycopg2
    ```

#

5. Run the server file. Make sure your PostgreSQL server is still running. Your application server will run locally at __*http://localhost:5000/*__ :
    ```bash
    $ python app.py
    ```

#

6. Give a request to the server. You can use __Postman__ app:
    
    __See the opening screen (*home.html*)__
    ```bash
    GET /
    ```

    __Post an address to database (change header and body to JSON type):__ 
    ```bash
    POST /address
    body request: {"country_lv": "us",
            "state_lv": "",
            "city_lv": "",
            "subdiv_lv": "",
            "postcode_lv": "",
            "street_lv": ""}
    ```
    __Get all addresses & specific address by id:__
    ```bash
    GET /address
    GET /address/{:id} (i.e: /1)
    ```
    __Update an address by id__:
    ```bash
    PUT /address/{:id}
    body request: {"country_lv": "us",
            "state_lv": "",
            "city_lv": "",
            "subdiv_lv": "",
            "postcode_lv": "",
            "street_lv": ""}
    ```
    __Delete an address by id:__
    ```bash
    DELETE /address/{:id}
    ```