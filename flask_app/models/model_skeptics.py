#Get the connection 
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA
from flask import flash
from flask_app.models import model_user
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE

class Skeptic:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']

        self.users = []
        self.sightings = []
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one
    def user(self, data):
        return model_user.User.get_one({"id": data['user_id']})
    #if you use data then remember to match up the %(same_key)s 

    # C
    @classmethod
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO skeptics (user_id, sighting_id)"
        query += " VALUES (%(user_id)s, %(sighting_id)s);"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id

    # R
    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM skeptics;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    
    @classmethod
    def get_all_with_user_id(cls, data) -> list: #this is the same
        query = "SELECT * FROM skeptics LEFT JOIN sightings ON skeptics.sighting_id = sightings.id WHERE skeptics.user_id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

        if results_from_db:
            ol = []
            for values in results_from_db :  #turn those dictionaries into objects
                ol.append(cls(values))
            return ol # so this way we havve an entire LIST of recipes made by THAT id if we wanted filtering.... we don't need filtering
        else : return []
        
        
    @classmethod
    def get_all_with_sighting_id(cls, data) -> list: #this is the same
        query = "SELECT * FROM skeptics LEFT JOIN users ON skeptics.user_id = users.id WHERE skeptics.sighting_id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        print(results_from_db)
        if results_from_db:
            ol = cls(results_from_db[0])
            for values in results_from_db :  #turn those dictionaries into objects
                ol.users.append(ol.user(values))
            return ol 
        else : return []
    @classmethod
    def get_one_with_sighting_id_and_user_id(cls, data) -> list: #this is the same
        query = "SELECT * FROM skeptics WHERE skeptics.sighting_id= %(sighting_id)s and skeptics.user_id= %(user_id)s ;"
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        print(results_from_db)
        if results_from_db:
            return cls(results_from_db[0])
        return []

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM meals WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        if results_from_db:
            return cls(results_from_db[0])
            # for values in results_from_db :  #turn those dictionaries into objects
            #     to_object.append(cls(values))
            #return to_object
        else : return []
            
    
    # @classmethod
    # def get_one_with_account_id(cls, data) -> list: #this is the same
    #     query = "SELECT * FROM meals WHERE account_id= %(account_id)s "
    #     results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
    
    #     if results_from_db:
    #         return cls(results_from_db)
    #         # for values in results_from_db :  #turn those dictionaries into objects
    #         #     to_object.append(cls(values))
    #         # return to_object
    #     else : return []
            
    # U
    @classmethod
    def update(cls,data): #RETURNS NOTHING
        query = "UPDATE meals SET title=%(title)s, short_prep=%(short_prep)s, description=%(description)s, direction=%(direction)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)


    # D
    @classmethod 
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM meals WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
    
    @classmethod 
    def delete_with_sighting_id_and_user_id(cls,data): #RETURNS NOTHING
        query = "DELETE FROM skeptics WHERE sighting_id=%(sighting_id)s AND user_id=%(user_id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
    