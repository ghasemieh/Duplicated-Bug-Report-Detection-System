# Extract new bug report return as dataframe
import requests
import pandas as pd

def API_data_extract(frequency = '2h'):
    controller = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,summary,status,creation_time,product,component&chfield=%5BBug%20creation%5D&chfieldfrom=-'
    get_bug_url = controller + frequency + '&chfieldto=Now'
    response = requests.get(get_bug_url)
    response_json = response.json()
    data = response_json["bugs"]
    print("Number of bug reports:", len(data))
    return pd.DataFrame(data)



