from couchdb import Server

email = 'ruddy@gmail.com'
doc = {'_id':'ruddy@gmail.com', 'Database': 'dev-jackie-bucket2', 'School': 'Bloomington', 'Name': 'Ruddy', 'S3': 'peter-marsfarm-08052020', 'S3_link': 'https://peter-marsfarm-08052020.s3.us-east-2.amazonaws.com/', 'Device': 'Back40', 'Email': 'ruddy@gmail.com'}

doc2 = {'_id':'howard.webb@gmail.com', 'Database': 'dev-jackie-bucket2', 'School': 'Webster Groves', 'Name': 'Howard Webb', 'Devices': [{'Device': {'Database': 'dev-jackie-bucket', 'Name': 'Farm1', 'S3_link': 'https://peter-marsfarm-08052020.s3.us-east-2.amazonaws.com/', 'S3': 'peter-marsfarm-08052020'}}, {'Device': {'Database': 'dev-jackie-bucket2', 'Name': 'Farm2', 'S3_link': 'https://peter-marsfarm-08052020.s3.us-east-2.amazonaws.com/', 'S3': 'peter-marsfarm-08052020'}}], 'S3': 'peter-marsfarm-08052020', 'S3_link': 'https://peter-marsfarm-08052020.s3.us-east-2.amazonaws.com/', 'Device': 'Farm2', 'Email': 'webb.howard@gmail.com'}

#print(doc["_id"])
print(doc["Email"])
print(doc["Device"])
#print(doc["Devices"][0])
      

url = 'http://openagbloom.ddns.net/couch'
# this should not change
db_name = 'user'
server = Server(url)
db = server[db_name]
id, rev = db.save(doc)
#db[email] = doc
print(id, rev)
#rec = db['howard.webb@gmail.com']
#print("Got Rec")
#print(rec)

