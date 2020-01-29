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

from Modules.Bugzilla_API import API_data_extract
from Modules.text_processing import preprocessing
import pandas as pd
from Modules import postgres as ps, similarity_models as sm
from flask import Flask, render_template, request, redirect

# Present on the website
app = Flask(__name__)
# create the table if is not existed
ps.create_table('temp_bug_db',True)
ps.create_table('bug_db')

data_df = pd.DataFrame()
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return 'There was an issue with home page'
    else:
        try:
            show_df = data_df[["id", "creation_time", "summary","duplicates"]]
            return render_template('main.html', tables=[show_df.to_html(classes='data')], titles=show_df.columns.values)
        except:
            return render_template('main.html', tables=[data_df.to_html(classes='data')],titles=data_df.columns.values)

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST' or request.method == 'GET':
        try:
            global data_df
            # Extract data from Bugzilla website fot the past n hours (xh), days (xd), month (xm), year (xy)
            data_df = API_data_extract('10d')
            data_df = data_df.sort_values(by='id', ascending=False).reset_index()
            return redirect('/')
        except:
            return 'There was an issue refreshing the page'

@app.route('/save_db', methods=['GET', 'POST'])
def save_db(db_name = 'temp_bug_db'):
    try:
        # Preprocess the data_df
        data_list = []
        global data_df
        temp_df = data_df.sort_values(by='id', ascending=True).reset_index()
        for tup in temp_df.itertuples():
            # search database if the bug report was new then do processing and save it in the database
            processed_summary = preprocessing(data_df, tup.id, 'summary')
            data_list.append([tup.id, tup.type, tup.product, tup.component, tup.creation_time,
                              tup.status, tup.priority, tup.severity, tup.version, tup.summary, processed_summary,tup.duplicates])
        new_data_df = pd.DataFrame(data_list, columns=["id", "type", "product", "component", "creation_time", "status",
                                                       "priority", "severity", "version", "summary","processed_summary","duplicates"])
        # Save into a temp_bug_db database
        for tup in new_data_df.itertuples():
            ps.insert(db_name,tup.id,tup.type,tup.product,tup.component,tup.creation_time,tup.status,
                      tup.priority,tup.severity,tup.version,tup.summary,tup.processed_summary,tup.duplicates)
        # Update the bug_db database
        ps.update_db()
        return redirect('/')
    except:
        return 'There was an issue adding your records to data base'

@app.route('/find_similar',methods=['GET', 'POST'])
def find_similar(db_name = 'bug_db'):
    if request.method == 'POST':
        ps.update_db()
        task_id = request.form['id']
        try:
            if task_id != '':
                df = ps.extract(db_name, task_id)
                # df = API_id_extract(task_id)
                # find the similar bug report
                if not df.empty:
                    n_top(df)
                    return render_template('main.html', tables=[result.to_html(classes='data')],titles=result.columns.values)
                else:
                    return redirect('/')
            else:
                return 'There was no entry'
        except:
            return 'There id is not in the database'
    else:
        return render_template('main.html', tables=[data_df.to_html(classes='data')],titles=data_df.columns.values)

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
    original_data = ps.view('bug_db')
    similarity_list = sm.n_top_finder(df,10,original_data)
    word2vec_df = similarity_list[0][1]
    tfidf = similarity_list[0][2]
    bm25f = similarity_list[0][3]
    global result
    result = pd.merge(word2vec_df,tfidf, on='id',how='outer')
    result = pd.merge(result,bm25f, on='id',how='outer')
    id_summary_df = original_data[['id','summary','creation_time', "duplicates"]]
    result = pd.merge(result,id_summary_df, on='id',how='left')

if __name__ == "__main__":
    app.run(debug=True)