# Duplicate Bug Report Detection System

![Image of Bug](/image/BR1.png)

## Background
As software programs become increasingly large and complex, it is important to improve the quality of software maintenance. Bug report recommendations can significantly improve the triaging of bug reports. It is difficult to inspect the new incoming reports manually to route to the developers who have fixed the duplicate bugs. Automatic identification of Duplicate bug reports is a critical research problem in the software repositories’ mining area.

## Aim
The project aims to propose an effective unsupervised and supervised models to detect duplicate bug report in the Bugzilla repository. The search engine finds the top-N most similar reports to a given report, and deduplicate issues faster. Moreover, it presents an analytical dashboard to developers to understand the different aspects of the bug reports’ statistics and major sources of bug generation.

## ETL Process
The search engine extracts data using the Bugzilla REST API https://wiki.mozilla.org/Bugzilla:REST_API and creates a data-lake using MongoDB. Then it verifies the data quality and conducts data wrangling and cleaning. 

## Data Preparation
Since the data is considered as big data the engine loads the data to Hadoop HDFS and performs text preprocessing using PySpark which includes: 
- Converting text to lowercase
- Splitting the words into 3 steps using 
  1. ASCII character identification for English 
  2. split by space  
  3. Wordninja
- Applying normalizes
- Applying contractions or expansions
- Removing punctuations, tags, special characters, digits
- Stemming
- Lemmatization. 

Then it stores the processed data in PostgreSQL. 

## Evaluation
The empirical evaluation is performed on the open datasets of the Bugzilla repository. The metrics used for evaluation are Mean Average Precision (MAP), Mean Reciprocal Rank (MRR) and Recall rate. 

## Visualization and Presentation
The top-N most similar reports to a given report are presented on a web page using Flask. Also, It presents the developer the statistical information about the bug reports in a dashboard using D3.js

## Implementation Method
Implementation Method: The search engine is implemented on AWS using Docker Composer and ECS with Fargate

![Image of Application Process](/image/ApplicationStructure.jpg)

# Installation Guide

To run the application there are two options:
- Use the docker image
- Use the source code 

## Implement the Application Using Docker

Please follow the steps below:

1. Install docker CE from https://docs.docker.com/install/linux/docker-ce/ubuntu/
2. Install docker compose from https://docs.docker.com/compose/install/
3. Create a vim file with name `docker-compose.yml` where you want to run the application using the content below:

```
version: '3'
services:
  web:
    build: .
    image: applia65/duplicatebugreportsearchengine:web
    # restart: always
    environment:
      DATABASE_HOST: postgres_docker
      DATABASE_USER: postgres
      DATABASE_PASSWD: password123
      DATABASE_DATABSE_NAME: bug_database
      MONGO_ADDRESS: mongodb://mongodb_docker:27017/
    ports:
      - "0.0.0.0:5000:5000"
    depends_on:
      - postgres_docker
      - mongodb_docker

  postgres_docker:
    image: postgres:10
    # restart: always
    # # Allow access from Development machine
    # ports:
    #  - "0.0.0.0:5432:5432"
    volumes:
      - ./pg_data/:/var/lib/postgresql/data:Z
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password123
      POSTGRES_DB: bug_database

  mongodb_docker:
    image: mongo:latest
    #restart: always
    #environment:
    #  MONGO_INITDB_ROOT_USERNAME: root
    #  MONGO_INITDB_ROOT_PASSWORD: example
```

4. Execute the code below where you create `docker-compose.yml` and wait until your server downloads all containers.

```
sudo docker-compose pull
```

5. Run the application.

```
sudo docker-compose up
```

6. Open your browser using `0.0.0.0:5000` address.

## Implement the Application Using the Source Code

Please follow the steps below:

1. Pull the codes by git
2. Install all requirements 

```
pip install --no-cache-dir -r requirements.txt
```

3. Install the WordNet which is about 900 MB

```
python -m spacy download en_core_web_lg
```

4. Install MongoDB from https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
5. Run the MongoDB service

```
sudo systemctl start mongod
```

6. Verify that MongoDB has started successfully.

```
sudo systemctl status mongod
```

7. Install PostgreSQL Version 10 from https://www.postgresql.org/download/linux/debian/

8. Run the Postgresql service

```
sudo systemctl start postgresql
```

9. Verify that Postgresql has started successfully.

```
sudo systemctl status postgresql
```

10. Create a user `postgres` with password `password123`

11. Run the application 

```
python ./main.py
```

12. Open your browser using `0.0.0.0:5000` address.

### Please contact me if you have any question.
