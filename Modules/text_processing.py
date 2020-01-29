#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

# Alireza Ghasemieh
# a.ghasemieh65@gmail.com
# 2019 - 2020
# This module is responsible to preprocess the text inside a
# data frame and gives a data frame with the processed text
# It perform the following processes to the text:

# Convert to lowercase
# Split the words using 1. ASCII character identification for english 2. Split by Space  3. wordninja
# Apply normlise
# Apply contractions/expansions
# Remove punctuations
# remove tags.
# remove special characters and digits.
# Stemming/Lemmatisation.

# The input is the df name and the textual attribute
# name and the sample size from the df if you want to
# conduct preprocess to a portion of the df
# ---------------------------------------------------------------------------
# The following is the dependency list of the module
# conda install -c conda-forge spacy
# !pip install wordninja
# !pip install normalise
# !pip install pycontractions
# conda install -c conda-forge spacy-lookups-data
# !python -m spacy download en_core_web_lg
# ---------------------------------------------------------------------------
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import spacy
nlp = spacy.load('en_core_web_lg')
#import nltk
# nltk.download('brown')
# nltk.download('names')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
import wordninja as nj  # for spliting the words in each documents
# import normalise as ns
#from pycontractions import Contractions  # for expansion and contrations
import contractions
import re  # remove tags.
import time
import progressbar as pb

def remove_nan(df):
    print('Remove NA')
    blanks = []
    print("Before removing the NaN:")
    print(df.isnull().sum())
    for x in df.itertuples():
        if type(x.short_desc)!=str: # detect the NaN
            blanks.append(x.Index)
        elif not x.short_desc: # detect empty string
            blanks.append(x.Index)
    df.drop(blanks,inplace=True)
    print("\nAfter removing the NaN:\n",df.isnull().sum())

def remove_nan_processed(df):
    print('Remove NA')
    blanks = []
    print("Before removing the NaN:")
    print(df.isnull().sum())
    for x in df.itertuples():
        if type(x.short_desc_processed)!=str: # detect the NaN
            blanks.append(x.Index)
        elif not x.short_desc_processed: # detect empty string
            blanks.append(x.Index)
    df.drop(blanks,inplace=True)
    print("\nAfter removing the NaN:\n",df.isnull().sum())

def preprocessing(df, id, text_attribute_name):
    # Extract and convert short_desc to string
    row = df[df['id'] == int(id)]  # Extract a tuple from the dataframe
    short_desc_to_string = row[text_attribute_name].to_string(index=False)  # Conver short_desc to string
    short_desc_to_string = short_desc_to_string[1:]  # Remove the first space char from the begnning

    # Convert to lowercase
    short_desc_lowercase = short_desc_to_string.lower()

    # Split the words using 1. ASCII character identification for english 2. Split by Space  3. wordninja
    short_desc_splited = nj.split(short_desc_lowercase)

    # Apply normlise
    # short_desc_normalised = ns.normalise(short_desc_splited, verbose=False)

    short_desc_normalised_listToStr = ' '.join(map(str, short_desc_splited))

    # Apply contractions/expansions
    short_desc_contract = contractions.fix(short_desc_normalised_listToStr)

    # remove tags.
    clean = re.compile('<.*?>')
    short_desc_removed_tag = re.sub(clean, '', str(short_desc_contract))

    # remove special characters and digits.
    short_desc_removed_special_char = [re.sub(r"[^a-zA-Z]+", ' ', k) for k in str(short_desc_removed_tag).split("\n")]

    # Remove Punctuations and Stop words
    short_desc_doc = nlp(str(short_desc_removed_special_char))
    short_desc_list = []
    for token in short_desc_doc:
        if token.is_punct == False and token.is_stop == False:
            short_desc_list.append(token)
        
    #Convert list to string
    short_desc_string = ""    
    for element in short_desc_list:  
        short_desc_string += str(element) +' '
    
    # Stemming/Lemmatisation.
    short_desc_lemmata = [token.lemma_ for token in nlp(short_desc_string)]
    short_desc_preprocessed = ' '.join(map(str, short_desc_lemmata))

    # Remove single letters
    result = ' '.join( [w for w in short_desc_preprocessed.split() if len(w)>1] )
    return result

def text_preprocessing(df, text_attribute_name, sample_number=None):
    start_time = time.time()
    print('Preprocessing the text')
    if sample_number is not None:
        sample_size = sample_number  # Sample Size
        progress = pb.ProgressBar(maxval=sample_size).start()
    else:
        dataset_length = len(df)
        progress = pb.ProgressBar(maxval=dataset_length).start()
    progvar = 0
    processed_string_list = []

    for x in df.itertuples():
        string = preprocessing(df, x.id, text_attribute_name)
        processed_string_list.append((x.id, string))

        # Show the progress in the output
        progress.update(progvar + 1)
        progvar += 1

        # Terminate the process when reach to sample size
        if (sample_number is not None) and (progvar >= sample_size):
            break
    # Convert list to dataframe
    text = text_attribute_name + '_processed'
    processed_string_df = pd.DataFrame(processed_string_list, columns=['id', text])
    del processed_string_list

    # Join two df
    processed_data_df = pd.merge(processed_string_df, df, on='id')
    # remove NA
    remove_nan_processed(processed_data_df)
    # show the time of process
    print("Text preprocessing --- %s seconds ---" % (time.time() - start_time))
    return processed_data_df