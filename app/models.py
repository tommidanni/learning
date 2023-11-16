from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin
from sqlalchemy import insert, update, select, delete




user_to_product = db.Table(
    'user_to_product',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name = 'fk_user')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id', name = 'fk_product')),
    db.Column('quantity', db.Integer, nullable=False),
    db.UniqueConstraint('user_id', 'product_id', name='uq_user_product')
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name=db.Column(db.String(64), index=True, unique=True)
    product_price=db.Column(db.Integer)
    quantity=db.Column(db.Integer)
    product_type=db.Column(db.String(64))
    product_desc=db.Column(db.Text)
    product_img=db.Column(db.String(64))

    users = db.relationship('User', secondary='user_to_product', back_populates='products')

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    products = db.relationship('Product', secondary='user_to_product', back_populates='users')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_product(self, product_id, quantity):

        product=Product.query.get(product_id)

        if product is None or product.quantity <= 0 :
            return False
        
        if product in self.products :

            get_statement= (select(user_to_product.c.quantity)).where(user_to_product.c.product_id== product_id and user_to_product.c.user_id == self.id)
            cell=db.session.execute(get_statement)
            new_quantity=cell.fetchone()[0]+1

            update_statement = (update(user_to_product).where(user_to_product.c.product_id == product_id and user_to_product.c.user_id==self.id).values(quantity=new_quantity))
            db.session.execute(update_statement)

        else :  
            
            insert_statement = insert(user_to_product).values(user_id=self.id, product_id=product_id, quantity=quantity)
            db.session.execute(insert_statement)
            
        db.session.commit()
        return True

    def empty_cart(self):

        delete_statement=(delete(user_to_product).where(user_to_product.c.user_id==self.id))
        print(delete_statement)
        db.session.execute(delete_statement)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
