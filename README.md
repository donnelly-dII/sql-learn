# sql-learn

# Install

## Prerequisites

This project assumes that you have the following technologies available either on your local machine, or for whatever environment you're implementing and running
in: 

```
python 3.6 + 
pip (version 20+ preferred)
docker desktop (only if planning to run DB in container) 
MySQL Workbench (highly reccomended for visualizing data)
```

## Installing SQL DB

This is a learning project for SQL, so obviously we'll need a SQL DB to work with! I've chosen to use MySQL as it's the most popular open-source SQL DB in the world. MySQL also has many tools and integrations inside of python that are useful that we can use later. 

Now you'll need to setup a MySQL database to connect on the backend of our flask API server. I used docker, but any type of MySQL server connection can be tied into 
the application through the environment variables configured (More on this later). 

To create your ```mysql``` container, run the following command in terminal or command prompt:
```
docker run --name test-sql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<password> -e MYSQL_DATABASE=test -d mysql:latest
```
Make sure to enter your own value for password! After creating your container, boot it up by running:
```
docker start test-sql
```

You can connnect to this via the Workbench app now


To Install, we reccomend first creating a venv running python3.6+. 
Once in your activated virtual environment, install the application requirements:
```
pip install -r requirements
```



## Setup & Run Flask API Server

To execute the server, simply run the file located at:
```
sql_learning_app.run
```
