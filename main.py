from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, func
import smtplib
import os
from dotenv import load_dotenv

#ENVIRONMENTAL VARIABLES
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = Flask(__name__)
app.secret_key = SECRET_KEY

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

class Cafe(Base):
    __tablename__ = "cafes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String, nullable=False)
    detail: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reviews = relationship("Review", back_populates="cafe", cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe_id: Mapped[int] = mapped_column(Integer, ForeignKey("cafes.id"), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    cafe = relationship("Cafe", back_populates="reviews")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", user= current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", user= current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/')
def index():
    cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=cafes, user=current_user)

@app.route('/edit/<int:cafe_id>', methods=["GET", "POST"])
@login_required
def edit_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if request.method == "POST":
        cafe.name = request.form["name"]
        cafe.location = request.form["location"]
        cafe.img_url = request.form["img_url"]
        cafe.coffee_price = request.form["coffee_price"]
        cafe.detail = request.form["detail"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", cafe=cafe, user = current_user)

@app.route('/add', methods=["GET", "POST"])
@login_required
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form["name"],
            location=request.form["location"],
            img_url=request.form["img_url"],
            coffee_price=request.form["coffee_price"],
            detail=request.form["detail"],
            rating=0.0  # Default rating
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html", user=current_user)


@app.route('/user_add', methods=['GET','POST'])
def user_add_cafe():
    if request.method == "POST":
            name=request.form["name"],
            location=request.form["location"],
            img_url=request.form["img_url"],
            coffee_price=request.form["coffee_price"],
            detail=request.form["detail"],
            rating=0.0

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
                connection.starttls()
                connection.login(user= EMAIL_USER, password= EMAIL_PASS)
                connection.sendmail(
                    from_addr=EMAIL_USER,
                    to_addrs=EMAIL_USER,
                    msg=f'''Subject: New Cafe Addition Request\n\n
                    A user has requested to add a new cafe:
                    
                    Name: {name}
                    Location: {location}
                    Image URL: {img_url}
                    Coffee Price: {coffee_price}
                    Details: {detail}
                    Rating: {rating}
''')
            return redirect(url_for("index"))
    return render_template("user_add.html", user=current_user)


@app.route('/review/<int:cafe_id>', methods=["GET", "POST"])
def review_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if request.method == "POST":
        new_review = Review(
            cafe_id=cafe_id,
            rating=float(request.form["rating"])
        )
        db.session.add(new_review)
        db.session.commit()

        # Update average rating
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.cafe_id == cafe_id).scalar()
        cafe.rating = round(avg_rating, 1)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("review.html", cafe=cafe, user= current_user)

@app.route('/delete/<int:cafe_id>', methods=['GET','POST'])
def delete(cafe_id):
    cafe_to_delete = db.session.get(Cafe, cafe_id)

    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
