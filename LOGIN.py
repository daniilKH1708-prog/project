from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# =========================
# SETTINGS
# =========================

app.secret_key = "my_secret_key"

# Основная база — пользователи
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///C:/Users/kharc/PyCharmMiscProject/users.db"
)

# Дополнительная база — товары
app.config["SQLALCHEMY_BINDS"] = {
    "products": "sqlite:///C:/Users/kharc/PyCharmMiscProject/project.db"
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"

    user = db.Column(
        db.String(100),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )




class Product(db.Model):
    __bind_key__ = "products"
    __tablename__ = "project"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.String(255)
    )

    category = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    rating = db.Column(
        db.Float
    )



@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")


        user = Users.query.filter_by(
            user=username
        ).first()

        if user and user.password == password:

            session["username"] = user.user

            return redirect("/products")

        return render_template(
            "login.html",
            error="Wrong username or password"
        )

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Проверяем пользователя в users.db
        existing_user = Users.query.filter_by(
            user=username
        ).first()

        if existing_user:

            return render_template(
                "register.html",
                error="Такой пользователь уже существует"
            )

        # Создаём пользователя
        new_user = Users(
            user=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        session["username"] = username

        return redirect("/products")

    return render_template("register.html")


# =========================
# PRODUCTS
# =========================

@app.route("/products")
def products():

    if "username" not in session:
        return redirect("/login")

    # Получаем товары из project.db
    all_products = Product.query.all()

    return render_template(
        "products.html",
        products=all_products,
        username=session["username"]
    )

@app.route("/product/<int:product_id>")
def product_details(product_id):


    product = Product.query.get_or_404(product_id)

    return render_template(
        "product_details.html",
        product=product
    )
# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# START
# =========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()


    app.run(debug=True)