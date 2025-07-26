import os
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Product, Category
from forms import RegisterForm, LoginForm, ProductForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

admin = Admin(app, name='Admin Panel')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Category, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash('Muvaffaqiyatli ro‘yxatdan o‘tildi!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login yoki parol noto‘g‘ri')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file = filename
        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            image=image_file,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Mahsulot qo‘shildi!')
        return redirect(url_for('home'))
    return render_template('add_product.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
