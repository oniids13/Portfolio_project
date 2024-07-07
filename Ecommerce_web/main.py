from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from wtforms.validators import DataRequired, NumberRange
from flask_migrate import Migrate




app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)


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


with app.app_context():
    db.create_all()



class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Cart')


@app.route('/')
def home():
    orders = session.get('orders')
    return render_template('index.html', active_page='home', total_quantity=orders)


@app.route('/store', methods=["GET", "POST"])
def store():
    all_products = ProductList.query.all()
    form = AddToCartForm()

    if request.method == "POST":
        print("Form submitted")
        print(request.form)
        try:
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
        except ValueError:
            print("Invalid data type for product ID or quantity")
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
                        'product_name': product.product_name,
                        'price': int(product.price),
                        'quantity': int(quantity)
                    }
                    cart_list.append(selected_items)
                session['cart'] = cart_list

                flash(f'Added {quantity} {product.product_name}(s) to your cart!', 'success')
                print(f"Cart after adding product {product.product_name}: {session['cart']}")  # Debugging statement
                return redirect(url_for('store'))
            else:
                flash(f'Not enough stock available for {product.product_name}.', 'danger')
        else:
            print("Form validation failed")
            print(form.errors)  # Debugging statement
    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    session['orders'] = total_quantity
    return render_template('shop.html', active_page='shop', products=all_products, form=form, total_quantity=total_quantity)


@app.route('/about')
def about():
    orders = session.get('orders')
    return render_template('about.html', active_page='about', total_quantity=orders)

@app.route('/contact')
def contact():
    orders = session.get('orders')
    return render_template('contact.html', active_page='contact', total_quantity=orders)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, total_quantity=total_quantity)

@app.route('/checkout')
def check_out():
    cart_items = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    if not cart_items:
        flash('Your cart is empty. Please add items to your cart before checking out.', 'danger')
        return redirect(url_for('cart'))

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price, total_quantity=total_quantity)


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

if __name__ == "__main__":
    app.run(debug=True)