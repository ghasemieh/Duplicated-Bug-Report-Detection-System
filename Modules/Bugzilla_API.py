# Extract new bug report return as dataframe
import requests
import pandas as pd

def API_data_extract(frequency = '2h'):
    controller = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary&chfield=%5BBug%20creation%5D&chfieldfrom=-'
    get_bug_url = controller + frequency + '&chfieldto=Now'
    try:
        response = requests.get(get_bug_url)
        response_json = response.json()
        data = response_json["bugs"]
        print("Number of bug reports:", len(data))
        return pd.DataFrame(data)
    except:
        df = pd.DataFrame([])
        return df

def API_id_extract(id):
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



