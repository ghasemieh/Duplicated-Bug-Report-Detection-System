#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import postgres as ps
from flask import Flask, render_template, request, redirect
import time

# Present on the website

app = Flask(__name__)

new_data_df = pd.DataFrame()

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['id']
        # new_task = Todo(content=task_content)

        try:
            # db.session.add(new_task)
            # db.session.commit()
            print(task_content)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('main.html', tables=[new_data_df.to_html(classes='data')],
                                   titles=new_data_df.columns.values)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        main()
        return redirect('/')


def main():
    # Extract data from Bugzilla website fot the past 2 hours
    data_df = API_data_extract('2h')

    # Preprocess the data_df
    data_list = []
    for tup in data_df.itertuples():
        processed_summary = preprocessing(data_df,tup.id,'summary')
        data_list.append([tup.id,tup.product,tup.component,tup.creation_time,tup.summary,processed_summary,tup.status])
    global new_data_df
    new_data_df = pd.DataFrame(data_list,columns = ["id","product","component","creation_time","summary","processed_summary","status"])

    # create the table if is not existed
    ps.create_table()
    # Save into a SQL database
    for tup in new_data_df.itertuples():
        ps.insert(tup.id,tup.product,tup.component,tup.creation_time,tup.summary,tup.processed_summary,tup.status)

    # Find the n-top similar bug report


if __name__ == "__main__":
    app.run(debug=True)