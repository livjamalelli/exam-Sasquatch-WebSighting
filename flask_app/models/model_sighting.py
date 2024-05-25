#Get the connection 
from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app import DATABASE_SCHEMA
from flask_app.models import model_user
import datetime
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE

class Sighting:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.location = data['location']
        self.happening = data['happening']
        self.sighting_at = data['sighting_at'] #this is the date it was sighted at
        self.sasquatch_count = data['sasquatch_count']

        self.user_id = data['user_id']
        self.creator = []
        if 'creator' in data:
            self.creator = data['creator'] 
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one
    def get_time_old(self):
        # f = '%Y-%m-%d %H:%M:%S'
        # offset = datetime.datetime.now()- self.created_at
        time = largest_time_unit((datetime.datetime.now()- self.created_at).seconds)
        return time
    #if you use data then remember to match up the %(same_key)s 

    # C
    @classmethod
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO sightings (location, happening, sighting_at, sasquatch_count, user_id) VALUES (%(location)s, %(happening)s, %(sighting_at)s, %(sasquatch_count)s, %(user_id)s)"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id

    # R
    # @classmethod
    # def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
    #     query = "SELECT * FROM sightings;"
    #     results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
    #     to_object =[] 
    #     if results_from_db:
    #         for values in results_from_db :  #turn those dictionaries into objects
    #             to_object.append(cls(values))
    #         return to_object
    #     else : return []
    
    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM sightings;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                object =cls(values)
                object.creator = model_user.User.get_one({"id" : values['user_id']})
                to_object.append(object)
            return to_object
        else : return []

    @classmethod
    def get_all_with_creators(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id "
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                object =cls(values)
                object.creator = values['first_name'] + " " + values['last_name']#model_user.User.get_one({"id" : values['user_id']})
                to_object.append(object)
            return to_object
        else : return []
        



    @classmethod
    def get_one(cls, data):#this is the same throws the object back as a signle instead of a list 
        query = "SELECT * FROM sightings WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
            
    @classmethod
    def get_one_with_creator(cls, data):#this is the same throws the object back as a signle instead of a list 
        query = "SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id WHERE sightings.id= %(id)s;"
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        print(results_from_db)
        if results_from_db:
            # user = model_user.User.get_one({"id": results_from_db[0]['user_id']})
            # to_obj = dict(results_from_db[0])
            # to_obj['creator'] = user
            # return_object = cls(to_obj)
            # return return_object
            object =cls(results_from_db[0])
            object.creator = results_from_db[0]['first_name'] + " " + results_from_db[0]['last_name']
            #model_user.User.get_one({"id" : results_from_db[0]['user_id']}).get_full_name()
            return object
        else : return []
            



    # U
    @classmethod
    def update(cls,data): #RETURNS NOTHING
        query = "UPDATE sightings SET location=%(location)s, happening=%(happening)s, sighting_at=%(sighting_at)s, sasquatch_count=%(sasquatch_count)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod 
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM sightings WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['location']) < 2:
            flash("The location needs to be at least 2 characters long", "sighting_location_err")
            is_valid = False
        # if "short_prep" not in data:
        #     flash("You didn't say if this took under 30 minutes", "meal_short_prep_err")
        #     is_valid = False
        # if len(data['description']) < 2:
        #     flash("The discription must be at least 2 characters", "meal_description_err")
        #     is_valid = False
        if len(data['happening']) < 2:
            flash("The directions must be at least 2 characters", "sasquatch_happeing_err")
            is_valid = False
        if data['sighting_at'] == '':
            flash("You didn't say when you saw them!", "sasquatch_date_err")
            is_valid = False
        if data['sasquatch_count'] == '0':
            flash("This shouldn't be 0", "sasquatch_count_err")
        return is_valid


        
        
def largest_time_unit(seconds):
    if seconds > 86400: #day
        return str(int(seconds/86400)) + " days" 
    elif seconds > 3600: #hour
        return str(int(seconds/3600)) + " hours" 
    elif seconds > 60 : 
        return str(int(seconds/60)) + " minutes"
    else :
        return str(seconds) + " seconds"

