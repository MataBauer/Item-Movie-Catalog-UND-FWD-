
# Item Catalog proje

Goal of this project was to build an application which will operate with database and users will be allowed to: *see, create, edit* and *delete* items online. 

## Getting started

In this folder you have:
1. ReadMe.md
	*This document is written in Markdown and will give you overview about this project, it's functionality and prerequisites.*  
   *To get more information about markdown* [click here](https://guides.github.com/features/mastering-markdown/#syntax).
2. Python3 code files:
	* application.py - *Includes code of the application*
	* movies_db_create.py - *Includes code to create database and fill it with values (values are included in this file)*
	* movies_db_mapping.py - *Include code for database set up and mapping *
	* movies_db_sanity_check.py - *Includes couple of statements to check if DB is running and is filled with correct data
3. templates folder:
	*Includes html template files.*
4. static folder:
	*Includes all images and also the style sheet for web.*
5. JSON file:
	*Includes client_secret key and allow the users to log in and see if they are already logged in.*
 

## Prerequisites

You need to have:
1. installed virtual machine (I used VirtualBox)
   * *You can finde referneces and dowload the VirtualBox here:* [virtualbox.org](https://www.virtualbox.org).
2. installed software which cofigures the VM (I used Vagrant)
   * *You can finde referneces and dowload the Vagrant here:* [virtualbox.org](https://www.vagrantup.com/intro/index.html).
   * *You will also need a configuration file to set up your VM;* [get configuration file](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) _-> this file is provieded by UDACITY_
3. you will also need Python 3.5.2 (it will be installed automatically if you will use the vagrant configuration file listed previously) 
   * *If you need more referneces on Python 3.5.2 you can read through documentation on* [Python.org](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


## Get the application runing!

### Prepare the virtual machine
- Once you installed VM, and set up Vagrant (as mentioned previously in _**Prerequisites**_) you are ready to bring up your VM. To do so open your *terminal*, go to directory where you installed *Vagrant* use `vagrant up` command and then log in with `vagrant ssh`.

### Create the database

Open your terminal, start your VM, make sure you are in proper folder (folder where you downloaded files from this archive). 
Follow these steps:
1. `python3 movies_db_create.py` -> creates a database (in the file you can see that *movies.db* file was created.
2. to ensure you have data in DB and it is properly run `python3 movies_db_sanity_check.py` and check its output

### Run the server

You are still in your terminal and VM (you must be in the same folder where your DB was created). You previously created the DB no follow below steps to run the server:
1. `python3 application.py` -> this will start the server
	![Alt text](/static/rm-img1.png?raw=true "screenshot1")
2. open your web browser and go to `localhost:5000/` -> *this will load the main page*
3. on the left side you find the menu -> click on the *Projec Item Catlog*
	* this will redirect you to the movie category site, from there you move to:
		* see all categories / create new / edit / delete category
		* see movies within specific category / create new movie under specific category / edit and delete movie

## To create/edit/delete you need to be logged in with your Google account!
There is an authorisation set up with Google application. Users who do not want to log in will only see categories and movies in categories but will not be able to create, edit or delete any items.
	


# THE END

Now you see my favourite movies in my movie database. Have fun with playing around with it. :smirk:

### Author

Martina Bauerova
