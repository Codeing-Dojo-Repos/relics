from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import relic_model
import re
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

class User:
    db = 'week7_db'

    def __init__( self, data ):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.relics = []

    @staticmethod
    def validata_email(email):
        is_valid = True
        if len(email) <= 2:
            flash("Email gotta be > 2 chars", "reg")
            is_valid = False
        if not emailRegex.match(email):
            flash('Invalid email addy', "reg")
            is_valid = False
        return is_valid

    @staticmethod
    def validata_fname(fname):
        print('validating fname...')
        is_valid = True
        if len(fname) < 3:
            flash("First name gotta be > 2", "reg")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validata_lname(lname):
        print('validating lname...')
        is_valid = True
        if len(lname) < 3:
            flash("Last name gotta be > 2", "reg")
            is_valid = False
        return is_valid

    @staticmethod
    def validata_password( password, cpassword ):
        is_valid = True
        if len(password) < 8:
            flash("password gotta be > 7", "reg")
            is_valid = False
        if password != cpassword:
            flash("password have to match", "reg")
            is_valid = False
        return is_valid

    @staticmethod
    def validate(data):
        is_valid = True
        if not User.validata_fname(data['fname']):
            is_valid = False
        return is_valid

    @classmethod
    def insert(cls, data):
        query = """insert into users (fname, lname, email, `password`)
                    values (%(fname)s, %(lname)s, %(email)s, %(password)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = """select id, fname, lname, email, password
                    from users
                    where email like %(email)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """select id, fname, lname, email, password
                    from users
                    where id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]
    
    @classmethod
    def get_relics_by_user(cls, data):
        query = """select * from relics
                    where user_id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
