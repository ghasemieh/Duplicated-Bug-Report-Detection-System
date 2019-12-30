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
import normalise as ns
#from pycontractions import Contractions  # for expansion and contrations
import contractions
import re  # remove tags.

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
    short_desc_normalised = ns.normalise(short_desc_splited, verbose=False)
    short_desc_normalised_listToStr = ' '.join(map(str, short_desc_normalised))

    # Apply contractions/expansions
    short_desc_contract = contractions.fix(short_desc_normalised_listToStr)

    # remove tags.
    clean = re.compile('<.*?>')
    short_desc_removed_tag = re.sub(clean, '', str(short_desc_contract))

    # remove special characters and digits.
    short_desc_removed_special_char = [re.sub(r"[^a-zA-Z]+", ' ', k) for k in str(short_desc_removed_tag).split("\n")]

    # Remove Punctuations and Stop words
    short_desc_doc = nlp(str(short_desc_removed_special_char))
    short_desc_map = map(lambda token: token if (token.is_punct == False and token.is_stop == False) else None,
                         short_desc_doc)
    short_desc_list = list(short_desc_map)

    # Convert list to string and remove one-character word
    short_desc_string = ""
    for element in short_desc_list:
        if element is not None and len(element) > 1:
            short_desc_string += str(element) + ' '
    short_desc_string = short_desc_string[:-1]

    # Stemming/Lemmatisation.
    short_desc_lemmata = [token.lemma_ for token in nlp(short_desc_string)]
    short_desc_preprocessed = ' '.join(map(str, short_desc_lemmata))
    return short_desc_preprocessed

def text_preprocessing(df, text_attribute_name, sample_number=None):
    import time
    import progressbar as pb
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

def index_to_id(df,original_df):
    import time
    import progressbar as pb
    print('Convert index to id')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        df.loc[tup.Index,'id1'] = original_df.iloc[tup.id1]['id']
        df.loc[tup.Index,'id2'] = original_df.iloc[tup.id2]['id']
        progress.update(progvar + 1)
        progvar += 1
    print("Index to id and Remove diff product score\n --- %s seconds ---" % (time.time() - start_time))

def index_to_id_remove_diff_product_score(df,original_df):
    import time
    import progressbar as pb
    print('Convert index to id and remove diff product score')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        ID1 = original_df.iloc[tup.id1]['id']
        ID2 = original_df.iloc[tup.id2]['id']
        df.loc[tup.Index,'id1'] = ID1
        df.loc[tup.Index,'id2'] = ID2
        product1 = original_df.loc[lambda df: df['id'] == ID1,'product'].array[0]
        product2 = original_df.loc[lambda df: df['id'] == ID2,'product'].array[0]
        if product1 != product2:
            df.drop([tup.Index],inplace=True)
        progress.update(progvar + 1)
        progvar += 1
    print("Index to id and Remove diff product score\n --- %s seconds ---" % (time.time() - start_time))
    
def remove_diff_product_score(df,original_df):
    import time
    import progressbar as pb
    print('Remove record of diff product')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        product1 = original_df.loc[lambda df: df['id'] == tup.id1,'product'].array[0]
        product2 = original_df.loc[lambda df: df['id'] == tup.id2,'product'].array[0]
        if product1 != product2:
            df.drop([tup.Index],inplace=True)
        progress.update(progvar + 1)
        progvar += 1
    print("Remove diff product score --- %s seconds ---" % (time.time() - start_time))
    
def id_builder(df):
    length = len(str(len(df)))
    ID = []
    for x in df.itertuples():
        ID1 = int(x.id1)
        ID2 = int(x.id2)
        ID.append(ID1*pow(10,length) + ID2)
    ID_df = pd.DataFrame(ID, columns=['ID'])
    return  pd.merge(df, ID_df, left_index=True, right_index=True)