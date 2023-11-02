from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin



cart_to_product = Table(
    'user_to_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name=db.Column(db.String(64), index=True, unique=True)
    product_price=db.Column(db.Integer)
    product_desc=db.Column(db.Text)



    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

def Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), index=True, unique=True)

    products = db.relationship('Product', secondary='', back_populates='carts')

    def __repr__(self):
        return '<Cart of client {}>'.format(self.username)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

