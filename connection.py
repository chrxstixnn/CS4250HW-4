from pymongo import MongoClient



DB_NAME = "Homework4"
DB_HOST = "localhost"
DB_PORT = 27017


#connects database
def connectDataBase():
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db

    except:
        print("Database not connected successfully")

# creates page document for database
def createPage(col, url, html):
    col.insert_one({"url": url, "html": str(html)})
