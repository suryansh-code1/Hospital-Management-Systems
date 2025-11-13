from flask_login import UserMixin
from . import db
from sqlalchemy import UniqueConstraint
from datetime import date, time


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def role(self):
        return "admin"

    def get_id(self):
        return f"admin:{self.id}"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors = db.relationship('Doctor', backref='specialization', lazy=True)


class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    availability_json = db.Column(db.Text, default='{}')
    is_active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    @property
    def role(self):
        return "doctor"

    def get_id(self):
        return f"doctor:{self.id}"


class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    address = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    @property
    def role(self):
        return "patient"

    def get_id(self):
        return f"patient:{self.id}"


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked')  # Booked/Completed/Cancelled

    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

    __table_args__ = (
        UniqueConstraint('doctor_id', 'date', 'time', name='uix_doctor_datetime'),
    )


class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), unique=True, nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
