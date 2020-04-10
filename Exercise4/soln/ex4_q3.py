from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701177:201701177@cluster0-fbwsl.mongodb.net/test?retryWrites=true&w=majority")
db=client["analytics"]

agr = [{"$match" : {"username" : "ashley97"}},
       #{"$unwind" : {"path" : "$accounts"}}, 
       {"$lookup" : {
            "from" : "transactions",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        {"$unwind" : {"path" : "$output"}},
        {"$project": {"username" : "ashley97","ans":"output.transactions.total",
                     "items": {
                "$filter": {
                    "input": "$output.transactions",
                    "as": "s",
                    "cond": {
                        "$eq": ["$$s.transaction_code", "buy"]
                    }
                }
            }
         }
         },
        {"$unwind" : {"path" : "$items"}},
        {"$group" : {"_id" : "$username","ans" : {"$sum" : {"$toDecimal" : "$items.total"}}}},
       {"$project" : {
                   "_id" : 0,
                   "username" : "ashley97",
                   "ans" : {"$round" : ["$ans",0]}
               }}
    ]

val = db.customers.aggregate(agr)

for v in val:
    pprint(v)
    
