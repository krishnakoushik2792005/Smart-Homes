from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)  # Add this line
    password = db.Column(db.String(200), nullable=False)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    contact_name = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    video_filename = db.Column(db.String(100), nullable=False)
    listing_type = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(50), nullable=True)  # Add this line for area if needed

