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
"""
import time

import pymongo
from flask import Flask, render_template, request, redirect
from pandas import merge, DataFrame

from Modules import postgres as ps, similarity_models as sm
from Modules.Bugzilla_API import API_data_extract_2
from Modules.text_processing import preprocessing

app = Flask(__name__)  # Present on the website
ps.create_table()  # create the table if is not existed
with open('current_bug_id.txt', 'r') as f:
    current_bug_id = f.read()  # Set bug id pointer


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return 'There was an issue with home page'
    else:
        try:
            # Read the last 20 bug report from mongodb and put in data_df
            client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
            mydb = client["mydatabase"]
            mycol = mydb["bug_report"]
            db_read_pointer = int(current_bug_id) - 20
            last_n_bug_report = mycol.find({"id": {"$gt": db_read_pointer}})
            global data_df
            data_df = DataFrame(list(last_n_bug_report))
            data_df = data_df.sort_values(by='id', ascending=False).reset_index()
            show_df = data_df[["id", "creation_time", "summary", "duplicates"]]
            return render_template('main.html', tables=[show_df.to_html(classes='data')], titles=show_df.columns.values)
        except:
            return render_template('main.html', tables=[data_df.to_html(classes='data')], titles=data_df.columns.values)


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST' or request.method == 'GET':
        try:
            global current_bug_id
            current_bug_id_str = str(current_bug_id)
            new_bug_df = API_data_extract_2(current_bug_id_str)
            if len(new_bug_df) > 0:
                current_bug_id = new_bug_df['id'].max()
                # Update the bug id pointer
                with open('current_bug_id.txt', 'w') as f:
                    f.write('%d' % current_bug_id)
                try:
                    # Preprocess the new_bug_df
                    bug_list = []
                    new_bug_df = new_bug_df.sort_values(by='id', ascending=True).reset_index()
                    for tup in new_bug_df.itertuples():
                        processed_summary = preprocessing(new_bug_df, tup.id, 'summary')
                        bug_list.append([tup.id, tup.type, tup.product, tup.component, tup.creation_time, tup.status,
                                         tup.priority, tup.severity, tup.version, tup.summary, processed_summary,
                                         tup.duplicates])
                    processed_data_df = DataFrame(bug_list,
                                                  columns=["id", "type", "product", "component", "creation_time",
                                                           "status", "priority"
                                                      , "severity", "version", "summary", "processed_summary",
                                                           "duplicates"])
                    # Save into a bug_db SQL database
                    for tup in processed_data_df.itertuples():
                        ps.insert(tup.id, tup.type, tup.product, tup.component, tup.creation_time, tup.status,
                                  tup.priority, tup.severity, tup.version, tup.summary, tup.processed_summary,
                                  tup.duplicates)
                    return redirect('/')
                except:
                    return 'There was an issue adding your records to SQL database'
            return redirect('/')
        except:
            return 'There was an issue refreshing the page'


@app.route('/find_similar', methods=['GET', 'POST'])
def find_similar():
    if request.method == 'POST':
        task_id = request.form['id']
        # try:
        if task_id != '':
            df = ps.extract(task_id)
            # df = API_id_extract(task_id)
            # find the similar bug report
            if not df.empty:
                n_top(df)
                return render_template('main.html', tables=[result.to_html(classes='data')],
                                       titles=result.columns.values)
            else:
                return redirect('/')
        else:
            return 'There was no entry'
        # except:
        #     return 'There id is not in the database'
    else:
        return render_template('main.html', tables=[data_df.to_html(classes='data')], titles=data_df.columns.values)


# Find the n-top similar bug report
def n_top(df):
    """
        -------------------------------------------------------
        Extract the n-top most similar reports
        Use: n_top(df)
        -------------------------------------------------------
        Returns:
            A data frame to present in the web
        -------------------------------------------------------
    """
    start_time = time.time()
    original_data = ps.view()
    similarity_list = sm.n_top_finder(df, 20, original_data)
    word2vec_df = similarity_list[0][1]
    tfidf_df = similarity_list[0][2]
    bm25f_df = similarity_list[0][3]

    global result
    result = merge(word2vec_df, tfidf_df, on='id', how='outer')
    result = merge(result, bm25f_df, on='id', how='outer')
    id_summary_df = original_data[['id', 'summary', 'creation_time', "duplicates"]]
    result = merge(result, id_summary_df, on='id', how='left')
    result = result.fillna(0)
    result["total_score"] = result["word2vec_score"] + result["tfidf_score"] + result["bm25_score"]
    result = result.sort_values(['total_score', 'creation_time'], ascending=[False, True]).head(20)
    print("Calculation Done", "--- %s seconds ---\n" % (time.time() - start_time))


if __name__ == "__main__":
    app.run(debug=False)
