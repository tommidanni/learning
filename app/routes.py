from app import app, db
from flask import url_for, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from app.models import User, Product, user_to_product
from app.forms import LoginForm

@app.route('/')
def index():
    return render_template('index.html')

app.route('/index')(index)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/index_2')
def index_2():
    return render_template('index_2.html')

@app.errorhandler(404)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('404.html'), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        message='You must be logged in to add items to your cart'
        return redirect(url_for('login_form', message))
    else:
        selection_statement=select(user_to_product).where(user_to_product.c.user_id==current_user.id)
        result=db.session.execute(selection_statement)
        selected_products=result.all()
        products=[]
        for p in selected_products : 
            current=Product.query.get(p[1])
            new=[current.product_name, p[2], current.product_img, current.product_price]
            products.append(new)
        return render_template('cart.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        if id is not None:
            product=Product.query.get(id)
            if product.quantity > 0:
                current_user.add_product(id, 1)
                return jsonify({"message" : "success"})
            if product.quantity <= 0:
                return jsonify({"message" : "unavailable"})
        else:
            return jsonify({"message": "invalid_id"})
    else:
        return jsonify({"message": "invalid_request_method"})

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if request.method== 'POST':
        current_user.empty_cart()
        return jsonify({"message" : "success"})

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
    products=Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/single-product')
def single_product():
    return render_template('single-product.html')

@app.route('/login-form/<message>', methods=['GET', 'POST'])
def login_form(message):
    form= LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login_form', message='Wrong username or password'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login_form.html', form=form, message=message)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

