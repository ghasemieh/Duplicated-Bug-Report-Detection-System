"""
-------------------------------------------------------
Duplicated Bug Report Detection
-------------------------------------------------------
Copyright (c) 2020.
Author: Alireza Ghasemieh
Email: a.ghasemieh65@gmail.com
https://github.com/ghasemieh
__Updated__ = 1/29/20, 6:35 AM.
-------------------------------------------------------

This module id responsible for calculating the similarity score between two given text
"""

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from Modules import postgres as ps
import time
import _pickle as cPickle
# Model-1: Similarity Score - Word2vec -------------------------------------------------------------------------
import spacy
nlp = spacy.load('en_core_web_lg')
processed_data_nlp_df = []
global main_data_len
main_data_len = len(processed_data_nlp_df)

# Convert summary str to nlp format to fasten the computation process
def word2vec_preprocess(df):
    """
        -------------------------------------------------------
        Tokenize the summary
        Use: word2vec_preprocess(df)
        -------------------------------------------------------
        Returns:
            Nothing - Create processed_data_nlp_df for the word2vec_similarity function
        -------------------------------------------------------
    """
    print('Word2Vec Preprocessing - Convert Summary to NLP Format')
    start_time = time.time()
    processed_data_nlp = []
    for tup in df.itertuples():
        processed_data_nlp.append((tup.id, tup.product, nlp(tup.processed_summary)))
    global processed_data_nlp_df
    processed_data_nlp_df = pd.DataFrame(processed_data_nlp, columns=['id', 'product', 'processed_summary'])
    global main_data_len
    main_data_len = len(processed_data_nlp_df)
    print("Save File")
    with open('processed_data_nlp_df.pickle', 'wb') as f:
        cPickle.dump(processed_data_nlp_df, f)

    execution_flag_word2vec = 1
    with open('execution_flag_word2vec.txt', 'w') as f:
        f.write('%d' % execution_flag_word2vec)

    max_id = df['id'].max()
    with open('max_id.txt', 'w') as f:
        f.write('%d' % max_id)

    print("Word2Vec Preprocess Done", "--- %s seconds ---" % (time.time() - start_time))

def word2vec_preprocess_update(df):
    print("Word2Vec Preprocessing Update - Convert Summary to NLP Format")
    start_time = time.time()

    with open('max_id.txt', 'r') as f:
        max_id = int(f.read())

    processed_data_nlp = []
    for id in range(max_id+1,df['id'].max()+1):
        tup = pd.DataFrame(ps.extract(str(id)))
        if len(tup) != 0:
            processed_data_nlp.append((tup["id"][0], tup["product"][0], nlp(str(tup["processed_summary"][0]))))
    processed_new_data_nlp_df = pd.DataFrame(processed_data_nlp, columns=['id', 'product', 'processed_summary'])
    global processed_data_nlp_df
    main_data_len = len(processed_data_nlp_df)
    if main_data_len == 0:
        print("Load File")
        with open('processed_data_nlp_df.pickle', 'rb') as f:
            processed_data_nlp_df = cPickle.load(f)
        main_data_len = len(processed_data_nlp_df)

    processed_data_nlp_df = pd.concat([processed_new_data_nlp_df, processed_data_nlp_df], ignore_index= True)

    max_id = df['id'].max()
    with open('max_id.txt', 'w') as f:
        f.write('%d' % max_id)

    print("Word2Vec Preprocessing Update Done", "--- %s seconds ---\n" % (time.time() - start_time))

