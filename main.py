#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import postgres as ps


# Extract data from Bugzilla website fot the past 2 hours
data_df = API_data_extract('3h')

# Preprocess the data_df
data_list = []
for tup in data_df.itertuples():
    processed_summary = preprocessing(data_df,tup.id,'summary')
    data_list.append([tup.id,tup.product,tup.component,tup.creation_time,tup.summary,processed_summary,tup.status])
new_data_df = pd.DataFrame(data_list,columns = ["id","product","component","creation_time","summary","processed_summary","status"])

# create the table if is not existed
ps.create_table()
# Save into a SQL database
for tup in new_data_df.itertuples():
    ps.insert(tup.id,tup.product,tup.component,tup.creation_time,tup.summary,tup.processed_summary,tup.status)

# Find the n-top similar bug report

# Present on the website