from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from validate_email import validate_email
from config import db, bcrypt

import dns.resolver 
import re

Base = declarative_base()

# ----------------------------------------------------------------------------------------------------- 
#                                                                                        CLASS USER
# -----------------------------------------------------------------------------------------------------

class User(db.model, SerlializerMixin):
    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
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
        
    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        domain = email.split('@')[1]
        try:
            dns.resolver.resolve(domain, 'MX')
        except dns.resolver.NXDOMAIN:
            raise ValueError("Invalid email domain")
        except dns.resolver.NoAnswer:
            raise ValueError("Invalid email domain")

        if not validate_email(email):
            raise ValueError("Email does not exist")

        return email
    
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
    company_name = db.Column(db.String)
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                      SUB-CLASS ADMIN
# ----------------------------------------------------------------------------------------------------- 

class Admin(User):
    __tablename__='admins'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                           CLASS SITE
# ----------------------------------------------------------------------------------------------------- 

class Site(db.Model, SerializerMixin):
    __tablename__='sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String, unique=True)
    ahj = db.Column(db.String)
    notes = db.Column(db.String)
    wo = db.Column(db.Integer)
    po = db.Column(db.Integer)
    
    poc = db.Column(db.String) ## -- possible relationship to 'users'
    
    schedule_info = db.column(db.Datetime) ## -- should be related to 'tickets'
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                         CLASS TICKET
# ----------------------------------------------------------------------------------------------------- 

class Ticket(db.Model, SerializerMixin):
    __tablename__='Tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                      CLASS PROPOSALS
# ----------------------------------------------------------------------------------------------------- 

class Proposal(db.Model, SerializerMixin):
    __tablename__='proposals'
    
    id = db.Column(db.Integer, primary_key=True)
    
# ----------------------------------------------------------------------------------------------------- 
#                                                                                           CLASS PARTS
# ----------------------------------------------------------------------------------------------------- 

class Part(db.Model, SerializerMixin):
    __tablename__='parts'
    
    id = db.Column(db.Integer, primary_key=True)
    # GETS FREAKY HERE BABYYYYYYY! OH YEA!