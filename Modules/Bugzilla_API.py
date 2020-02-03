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
# Extract new bug report return as dataframe
import pandas as pd
import pymongo
import requests
import datetime
import pytz


def API_data_extract(from_a_preiod_of_time_untill_now='2h'):
    """
        -------------------------------------------------------
        Extract data from bugzilla website based on the a period of time untill now and then insert to the
        mongoDB to make a data-lake
        Use: data = API_data_extract(from_a_preiod_of_time_untill_now = '2h')
        -------------------------------------------------------
        Returns:
            A data frame of the data
        -------------------------------------------------------
    """
    controller = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary,duplicates&chfield=%5BBug%20creation%5D&chfieldfrom=-'
    get_bug_url = controller + from_a_preiod_of_time_untill_now + '&chfieldto=Now'
    try:
        # Extract data from Bugzilla
        response = requests.get(get_bug_url)
        response_json = response.json()
        data = response_json["bugs"]
        print("Number of bug reports:", len(data))

        # Initiate mongoDB
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = client["mydatabase"]
        mycol = mydb["bug_report"]
        mycol.create_index([('id', pymongo.ASCENDING)], unique=True)

        for tup in data:
            # convert the date and time
            time_convert = datetime.datetime.strptime(tup['creation_time'], "%Y-%m-%dT%H:%M:%SZ")
            tup["creation_time"] = time_convert
            # add insertion time to the record
            tz_London = pytz.timezone('Europe/London')
            tup['insertion_time'] = datetime.datetime.now(tz_London)
            # Insert record to mongoDB
            try:
                mycol.insert_one(tup)
            except:
                print(tup['id'], ' Duplicate Bug Report')
        data = pd.DataFrame(data)
        data.drop(columns=['_id'], inplace=True)
        return data
    except:
        print("API Error")


def API_id_extract(id):
    """
        -------------------------------------------------------
        Extract data from bugzilla website based on the ID
        Use: data = API_data_extract(id = 100)
        -------------------------------------------------------
        Returns:
            A data frame of the data
        -------------------------------------------------------
    """
    id_str = str(id)
    get_bug_url = 'https://bugzilla.mozilla.org/rest/bug/' + id_str +'?include_fields=id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary'
    try:
        response = requests.get(get_bug_url)
        response_json = response.json()
        data = response_json["bugs"]
        print(data)
        return pd.DataFrame(data)
    except:
        df = pd.DataFrame([])
        return df



