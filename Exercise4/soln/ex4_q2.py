from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701177:201701177@cluster0-fbwsl.mongodb.net/test?retryWrites=true&w=majority")
db=client["analytics"]


t = list(db.accounts.find(
            {"products" : {"$in" : ["Commodity"]}}
        ))
db.temp.drop()
db.temp.insert_many(t)

agr = [#{"$unwind" : {"path" : "$accounts"}},
       {"$lookup" : {
            "from" : "temp",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        {"$project" : {"_id" : 0}},
        {"$unwind" : {"path" : "$output"}},
        {"$group" : {"_id" : "$email","avg_limit" : {"$avg" : "$output.limit"}}}
       ]


val = list(db.customers.aggregate(agr))
db.temp.drop()
db.temp.insert_many(val)

for v in val:
    pprint(v)
    
db.temp.drop()





