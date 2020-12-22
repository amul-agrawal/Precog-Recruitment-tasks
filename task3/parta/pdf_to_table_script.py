import tabula
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@task3-cluster.yep8d.mongodb.net/<DATABASENAME>?retryWrites=true&w=majority")

db = client.get_database('<DATABASENAME>')

def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')


path = str(input("Enter the path: "))
name = str(input("Enter the Collection name for database: "))

if db.get_collection(name) is not None:
  print("Change collection name, there is already a collection with this name.")
  exit(0)

records = db.create_collection(name)

tabula.convert_into(path , f"./{name}.csv" , output_format="csv", pages='all')

print(csv_to_json(f"./{name}.csv"))

records.insert_many(csv_to_json(f"./{name}.csv", header=0))
