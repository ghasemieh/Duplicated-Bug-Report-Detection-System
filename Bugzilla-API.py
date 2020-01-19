# Extract new bug report and save them in SQLite
import requests
import json

def API_extract(frequency = '6h'):
    controller = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,summary,status,creation_time,product,component&chfield=%5BBug%20creation%5D&chfieldfrom=-'
    get_bug_url = controller + frequency + '&chfieldto=Now'
    response = requests.get(get_bug_url)
    response_json = response.json()
    parent = response_json["bugs"]
    for item in parent:
        #print(item['id'],item['creation_time'],item['product'])
    return parent

print(API_extract('6h'))


