from pymongo import MongoClient

# logon string to get into the database
URL = 'mongodb+srv://webbhm:sHzHKD9_vZUGCZ4@gbe-d.cc79x.mongodb.net/'

class MongoUtil(object):
    
    def __init__(self, db="gbe"):
        # Create a database client
        url = URL + db
        #url = 'mongodb+srv://webbhm:sHzHKD9_vZUGCZ4@gbe-d.cc79x.mongodb.net/gbe'
        print("Init", url)
        self._client = MongoClient(url)
        print("Initialized")
        
    # save activity records
    def save_many(self, db, col, rec_set):
        # save array of records to database (db) and collection (col)
        db = self._client[db]
        col = db[col]
        ret = col.insert_many(rec_set)
        pprint(ret)
        
    def find(self, db, col, query):
        return self._client[db][col].find(query)
    
    # Main function used to access observtion data
    def aggregate(self, db, col, query):
        return self._client[db][col].aggregate(query)
    
    def count(self, db, col, query):
        return self._client[db][col].count(query)
    
    def distinct(self, db, col, item):
        return self._client[db][col].distinct(item)
    
if __name__ == "__main__":
    mu = MongoUtil("gbe")
    mu.find("gbe", "2020", {"subject.attribute.name":"temp"})