# Calculate the cosine similarity score
def word2vec_similarity(id, df):
    """
        -------------------------------------------------------
        Calculate the similarity score between the given id tuple and the rest of the database
        Use: similarity_score_df = word2vec_similarity(id, df)
        -------------------------------------------------------
        Returns:
            A data frame of ids and similarity scores
        -------------------------------------------------------
    """
    try:
        with open('execution_flag_word2vec.txt', 'r') as f:
            execution_flag_word2vec = int(f.read())
    except:
        execution_flag_word2vec = 0
    try:
        with open('max_id.txt', 'r') as f:
            max_id = int(f.read())
    except:
        max_id = 0
    global processed_data_nlp_df
    main_data_len = len(processed_data_nlp_df)

    if execution_flag_word2vec == 0:
        word2vec_preprocess(df)
    elif df['id'].max() > max_id:
        word2vec_preprocess_update(df)
    elif main_data_len == 0:
        with open('processed_data_nlp_df.pickle', 'rb') as f:
            processed_data_nlp_df = cPickle.load(f)
        max_id = processed_data_nlp_df['id'].max()
        with open('max_id.txt', 'w') as f:
            f.write('%d' % max_id)
        word2vec_preprocess_update(df)
        print("Save File")
        with open('processed_data_nlp_df.pickle', 'wb') as f:
            cPickle.dump(processed_data_nlp_df, f)

    print("Word2Vec Score Calculation")
    start_time = time.time()
    similarities_score_list = []
    product_main = processed_data_nlp_df.loc[lambda df: df['id'] == id, 'product'].array[0]
    processed_summary_main = processed_data_nlp_df.loc[lambda df: df['id'] == id, 'processed_summary'].array[0]
    for doc in processed_data_nlp_df.itertuples():
        product_other = processed_data_nlp_df.loc[lambda df: df['id'] == doc.id, 'product'].array[0]
        if product_main == product_other:
            similarity_score = doc.processed_summary.similarity(processed_summary_main)
            similarities_score_list.append((doc.id, similarity_score))
    # convert to dataframe
    word2vec_similarities_score_df = pd.DataFrame(similarities_score_list, columns=['id', 'word2vec_score'])
    word2vec_similarities_score_df = word2vec_similarities_score_df.reset_index(drop=True)
    print("Word2Vec Done", "--- %s seconds ---\n" % (time.time() - start_time))
    return word2vec_similarities_score_df

# Model-2: Similarity Score - TF-idf ----------------------------------------------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
tfidf_cosine_similarities = []
execution_count_tfidf = 0

def tfidf_preprocess(df):
    """
        -------------------------------------------------------
        Calculate the similarity score between the given id tuple and the rest of the database
        Use: tfidf_preprocess(df)
        -------------------------------------------------------
        Returns:
            Nothing - Create tf-idf for the tfidf_similarities function
        -------------------------------------------------------
    """
    print('TF-IDF Preprocessing - Vectorization and Similarity Score Calculation')
    start_time = time.time()
    X_train = df['processed_summary']
    # Vectorization
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(X_train)
    # Calculate the cosine similarity score
    global tfidf_cosine_similarities
    tfidf_cosine_similarities = linear_kernel(tfidf)
    global shape_tfidf
    shape_tfidf = tfidf_cosine_similarities.shape[0]
    global execution_count_tfidf
    execution_count_tfidf += 1
    print("TF-IDF Preprocess Done", "--- %s seconds ---" % (time.time() - start_time))

def tfidf_similarities(id, df):
    """
        -------------------------------------------------------
        Calculate the similarity score between the given id tuple and the rest of the database
        Use: similarity_score_df = tfidf_similarities(id, df)
        -------------------------------------------------------
        Returns:
            A data frame of ids and similarity scores
        -------------------------------------------------------
    """
    # if execution_count_tfidf == 0:
    tfidf_preprocess(df)
    print("TF-IDF Score Calculation")
    start_time = time.time()
    index_main = df.loc[lambda df: df['id'] == id].index.array[0]
    product_main = df.loc[lambda df: df['id'] == id, 'product'].array[0]
    tfidf_cosine_similarities_list = []
    for index_other in range(shape_tfidf):
        id_other = df.iloc[index_other]['id']
        product_other = df.iloc[index_other]['product']
        if product_main == product_other:
            tfidf_cosine_similarities_list.append([id_other, tfidf_cosine_similarities[index_main, index_other]])
    # Conver to dataframe
    tfidf_cosine_similarities_score_df = pd.DataFrame(tfidf_cosine_similarities_list, columns=['id', 'tfidf_score'])
    tfidf_cosine_similarities_score_df = tfidf_cosine_similarities_score_df.reset_index(drop=True)
    print("TF-IDF Done", "--- %s seconds ---\n" % (time.time() - start_time))
    return tfidf_cosine_similarities_score_df

# Model-3: Similarity Score - BM25F -----------------------------------------------------------------------------
from rank_bm25 import BM25Okapi
processed_corpus_list = []
bm25 = []
execution_count_bm25 = 0

