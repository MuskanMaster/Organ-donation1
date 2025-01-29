from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
# Configure the SQLite database (set it to use 'donations.db' file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    medical_condition_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    donor = db.relationship('Donor', backref='user', uselist=False)
    receiver = db.relationship('Receiver', backref='user', uselist=False)
    contact_us = db.relationship('ContactUs', backref='user')
    
    def _repr_(self):
        return f'<User {self.name}>'

# Define the Signup model
class Signup(db.Model):
    signup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='signup', uselist=False)

    def _repr_(self):
        return f'<Signup {self.username}>'

# Define the Login model
class Login(db.Model):
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def _repr_(self):
        return f'<Login {self.username}>'

# Define the Donor model
class Donor(db.Model):
    donor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    organisation = db.Column(db.String(100))
    phone_no = db.Column(db.String(15))
    medical_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='donor', uselist=False)

    def _repr_(self):
        return f'<Donor {self.name}>'

# Define the Receiver model
class Receiver(db.Model):
    receiver_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    organisation = db.Column(db.String(100))
    phone_no = db.Column(db.String(15))
    medical_condition_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='receiver', uselist=False)

    def _repr_(self):
        return f'<Receiver {self.name}>'

# Define the Contact Us model
class ContactUs(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='contact_us')

    def _repr_(self):
        return f'<ContactUs {self.name}>'

# Define the Donation Request model
class DonationRequest(db.Model):
    donation_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.donor_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.receiver_id'))
    request_message = db.Column(db.Text)

    donor = db.relationship('Donor', backref='donation_requests')
    receiver = db.relationship('Receiver', backref='donation_requests')

    def _repr_(self):
        return f'<DonationRequest {self.donation_request_id}>'

# Initialize the database
with app.app_context():
    db.create_all()


# Routes for main pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/forget')
def forget():
    return render_template('forget.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.route('/donor')
def donor():
    return render_template('donor.html')

@app.route('/receiver')
def receiver():
    return render_template('receiver.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Routes for specific organ donation pages
@app.route('/eye')
def eye():
    return render_template('eye.html')

@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/kidney')
def kidney():
    return render_template('kidney.html')

@app.route('/liver')
def liver():
    return render_template('liver.html')

@app.route('/lung')
def lung():
    return render_template('lung.html')

@app.route('/instestine')
def instestine():
    return render_template('instestine.html')

if __name__ == '__main__':
    app.run(debug=True)
