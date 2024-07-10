from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from wtforms.validators import DataRequired, NumberRange, URL
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from datetime import datetime
import os
import smtplib


app = Flask(__name__)
FLASK_KEY = os.environ.get('FLASK_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')
EMAIL = "onids1312@gmail.com"
app.config['SECRET_KEY'] = FLASK_KEY
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Decorator function for Admin
def admin_only(f):
    @wraps(f)
    def admin_required(*args, **kwargs):
        if current_user.id != 1 and current_user.id != 2:
            return abort(403)
        return f(*args, **kwargs)
    return admin_required


class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BSU_DB.db'
db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)
db.init_app(app)

class ProductList(db.Model):
    __tablename__ = 'product_list'
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)




with app.app_context():
    db.create_all()


class ProductForm(FlaskForm):
    product_name = StringField("Product Name")
    description = StringField("Description")
    price = IntegerField("Price")
    stock_quantity = IntegerField("Stock Quantity")
    img_url = StringField("Product Image URL")
    submit = SubmitField("Submit")


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Cart')


@app.route('/')
def home():
    current_year = datetime.now().year

    orders = session.get('orders')
    return render_template('index.html', active_page='home', total_quantity=orders, current_year=current_year)

@app.route('/admin_login', methods=['GET', 'POST'])
def login():
    current_year = datetime.now().year
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_result = db.session.execute(db.select(User).where(User.username == username))
        pass_result = db.session.execute(db.select(User).where(User.password == password))
        user = user_result.scalar()
        pwd = pass_result.scalar()
        print(user,pwd)
        if user and pwd:
            flash("You we're successfully logged in.")
            login_user(user)
            return redirect(url_for("admin"))
        else:
            flash("Please check your login credentials, if you're not admin, please leave this page.")
            return redirect(url_for('login'))


    return render_template('login.html', current_year=current_year)


@app.route('/admin', methods=["GET", "POST"])
@admin_only
def admin():
    current_year = datetime.now().year
    all_products = ProductList.query.all()


    return render_template('admin.html', current_year=current_year, products=all_products)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/store', methods=["GET", "POST"])
def store():
    current_year = datetime.now().year

    all_products = ProductList.query.all()
    form = AddToCartForm()

    if request.method == "POST":
        try:
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
        except ValueError:
            flash("Invalid data type for product ID or quantity", 'danger')
            return redirect(url_for('store'))

        form = AddToCartForm(request.form)

        if form.validate_on_submit():
            product = ProductList.query.get_or_404(product_id)
            if product and product.stock_quantity >= quantity:
                cart_list = session.get('cart', [])
                found = False

                for item in cart_list:
                    if item['product_name'] == product.product_name:
                        item['quantity'] += quantity
                        found = True
                        break
                if not found:
                    selected_items = {
                        'product_id': product.product_id,
                        'product_name': product.product_name,
                        'price': int(product.price),
                        'quantity': int(quantity)
                    }
                    cart_list.append(selected_items)
                session['cart'] = cart_list

                flash(f'Added {quantity} {product.product_name}(s) to your cart!', 'success')

                return redirect(url_for('store'))
            else:
                flash(f'Not enough stock available for {product.product_name}.', 'danger')
        else:
            print("Form validation failed")

    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    session['orders'] = total_quantity
    return render_template('shop.html', active_page='shop', products=all_products, total_quantity=total_quantity, form=form, current_year=current_year)


@app.route('/about')
def about():
    current_year = datetime.now().year

    orders = session.get('orders')
    return render_template('about.html', active_page='about', total_quantity=orders, current_year=current_year)

@app.route('/contact', methods=["POST", "GET"])
def contact():
    current_year = datetime.now().year
    print("Request method:", request.method)
    orders = session.get('orders')
    if request.method == "POST":
        name = request.form["name"]
        contact_number = request.form["contact_number"]
        message = request.form["message"]
        contact_form = {
            "name": name,
            "contact": contact_number,
            "message": message
        }
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=GOOGLE_KEY)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs="onids1312@gmail.com",
                msg=f"Subject: Customer Query{name}\n\nContact Number: {contact_number}\n{message}"
            )
        print(contact_form)

    return render_template('contact.html', active_page='contact', total_quantity=orders, current_year=current_year)

@app.route('/cart')
def cart():
    current_year = datetime.now().year

    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, total_quantity=total_quantity, current_year=current_year)

@app.route('/checkout', methods=["POST", "GET"])
def check_out():
    current_year = datetime.now().year

    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    if not cart_items:
        flash('Your cart is empty. Please add items to your cart before checking out.', 'danger')
        return redirect(url_for('cart'))

    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        address = request.form["address"] + " " + request.form['address2']
        baranggay = request.form["baranggay"]
        city = request.form["city"]
        payment_method = request.form["paymentMethod"]
        name_cc = request.form["cc-name"]
        cc_number = request.form["cc-number"]
        cc_expiration = request.form["cc-expiration"]
        cc_cvv = request.form["cc-cvv"]

        payment_details = {
            "customer details": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "address": address,
                "baranggay": baranggay,
                "city": city,
            },
            "card details": {
                "payment_method": payment_method,
                "name": name_cc,
                "number": cc_number,
                "expiration": cc_expiration,
                "CVV": cc_cvv,
            }
        }
        order_details = {
            "Items": cart_items,
            "Total": total_price
        }
        print(payment_details)
        print(order_details)
        for items in order_details["Items"]:
            result = ProductList.query.get_or_404(items["product_id"])
            new_stocks = result.stock_quantity - items["quantity"]
            result.stock_quantity = new_stocks
        db.session.commit()
        session.clear()
        return redirect('order_success')
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price, total_quantity=total_quantity, current_year=current_year)


@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<product_name>', methods=['POST'])
def remove_from_cart(product_name):
    cart_items = session.get('cart', [])
    updated_cart = [item for item in cart_items if item['product_name'] != product_name]
    session['cart'] = updated_cart
    return redirect(url_for('cart'))

@app.route('/order_success')
def order_success():
    current_year = datetime.now().year

    return render_template('order_success.html', current_year=current_year)

@app.route('/delete_product/<prod_id>', methods=['POST'])
def del_product(prod_id):
    prod_id = prod_id
    product_delete = ProductList.query.get_or_404(prod_id)
    db.session.delete(product_delete)
    db.session.commit()
    return redirect(url_for('admin'))

@admin_only
@app.route('/edit_product/<prod_id>', methods=['GET', 'POST'])
def edit_product(prod_id):
    current_year = datetime.now().year
    product = ProductList.query.get_or_404(prod_id)
    form = ProductForm()

    print("Request method:", request.method)

    if form.validate_on_submit():
        print('Handling POST request')
        product.product_name = form.product_name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock_quantity = form.stock_quantity.data
        product.img_url = form.img_url.data

        db.session.commit()
        print('Product updated successfully')

        return redirect(url_for('admin'))

    # For GET request, populate the form with existing product data
    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.description.data = product.description
        form.price.data = product.price
        form.stock_quantity.data = product.stock_quantity
        form.img_url.data = product.img_url

    return render_template('edit_prod.html', form=form, current_year=current_year)


@admin_only
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    current_year = datetime.now().year
    form = ProductForm()
    if form.validate_on_submit():
        print('Handling POST request')
        new_product = ProductList(
            product_name=form.product_name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('add_prod.html', form=form, current_year=current_year)


if __name__ == "__main__":
    app.run(debug=True)