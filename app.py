import streamlit as st 
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

PWD = open("mongodb.pwd", "r").read().strip()

uri = f"mongodb+srv://vidar1812:{PWD}@cluster0.zaamq.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
database = client['Database']

collection = database['Products']

results = collection.aggregate([
    {
        '$addFields': {
            'StockOrders': {
                '$add': [
                    '$UnitsInStock', '$UnitsOnOrder'
                ]
            }
        }
    }, {
        '$match': {
            '$expr': {
                '$gt': [
                    '$ReorderLevel', '$StockOrders'
                ]
            }
        }
    }
])
st.header('Products with insufficient stock')
for res in results:
    st.write(res)


