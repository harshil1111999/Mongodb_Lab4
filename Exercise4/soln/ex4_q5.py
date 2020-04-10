from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701177:201701177@cluster0-fbwsl.mongodb.net/test?retryWrites=true&w=majority")
db=client["analytics"]


t = list(db.accounts.find(
            {"products" : {"$in" : ["Commodity"]}}
        ))
db.temp.drop()
db.temp.insert_many(t)


agr = [{"$lookup" : {
            "from" : "temp",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        { "$match" : { "name" : "Leslie Martinez" } },
        #{"$unwind" : {"path" : "$accounts"}},
        {"$project" : {"output.account_id" : 1,"_id" : 0,"output.products":1}},
        {"$unwind" : {"path" : "$output"}}
       ]


val = list(db.customers.aggregate(agr))

for v in val:
    pprint(v["output"]["account_id"])
    db.transactions.delete_one({"account_id" : v["output"]["account_id"]})
    db.accounts.delete_one({"account_id" : v["output"]["account_id"]})
    db.customers.update_one(
            {},
            {"$pull" : { "accounts" : v["output"]["account_id"]}}
            )
db.temp.drop()
