from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nile_hospital.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

# migrate = Migrate(app,db)

class User(db.Model, SerializerMixin):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(220), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String, nullable = False)
    

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 8 characters.')
        return password
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Email is not valid. It must contain '@'.")
        return email
    
class Patient(db.Model,SerializerMixin):
    
    __tablename__ = "patients"    
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    gender = db.Column(db.String(100))
    address = db.Column(db.String(300))
    
    
    
    # One to many relationship with appointments
    appointments = db.relationship('Appointment',back_populates="patient",cascade='all, delete-orphan')
    
    # Many-to-many relationship with Doctor through Appointment
    doctors = db.relationship('Doctor', secondary='appointments', back_populates="patients")
    
    
    
    
    
class Doctor(db.Model,SerializerMixin):
    
    __tablename__ = "doctors"    
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(220), unique=True, nullable=False)
    speciality = db.Column(db.String(300))
    gender = db.Column(db.String(100))
    image_url = db.Column(db.String)
    
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"),nullable=False)
    
    # One to many relationship with appointments
    appointments = db.relationship('Appointment',back_populates="doctor",cascade='all, delete-orphan')
    
    department = db.relationship("Department", back_populates="doctors")
    
    # Many to many relationship with patients
    patients = db.relationship('Patient', secondary='appointments', back_populates="doctors")

class Appointment(db.Model,SerializerMixin):
    
    __tablename__ = "appointments"
    
    id = db.Column(db.Integer, primary_key = True)
    appointment_date = db.Column(db.Date,nullable=False)
    type_of_appointment = db.Column(db.String,nullable=False) 
    
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"),nullable = False) 
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"),nullable = False) 
    
    # Relationship between appointment with patient and doctor
    
    patient = db.relationship('Patient', back_populates="appointments")
    doctor = db.relationship('Doctor', back_populates="appointments")
    
    
class Department(db.Model,SerializerMixin):
    
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False) 
    number_of_doctors = db.Column(db.Integer)
    
    # One to many relationship with doctors
    doctors = db.relationship("Doctor",back_populates="department",cascade="all, delete-orphan")   
       
    
    

