from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL
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



@app.route('/')
def home():

    return render_template('index.html', active_page='home')

@app.route('/store', methods=["GET", "POST"])
def store():
    result = db.session.execute(db.select(ProductList))
    all_products = result.scalars()

    form = AddToCartForm()
    if form.validate_on_submit():
        product_id = int(request.form['product_id'])
        quantity = form.quantity.data

        product = db.get_or_404(ProductList, product_id)
        print(product)
        if product and product.stock_quantity >= quantity:
            # Update stock quantity
            product.stock_quantity -= quantity
            db.session.commit()

            # Add item to session cart
            if 'cart' not in session:
                session['cart'] = {}
            if product_id in session['cart']:
                session['cart'][product_id]['quantity'] += quantity
            else:
                session['cart'][product_id] = {
                    'product_name': product.product_name,
                    'price': product.price,
                    'quantity': quantity
                }

            flash(f'Added {quantity} {product.product_name} to your cart!', 'success')
            return redirect(url_for('store'))

        else:
            flash(f'Not enough stock available for {product.product_name}.', 'danger')

    return render_template('shop.html', active_page='shop', products=all_products, form=form)

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for product_id, item in session['cart'].items():
            total_price += item['price'] * item['quantity']
            cart_items.append({
                'product_id': product_id,
                'product_name': item['product_name'],
                'price': item['price'],
                'quantity': item['quantity']
            })

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


if __name__ == "__main__":
    app.run(debug=True)