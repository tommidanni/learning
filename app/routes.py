from app import app
from flask import render_template, flash, redirect
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.forms import LoginForm

@app.route('/')
def index():
    return render_template('index.html')

app.route('/index')(index)

@app.route('/index_2')
def index_2():
    return render_template('index_2.html')

@app.route('/404')
def page_not_found():
    return render_template('404.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/single-news')
def single_news():
    return render_template('single-news.html')

@app.route('/single-product')
def single_product():
    return render_template('single-product.html')

@app.route('/login-form', methods=['GET', 'POST'])
def login_form():
    form= LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.user.data)
        if user is None or not user.check_password(form.password.data):
            flash('wrong username or password')
            return redirect(url_for('/login_form'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

