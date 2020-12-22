# convert XML to JSON data and store it in mongodb

import xmltodict
import json
import ast
import pymongo

client = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@task3-cluster.yep8d.mongodb.net/<DATABASENAME>?retryWrites=true&w=majority")
db = client.get_database('<DATABASENAME>')

Collection = db["Users"]

def remove_at(st: str):
  return str(st[1:])

with open("Users.xml") as xml_file: 
  with open("Users.json", "w") as json_file: 
    i = 0 
    for line in xml_file:
      if i < 2:
        i = i + 1
        continue
      data_dict = xmltodict.parse(line)  
      json_data = json.dumps(data_dict)
      res = ast.literal_eval(json_data)
      # print(res['row'])
      res = res['row']

      keys = []
      for key, val in res.items():
        keys.append(key)

      for key in keys:
        res[remove_at(key)] = res.pop(key)
      
      json_data = json.dumps(res)
      json_file.write(json_data) 
      json_file.write('\n')
      if isinstance(json_data, list): 
        Collection.insert_many(json_data)   
      else: 
        Collection.insert_one(json_data)



