from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csaekk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    video_filename = db.Column(db.String(100), nullable=False)
    listing_type = db.Column(db.String(10), nullable=False)  # 'rent' or 'sell'
    city_type = db.Column(db.String(50), nullable=True)
    area = db.Column(db.String(100), nullable=True)
    specifications = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(150), db.ForeignKey('user.username'), nullable=False)

# Forms
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField('Login')

# Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if username exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        # Check if email exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        # Create new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    listings = Listing.query.filter_by(username=current_user.username).all()
    return render_template('profile.html', user=current_user, listings=listings)

@app.route('/rentals', methods=['GET'])
@login_required
def rentals():
    listings = Listing.query.all()
    return render_template('rentals.html', listings=listings)

@app.route('/design')
@login_required
def design():
    return render_template('design.html')

@app.route('/submit_listing', methods=['POST'])
@login_required
def submit_listing():
    price = request.form.get('price')
    contact_name = request.form.get('contact_name')
    contact_phone = request.form.get('contact_phone')
    video_file = request.files.get('video')
    listing_type = request.form.get('listing_type')
    city_type = request.form.get('city_type')
    area = request.form.get('area')
    specifications = request.form.get('specifications', '')

    if not all([price, contact_name, contact_phone, video_file, listing_type]):
        flash('All fields are required.', 'danger')
        return redirect(url_for('profile'))

    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join('static/videos', video_filename)
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    video_file.save(video_path)

    new_listing = Listing(
        price=price, contact_name=contact_name, contact_phone=contact_phone,
        video_filename=video_filename, listing_type=listing_type, city_type=city_type,
        area=area, specifications=specifications, username=current_user.username
    )
    db.session.add(new_listing)
    db.session.commit()
    flash('Listing submitted successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/delete_listing/<int:listing_id>', methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.username != current_user.username:
        flash('You do not have permission to delete this listing.', 'danger')
        return redirect(url_for('profile'))

    db.session.delete(listing)
    db.session.commit()
    flash('Listing deleted successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/search_rentals', methods=['POST'])
@login_required
def search_rentals():
    data = request.get_json()

    # Extract filters from the request
    budget = int(data.get('budget', 0))
    city_type = data.get('city_type', '').strip()
    listing_type = data.get('listing_type', '').strip().lower()  # Rent or Sell

    # Build the query
    query = Listing.query.filter(Listing.price <= budget)
    if city_type:
        query = query.filter(Listing.city_type == city_type)
    if listing_type in ['rent', 'sell']:
        query = query.filter(Listing.listing_type == listing_type)  # Correctly filter by listing type

    # Execute query and return results
    listings = query.all()
    return jsonify(listings=[
        {
            "listing_type": listing.listing_type,
            "price": listing.price,
            "contact_name": listing.contact_name,
            "contact_phone": listing.contact_phone,
            "video_filename": listing.video_filename,
            "city_type": listing.city_type,
            "area": listing.area,
            "specifications": listing.specifications,
        } for listing in listings
    ])




# Initialize database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
