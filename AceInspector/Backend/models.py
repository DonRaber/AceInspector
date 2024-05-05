from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

import re

from config import db, bcrypt

# ----------------------------------------------------------------------------------------------------- 
#                                                                                        CLASS USER
# -----------------------------------------------------------------------------------------------------

class User(db.model, SerlializerMixin):
    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)
    
    # -------------------
    #  Password Hashing
    # -------------------
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Access Denied")
    
    @password_hash.setter
    def password_hash(self, password):
        new_hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))

        self._password_hash = new_hashed_password.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    #------------------ 
    # Validations
    # -----------------
    
    @validates('password')
    def validates_password(self, key, password):
        if len(password) < 6:
            raise ValueError("Make sure your password is at least 7 characters")
        elif re.search('[0-9]',password) is None:
            raise ValueError("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            raise ValueError("Make sure your password has a capital letter in it")
        else:
            return password
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                 SUB-CLASS TECHNICIAN
# -----------------------------------------------------------------------------------------------------    
        
class Technician(User):
    __tablename__='technicians'
    
    id = db.Column(db.Integer, primary_key=True)
    license_no = db.Column(db.String, unique=True)
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                     SUB-CLASS CLIENT
# ----------------------------------------------------------------------------------------------------- 
    
class Client(User):
    __tablename__='clients'
    
    id = db.Column(db.Integer, primary_key=True)
    
    
