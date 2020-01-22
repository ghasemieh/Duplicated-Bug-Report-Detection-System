#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import postgres as ps
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Present on the website
app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'password123',
    'db': 'bug_database',
    'host': '127.0.0.1',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    product = db.Column(db.String(20), nullable=False)
    component = db.Column(db.String(20), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(5), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.String(200), nullable=False)
    processed_summary = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

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

@app.route('/find_id/<int:id>')
def find_id(id):
    task_content = request.form['id']
    task = Todo.query.get_or_404(task_content)

    try:
        print(task)
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

def main():
    # Extract data from Bugzilla website fot the past 2 hours
    data_df = API_data_extract('2h')

    # Preprocess the data_df
    data_list = []
    for tup in data_df.itertuples():
        processed_summary = preprocessing(data_df,tup.id,'summary')
        data_list.append([tup.id,tup.type, tup.product,tup.component,tup.creation_time,
                          tup.status, tup.priority, tup.severity, tup.version, tup.summary,processed_summary])
    global new_data_df
    new_data_df = pd.DataFrame(data_list,columns = ["id","type","product","component","creation_time","status","priority",
                                                    "severity","version","summary","processed_summary"])

    # create the table if is not existed
    ps.create_table()
    # Save into a SQL database
    for tup in new_data_df.itertuples():
        ps.insert(tup.id,tup.product,tup.component,tup.creation_time,tup.summary,tup.processed_summary,tup.status)

    # Find the n-top similar bug report


if __name__ == "__main__":
    app.run(debug=True)