#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import postgres as ps
from flask import Flask, render_template, request, redirect
import similarity_models as sm

# Present on the website
app = Flask(__name__)

new_data_df = pd.DataFrame()
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        try:
            show_df = new_data_df[["id", "summary"]]
            return render_template('main.html', tables=[show_df.to_html(classes='data')], titles=show_df.columns.values)
        except:
            return render_template('main.html', tables=[new_data_df.to_html(classes='data')],titles=new_data_df.columns.values)

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        try:
            global new_data_df
            # Extract data from Bugzilla website fot the past 2 hours
            data_df = API_data_extract('2h')
            # Preprocess the data_df
            data_list = []
            for tup in data_df.itertuples():
                # search database if the bug report was new then do processing and save it in the database
                processed_summary = preprocessing(data_df, tup.id, 'summary')
                data_list.append([tup.id, tup.type, tup.product, tup.component, tup.creation_time,
                                  tup.status, tup.priority, tup.severity, tup.version, tup.summary, processed_summary])
            new_data_df = pd.DataFrame(data_list,
                                       columns=["id", "type", "product", "component", "creation_time", "status",
                                                "priority", "severity", "version", "summary", "processed_summary"])
            new_data_df = new_data_df.sort_values(by='id', ascending=False).reset_index()
            # find the similar bug report

            return redirect('/')
        except:
            return 'There was an issue adding your task'

@app.route('/save_db', methods=['GET', 'POST'])
def insert_db():
    try:
        # create the table if is not existed
        ps.create_table()
        # Save into a SQL database
        for tup in new_data_df.itertuples():
            ps.insert(tup.id,tup.type,tup.product,tup.component,tup.creation_time,tup.status,
                      tup.priority,tup.severity,tup.version,tup.summary,tup.processed_summary)
        return redirect('/')
    except:
        return 'There was an issue adding your task'

@app.route('/find_id',methods=['GET', 'POST'])
def find_id():
    if request.method == 'POST':
        task_id = request.form['id']
        # try:
        # Buuuuuuuuuuuuuuuuuuuuuuuuuuggggggggggggggggggggggggggggggggggggggggg
        result_list = ps.extract(task_id)
        ls = list(result_list[0])
        df = pd.DataFrame(ls,columns=["id", "type", "product", "component", "creation_time", "status",
                                                "priority", "severity", "version", "summary", "processed_summary"])
        print(df)
            # find the similar bug report
        print(n_top(df))
        return redirect('/')
        # except:
        #     return 'There was an issue calculating the similarity'
    else:
        return render_template('main.html', tables=[new_data_df.to_html(classes='data')],titles=new_data_df.columns.values)

# Find the n-top similar bug report
trigger = 0
def n_top(df):
    global trigger
    if trigger == 0:
        global original_data
        original_data = ps.view()
        trigger = 1
    similarity_list = sm.n_top_finder(df,10,original_data)
    print(similarity_list)

if __name__ == "__main__":
    app.run(debug=True)