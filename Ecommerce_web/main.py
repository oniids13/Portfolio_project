from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
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






@app.route('/')
def home():

    return render_template('index.html', active_page='home')

@app.route('/store')
def store():
    result = db.session.execute(db.select(ProductList))
    all_products = result.scalars()
    return render_template('shop.html', active_page='shop', products=all_products)

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')




if __name__ == "__main__":
    app.run(debug=True)