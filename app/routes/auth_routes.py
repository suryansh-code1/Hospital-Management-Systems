from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..forms import LoginForm, PatientRegisterForm
from ..models import Admin, Doctor, Patient
from .. import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email_or_username.data.strip().lower()
        password = form.password.data

        # Try Admin (by username)
        admin = Admin.query.filter(Admin.username.ilike(identifier)).first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        # Try Doctor/Patient (by email)
        doctor = Doctor.query.filter(Doctor.email.ilike(identifier)).first()
        if doctor and check_password_hash(doctor.password_hash, password):
            login_user(doctor)
            return redirect(url_for('doctor.dashboard'))

        patient = Patient.query.filter(Patient.email.ilike(identifier)).first()
        if patient and check_password_hash(patient.password_hash, password):
            login_user(patient)
            return redirect(url_for('patient.dashboard'))

        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = PatientRegisterForm()
    if form.validate_on_submit():
        if Patient.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.register'))
        patient = Patient(
            name=form.name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            gender=form.gender.data,
            age=form.age.data,
            address=form.address.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(patient)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
