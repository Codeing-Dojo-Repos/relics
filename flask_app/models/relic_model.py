from operator import is_
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user_model import User

class Relic:
    db = "week7_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.discovery_date = data["discovery_date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_st = data["updated_at"]
        self.user = None

    @classmethod
    def add_relic(cls, data):
        print("adding relic...")
        query = """insert into relics (name, description, discovery_date, user_id)
                   values (%(name)s, %(description)s, %(discovery_date)s, %(user_id)s )"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_realics(cls):
        query = """select * from relics
                   join users on relics.user_id = users.id;"""
        result = connectToMySQL(cls.db).query_db(query)

        if len(result) == 0:
            return []
        
        all_relics = []
        for cur_relic_dic in result:
            relic_instance = Relic(cur_relic_dic)
            user_dic = {
                "id": cur_relic_dic['users.id'],
                "fname": cur_relic_dic['fname'],
                "lname": cur_relic_dic['lname'],
                "email": cur_relic_dic['email'],
                "password": cur_relic_dic['password'],
                "created_at": cur_relic_dic['users.created_at'],
                "updated_at": cur_relic_dic['users.updated_at']
            }
            user_instance = User(user_dic)
            relic_instance.user = user_instance
            all_relics.append(relic_instance)
        return all_relics

    @classmethod
    def get_one_realic_and_user(cls, data):
        query = """select * from relics
                   join users on relics.user_id = users.id
                   where relics.id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)

        if len(result) == 0:
            return []
        
        cur_relic_dic = result[0]
        relic_instance = Relic(cur_relic_dic)
        user_dic = {
            "id": cur_relic_dic['users.id'],
            "fname": cur_relic_dic['fname'],
            "lname": cur_relic_dic['lname'],
            "email": cur_relic_dic['email'],
            "password": cur_relic_dic['password'],
            "created_at": cur_relic_dic['users.created_at'],
            "updated_at": cur_relic_dic['users.updated_at']
        }
        user_instance = User(user_dic)
        relic_instance.user = user_instance
        return relic_instance

    @classmethod
    def edit_relic(cls, data):
        query="""update relics
                    set name = %(name)s,
                        discovery_date = %(discovery_date)s,
                        description = %(description)s
                  where id = %(id)s"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def delete_relic(cls, data):
        query="delete from relics where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_relic(relic_data):
        print(f"data: {relic_data}")
        is_valid = True
        if len(relic_data["name"]) < 4:
            flash('name too short', "relic")
            n = relic_data["name"]
            print(f"name is {n}")
            is_valid = False
        if len(relic_data["description"]) < 10:
            flash('description too short', "relic")
            print(2)
            is_valid = False
        if relic_data["discovery_date"] == '':
            flash("no date!", "relic")
            d = relic_data["discovery_date"]
            print(f"date is {d}")
            is_valid = False
        print(f"returning {is_valid}")
        return is_valid