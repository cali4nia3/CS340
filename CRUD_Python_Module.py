# Example Python Code to Insert a Document 

import os
import logging
from pymongo import MongoClient 
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from bson.objectid import ObjectId 

# Logger Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username
        PASS = password 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        
        # Validate password
        if not PASS:
            raise ValueError("Invalid PASS variable/Constructor arg")
            
        # 
        # Initialize Connection 
        # 
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d/?authSource=%s' % (USER,PASS,HOST,PORT, DB))
            self.client.admin.command('ping')
            logger.info("Connection Successful")
        except ConnectionFailure as e:
            logger.error("Failed connection to: %s", e)
            raise
            
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

###########################################################################
# CREATE METHOD
# Insert a document into the assigned collection
# Parameters:
#     data (dict) - chosen document to insert into collection
# Return:
#     boolean - true if successful, false if not
# Raises:
#     TypeError - if data entered is not type dict
#     ValueError - if data entered is empty
###########################################################################

            
    def create(self, data):
        # Validation Checks
        if not isinstance(data, dict):
            raise TypeError(f"Required dict data type, received {type(data).__name__}")
        if not data:
            raise ValueError("Empty document inserted")
            
        try:
            # Attempt to insert new document
            result = self.collection.insert_one(data)
            logger.info("New document inserted into collection _id: %s",
                        result.inserted_id)
            return True
        except OperationFailure as e:
            logger.error("New document insert failed: %s", e)
            return False

    
###########################################################################
# READ METHOD
# Finds a document matching the requested query
# Parameters:
#     query (dict) - identifying search criteria for requested document
# Return:
#     list - all successfully matching documents
# Raises:
#     TypeError - Invalid non-dict data type entered
###########################################################################


    def read(self, query):
        # Validation Check
        if not isinstance(query, dict):
            raise TypeError(f"Required dict data type, received {type(query).__name__}")
        
        try:
            # Attempt to find queried document
            result = self.collection.find(query)
            documents = list(result)
            logger.info("Read request returned %d documents matching query",
                        len(documents))
            return documents
        except OperationFailure as e:
            logger.error("Read request failed: %s", e)
            return []
    
###########################################################################
# UPDATE METHOD
# Updates all documents matching query with new_data entered
# Parameters:
#     query (dict) - identifying search criteria for requested document(s)
#     new_data (dict) - all fields to set with new data
# Return:
#     int - # of all successfully updated documents
# Raises:
#     TypeError - Invalid non-dict data type entered
#     ValueError - Either query or new_data are empty
###########################################################################

    def update(self, query, new_data):
        # Validation Checks
        if not isinstance(query, dict) or not isinstance(new_data, dict):
            raise TypeError("Parameters query & new_data must both be dicts")
        if not query:
            raise ValueError("query parameter cannot be null")
        if not new_data:
            raise ValueError("new_data parameter cannot be null")
            
        try:
            result = self.collection.update_many(query, {"$set": new_data})
            logger.info("Updated %d document(s)", result.modified_count)
            return result.modified_count
        except OperationFailure as e:
            logger.error("Updated documents failed: %s", e)
            raise
            
###########################################################################
# DELETE METHOD
# Deletes all documents matching entered query parameter
# Parameters:
#     query (dict) - identifying  criteria for all requested deletion document(s)
# Return:
#     int = # of documents deleted
# Raises:
#     TypeError - Invalid non-dict data type entered
#     ValueError - Invalid or empty query entered
###########################################################################

    def delete(self, query):
        # Validation Checks
        if not isinstance(query, dict):
            raise TypeError(f"Input query parameter must be of type dict, type entered {type(query).__name__}")
        if not query:
            raise ValueError("query cannot be empty")
            
        try:
            result = self.collection.delete_many(query)
            logger.info("Successfully deleted %d document(s)", result.deleted_count)
            return result.deleted_count
        except OperationFailure as e:
            logger.error("Deletion attempt failed: %s", e)
            raise
        