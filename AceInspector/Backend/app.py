from sqlalchemy_serializer import SerializerMixin
from 





class Users(db.model, SerlializerMixin):
    __tablename__='users'