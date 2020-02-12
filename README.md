# Duplicate Bug Report Detection System

![Image of Bug](/image/BR1.png)

## Background
As software programs become increasingly large and complex, it is important to improve the quality of software maintenance. Bug report recommendations can significantly improve the triaging of bug reports. It is difficult to inspect the new incoming reports manually to route to the developers who have fixed the duplicate bugs. Automatic identification of Duplicate bug reports is a critical research problem in the software repositories’ mining area.

## Aim
The aim of the project is to propose an effective unsupervised and supervised models to detect duplicate bug report in the Bugzilla repository. The search engine finds the top-N most similar reports to a given report, and deduplicate issues faster. Moreover, it presents an analytical dashboard to developers to understand the different aspects of the bug reports’ statistics and major sources of bug generation.

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
The top-N most similar reports to a given report is presented on a web page using Flask. Also, It presents the developer the statistical information about the bug reports in a dashboard using D3.js

## Implementation Method
Implementation Method: The search engine is implemented on AWS using Docker Composer and ECS with Fargate

![Image of Application Process](/image/ApplicationStructure.jpg)

