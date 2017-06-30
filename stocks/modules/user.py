"""
  USER MODEL
"""
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.admin.mod_acl.models import ACL_User_Roles


class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    ts_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    ts_updted = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = 'users'

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    # status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, id=None, email=None):
        if id:
            u = self.query.filter(User.id == id).first()
            if u:
                self.__build_obj__(u)
        elif email:
            self.email = email
            u = self.query.filter(User.email == email).first()
            if u:
                self.__build_obj__(u)

    def __repr__(self):
        return '<User %r, %r>' % (self.name, self.id)

    def __build_obj__(self, obj):
        self.id = int(obj.id)
        self.name = obj.name
        self.email = obj.email
        self.ts_created = obj.ts_created
        self.ts_updted = obj.ts_updted
        self.status = obj.status
        self.password = obj.password

    def save(self):
        if self.id == None:
            new_user = self
            db.session.add( new_user )
        db.session.commit()

    def delete( self ):
        if self.id:
            delete_user = self.query.filter( User.id == self.id ).first()
            if not delete_user:
                return False
            db.session.delete( delete_user )
            db.session.commit()
            return True
        return False

    def auth( self, password_to_check ):
        if self.id:
            auth = check_password_hash( self.password, password_to_check )
            if auth:
                return True
        return False

    def get_user_role( self ):
        if self.id:
            return ACL_User_Roles().get_by_user( self.id )

    def get_all( self ):
      users = []
      for u in self.query.filter().all():
        users.append( User( u.id ) )
      return users
  
class UserMeta(Base):

    __tablename__ = 'usermeta'

    key   = db.Column(db.String(128) , nullable=False)
    value = db.Column(db.String(256) , nullable=False)

# End File: app/admin/mod_user/models.py
