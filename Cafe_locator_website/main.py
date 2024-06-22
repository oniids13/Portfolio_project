from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_loc = StringField('Location', validators=[DataRequired()])
    seats = StringField('No. of Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[URL()])
    img_url = StringField('Image URL', validators=[URL()])
    has_toilet = BooleanField("Toilet")
    has_wifi = BooleanField('Wifi')
    has_sockets = BooleanField('Sockets')
    can_take_calls = BooleanField('Can take calls inside')
    submit = SubmitField()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cafe")
def cafe():
    result = db.session.execute(db.Select(Cafe))
    cafes = result.scalars().all()
    return render_template("cafe.html", cafes=cafes)

@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe_name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.cafe_loc.data,
            has_sockets=bool(form.has_sockets.data),
            has_toilet=bool(form.has_toilet.data),
            has_wifi=bool(form.has_wifi.data),
            can_take_calls=bool(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=f"₱{int(form.coffee_price.data)}"
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafe'))
    return render_template("add_cafe.html", form=form)






if __name__ == '__main__':
    app.run(debug=True)