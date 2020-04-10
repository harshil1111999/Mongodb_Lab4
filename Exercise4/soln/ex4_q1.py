from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701177:201701177@cluster0-fbwsl.mongodb.net/test?retryWrites=true&w=majority")
db=client["analytics"]


t = list(db.accounts.find(
            {"products" : {"$in" : ["InvestmentStock"]}}
        ))
db.temp.drop()
db.temp.insert_many(t)

#print(db.collection_names())
agr = [{"$unwind" : {"path" : "$accounts"}}, 
       {"$lookup" : {
            "from" : "temp",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        {"$project" : {"accounts" : 1, "username" : 1, "name" : 1, "email" : 1,"_id" : 0,"output.products" :1}}
       ]

val = list(db.customers.aggregate(agr))
db.temp.drop()
for v in val:
    pprint(v)