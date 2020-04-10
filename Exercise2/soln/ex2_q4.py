
#Recommended to use python try-except block to perform error handling.
from pprint import pprint
#use pprint instead of print to clearly print output documents
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure
client=MongoClient("mongodb+srv://201701177:201701177@cluster0-fbwsl.mongodb.net/test?retryWrites=true&w=majority")
db=client["201701177"]
try:
    client.admin.command('ismaster')

except ConnectionFailure:
    print('Server not available')

except OperationFailure:
    print('wrong credentials')

else:
    print('connected to database')
    t = db.Sales.aggregate([{"$match" : {"storeLocation":"Denver"}},
                            {"$group" : {
                                    "_id":"null",
                                    "Total" : {"$sum" : {"$sum" : 
                                        {"$map" : 
                                            {
                                                "input" : "$items",
                                                "as" : "temp",
                                                "in" : {"$multiply" : [ "$$temp.price", "$$temp.quantity" ]}
                                            }}
                                        }}
                                    }}
                                ])

finally:
	client.close()

for docs in t:
    pprint(docs)
