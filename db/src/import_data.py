import os
import json

from pymongo import MongoClient

password = os.environ.get('SECRET_PW')
conn_str = str(os.environ.get('SVC_NAME')) + ":27017"

def get_data() -> list:
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
