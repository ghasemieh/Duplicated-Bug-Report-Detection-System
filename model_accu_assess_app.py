#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh
# Assessment the Model Accuracy -------------------------------------------------------------------------------
# Calculate the similarity score for the reported duplicated bug report
import pandas as pd
import similarity_models as sm
import warnings
warnings.filterwarnings('ignore')
import pickle
import text_processing as tp

# Import dataset
data = pd.read_csv('Data/TestData2500.csv',sep=',')
# Remove nan from the main dataset
tp.remove_nan(data)

# Preprocessing the short_desc
processed_data_df = tp.text_preprocessing(data,"short_desc")
# # Save to file to save time
processed_data_df.to_csv('Data/processed_TestData2500_df.csv',index=False)

# Load prosecced df from file to save time
processed_data_df = pd.read_csv('Data/processed_TestData2500_df.csv',sep=',')
duplicate_df = pd.read_csv('Data/duplicate_df.csv', sep=',')
duplicated_similarity_score_list = sm.n_top_finder(new_bug_df = duplicate_df, n_top = 20, main_database = processed_data_df)

# # Save the list to a file since it takes 8 hours to create it
# with open("Data/duplicated_similarity_score_list_2500.txt", "wb") as fp:  # Pickling
#     pickle.dump(duplicated_similarity_score_list, fp)

# # Read the list from a file
with open("Data/duplicated_similarity_score_list_2500.txt", "rb") as fp:  # Unpickling
    duplicated_similarity_score_list = pickle.load(fp)

# Calculate the Recall rate
def recall_rate_calculation(name_of_algorthem):
    if name_of_algorthem == 'word2vec':
        select_algorithm = 2
        print('word2vec result:')
    elif name_of_algorthem == 'tfidf':
        select_algorithm = 3
        print('TF-idf result:')
    elif name_of_algorthem == 'bm25':
        select_algorithm = 4
        print('bm25 result:')
    else:
        return "Wrong selection"
    found_counter = 0
    not_found_counter = 0
    for x in duplicated_similarity_score_list:
        dup = x[1]
        df = x[select_algorithm]
        if df.loc[df['id'] == dup].empty:
            not_found_counter += 1
        else:
            found_counter += 1
    print('Num of duplicated report found: ', found_counter)
    print('Num of duplicated report not found: ', not_found_counter)
    print('Recall (TP/TP+FN): ', round(found_counter / len(duplicated_similarity_score_list) * 100, 2), '%\n')

# Check the results
recall_rate_calculation('word2vec')
recall_rate_calculation('tfidf')
recall_rate_calculation('bm25')

# Calculate the MRR
def MRR_rate_calculation(name_of_algorthem):
    if name_of_algorthem == 'word2vec':
        select_algorithm = 2
        print('word2vec result:')
    elif name_of_algorthem == 'tfidf':
        select_algorithm = 3
        print('TF-idf result:')
    elif name_of_algorthem == 'bm25':
        select_algorithm = 4
        print('bm25 result:')
    else:
        return "Wrong selection"
    found_counter = 0
    not_found_counter = 0
    revers_sum = 0
    for x in duplicated_similarity_score_list:
        dup = x[1]
        df = x[select_algorithm].reset_index(drop=True)
        if df.loc[df['id'] == dup].empty:
            not_found_counter += 1
        else:
            found_counter += 1
            for tup in df.itertuples():
                if int(tup.id) == dup:
                    if tup.Index == 0:
                        revers_sum += 1 / (tup.Index + 1)
                    else:
                        revers_sum += 1 / (tup.Index)

    print('Num of duplicated report found: ', found_counter)
    print('Num of duplicated report not found: ', not_found_counter)
    print('MRR_rate: ', round((1 / len(duplicated_similarity_score_list)) * revers_sum, 5), '\n')

MRR_rate_calculation('word2vec')
MRR_rate_calculation('tfidf')
MRR_rate_calculation('bm25')

# Calculate the MAP
def MAP_rate_calculation(name_of_algorthem):
    if name_of_algorthem == 'word2vec':
        select_algorithm = 2
        print('word2vec result:')
    elif name_of_algorthem == 'tfidf':
        select_algorithm = 3
        print('TF-idf result:')
    elif name_of_algorthem == 'bm25':
        select_algorithm = 4
        print('bm25 result:')
    else:
        return "Wrong selection"
    found_counter = 0
    not_found_counter = 0
    sum_overall_AP = 0
    overall_AP = 0
    for x in duplicated_similarity_score_list:
        dup = x[1]
        df = x[select_algorithm].reset_index(drop=True)

        if df.loc[df['id'] == dup].empty:
            not_found_counter += 1
        else:
            num_true_positive = 1
            sumAP = 0
            for tup in df.itertuples():
                if int(tup.id) == dup:
                    found_counter += 1
                    if tup.Index == 0:
                        sumAP += num_true_positive / (tup.Index + 1)
                    else:
                        sumAP += num_true_positive / (tup.Index)
                num_true_positive += 1
            overall_AP = (1 / num_true_positive) * sumAP
        sum_overall_AP += overall_AP

    print('Num of duplicated report found: ', found_counter)
    print('Num of duplicated report not found: ', not_found_counter)
    print('MAP_rate: ', round(sum_overall_AP / len(duplicated_similarity_score_list) * 100, 5), '\n')

MAP_rate_calculation('word2vec')
MAP_rate_calculation('tfidf')
MAP_rate_calculation('bm25')

