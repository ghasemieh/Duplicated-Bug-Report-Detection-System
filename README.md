# Duplicate Bug Report Detection System

##Background
As software programs become increasingly large and complex, it is important to improve the quality of software maintenance. Bug report recommendations can significantly improve the triaging of bug reports. It is difficult to inspect the new incoming reports manually to route to the developers who have fixed the duplicate bugs. Automatic identification of Duplicate bug reports is a critical research problem in the software repositories’ mining area.

##Aim
The aim of this project is to propose an effective unsupervised model for duplicate bug recommendations.

###Method
The model combines the similarity scores from tf-IDF, Word2Vec and BM25F models.

###Evaluation Parameters 
The empirical evaluation is performed on the open datasets of Bugzilla repository. The metrics used for evaluation are Mean Average Precision(MAP), Mean Reciprocal Rank(MRR) and Recall rate.

###ETL
Data is available from https://wiki.mozilla.org/Bugzilla:REST_API is source to types of the bug records, where we run cron jobs and fetch the data in incremental way. 

###Visualization
Web-based framework to show the top most similar/duplicate bugs.
