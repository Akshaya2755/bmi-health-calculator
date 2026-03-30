from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# -------------------------
# MODELS
# -------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    bmi = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------
# ROUTES
# -------------------------

@app.route('/')
def home():
    return render_template('home.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# BMI CALCULATOR
@app.route('/bmi', methods=['GET', 'POST'])
@login_required
def bmi():
    bmi = None
    category = ""
    tip = ""
    color = "white"

    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
            tip = "Eat more nutritious food."
            color = "lightblue"

        elif bmi < 25:
            category = "Normal"
            tip = "Keep maintaining your lifestyle."
            color = "lightgreen"

        elif bmi < 30:
            category = "Overweight"
            tip = "Exercise regularly."
            color = "orange"

        else:
            category = "Obese"
            tip = "Consult a doctor and improve lifestyle."
            color = "red"

        # SAVE RECORD
        record = BMIRecord(
           height=height,
           weight=weight,
           bmi=bmi,
           category=category,
           user_id=current_user.id   
        )

    return render_template('bmi.html', bmi=bmi, category=category, tip=tip, color=color)


# HISTORY
@app.route('/history')
@login_required
def history():
    records = BMIRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', records=records)


# PROFILE
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


# EDIT PROFILE
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']

        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=current_user)


# -------------------------
# RUN
# -------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)