# preprocess - tokenize the summary to token
def bm25_preprocess(df):
    """
        -------------------------------------------------------
        Calculate the similarity score between the given id tuple and the rest of the database
        Use: bm25_preprocess(df)
        -------------------------------------------------------
        Returns:
            Nothing - Create tf-idf for the bm25_similarities function
        -------------------------------------------------------
    """
    print('BM25 Preprocess - Tokenize the Summary')
    start_time = time.time()
    global processed_corpus_list
    processed_corpus_list = []
    for x in df.itertuples():
        summary_splited = x.processed_summary.split(" ")
        processed_corpus_list.append(summary_splited)
    # Create a bm25 Object with the corpus
    global bm25
    bm25 = BM25Okapi(processed_corpus_list)
    global execution_count_bm25
    execution_count_bm25 += 1
    print("BM25 Preprocess Done", "--- %s seconds ---" % (time.time() - start_time))

# Calculate the similarity score
def bm25_similarity(id, df):
    """
        -------------------------------------------------------
        Calculate the similarity score between the given id tuple and the rest of the database
        Use: similarity_score_df = bm25_similarity(id, df)
        -------------------------------------------------------
        Returns:
            A data frame of ids and similarity scores
        -------------------------------------------------------
    """
    # if execution_count_bm25 == 0:
    bm25_preprocess(df)
    print("BM25 Score Calculation")
    start_time = time.time()
    index_main = df.loc[lambda df: df['id'] == id].index.array[0]
    product_main = df.loc[lambda df: df['id'] == id, 'product'].array[0]
    query = processed_corpus_list[index_main]
    doc_scores = bm25.get_scores(query)
    doc_scores_norm = [float(i)/max(doc_scores) for i in doc_scores]
    doc_scores_df = pd.DataFrame(doc_scores_norm, columns=['bm25_score'])
    # add id to the score list and remove unsimiliar product
    blanks = []
    for x in doc_scores_df.itertuples():
        id_other = df.iloc[x.Index]['id']
        product_other = df.iloc[x.Index]['product']
        # add id to the score list
        doc_scores_df.loc[x.Index, 'id'] = id_other
        if product_main != product_other:
            blanks.append(x.Index)
    doc_scores_df.drop(blanks, inplace=True)
    doc_scores_df = doc_scores_df.reset_index(drop=True)
    print("BM25 Done", "--- %s seconds ---\n" % (time.time() - start_time))
    return doc_scores_df

# Calculate the similarity scores and return the first n top scores  ------------------------------------------------
def similarity_score(id, df, top_n):
    """
        -------------------------------------------------------
        Calculate the word2vec, tfidf and BM25 similarity score between the given id tuple and the rest of the database
        and get the n-top records of each methods
        Use: similarity_score_df = similarity_score(id, df, top_n = 20)
        -------------------------------------------------------
        Returns:
            A data frame of ids and similarity scores
        -------------------------------------------------------
    """
    word2vec_similarity_df = word2vec_similarity(id, df).sort_values(by=['word2vec_score'], ascending=False).head(top_n)
    tfidf_similarity_df = tfidf_similarities(id, df).sort_values(by=['tfidf_score'], ascending=False).head(top_n)
    bm25_similarity_df = bm25_similarity(id, df).sort_values(by=['bm25_score'], ascending=False).head(top_n)
    return word2vec_similarity_df, tfidf_similarity_df, bm25_similarity_df

# Calculate the n-top similar bug report and return the list
def n_top_finder(new_bug_df, n_top,main_database):
    """
        -------------------------------------------------------
        Extract the similarity score for a given dataframe and all records in the database one by one
        Use: similarity_score_df = n_top_finder(new_bug_df, n_top,main_database)
        -------------------------------------------------------
        Returns:
            A list of data frames which contain the n-top similarity scores
        -------------------------------------------------------
    """
    duplicated_similarity_score_list = []
    for tup in new_bug_df.itertuples():
        word2vec_similarity_df, tfidf_similarity_df, bm25_similarity_df = similarity_score(tup.id, main_database,n_top)
        duplicated_similarity_score_list.append([tup.id, word2vec_similarity_df, tfidf_similarity_df, bm25_similarity_df])
    return duplicated_similarity_score_list

