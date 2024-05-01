# Finn_Mikkola_Portfolio
Finn Mikkola's portfolio repository for projects

Here is a list of projects that I can made either in School or in the Jump Program or just for fun!

capstone.ipynb was my capstone project in college. My classmates and I worked with proffesional company Intrusion looking at data for phishing websites. My model uses dynamic time warping to compare website traffic of known phishing sites, to other sites. It also looks at other factors such as peak traffic, date created, and how sharply the traffic declines after peak traffic. I unfortuatnly cannot share the original csv of data as I am not allowed to share it per requests of the Intrusion.

ETL project was a project I undertook with soe of my fellow jump teamates. Together we set up a ETL pipeline in AWS using s3, lambda, rds, and a ec2 instance to host our findings. More information is available in the read me. It is no longer hosted on aws as we deleted the instances to make room for new ones, but all the code and resources used is in this repository

Pep_one was the first major project my teamates and I took on in the Cognixia Jump Program. We used pandas to load in a dataset with resturant data. We cleaned the data by formatting rows, combinging csvs and yaml files, deleting and adding rows, and removing null values. Then we transfered the data into a sql alchemy database via python and created a simple frontend to perfrom user queries.

Scikit is a simple machine learning project that uses linear regression and logistic regression to train and predict the classiv iris data set. It was my first introduction with scikit learn. I also coded my own attempt at simple linear regression to predict gpa values vs hours studied.

Fallout_Hacking_Game: this is just a fun little python project I made to mimic the popular video game Fallouts hacking mini game. Try to guess the password in 4 attempts! 

Flask is a project I created using the very popular python framework Flask. It is a backend and somewhat of a front end for a pokemon cards api. I load in data from an exisitnig public pokemon card api, clean the data, then use Flask and Sql alchmey to build a database and schema to store information about the cards and user data. The api is hosted on a local server after running app.py and a simple html interface is in place to help users easily access pre coded sql queries.
