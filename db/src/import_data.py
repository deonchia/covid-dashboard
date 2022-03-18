import os
import json

from pymongo import MongoClient

"""
This module imports the data from the backend MongoDB server with the credentials
taken from the Kubernetes environmental variables with the MongoClient driver.
...
:return: json.dumps(data), the queried data.
:rtype: json
"""

password = os.environ.get('SECRET_PW')
conn_str = str(os.environ.get('SVC_NAME')) + ":27017"

def get_data() -> json:
    try:
        client = MongoClient(conn_str,
            username="root", 
            password=password)

        database = client['covid']['sg']
    except ConnectionRefusedError as err: 
        print(err)
        exit

    data=list(database.find())

    client.close()
    return json.dumps(data)
