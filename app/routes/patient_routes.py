from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from ..utils import role_required
from ..models import Appointment, Doctor, Department
from ..forms import AppointmentForm
from .. import db
from datetime import datetime


patient_bp = Blueprint('patient', __name__, template_folder='../templates/patient')


@patient_bp.route('/dashboard')
@login_required
@role_required('patient')
def dashboard():
    upcoming = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('patient/dashboard.html', appointments=upcoming)


@patient_bp.route('/book', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def book():
    form = AppointmentForm()
    form.doctor_id.choices = [(d.id, f"{d.name} ({d.specialization.name})") for d in Doctor.query.filter_by(is_active=True).all()]
    if form.validate_on_submit():
        appt = Appointment(
            doctor_id=form.doctor_id.data,
            patient_id=current_user.id,
            date=form.date.data,
            time=form.time.data,
            status='Booked'
        )
        db.session.add(appt)
        try:
            db.session.commit()
            flash('Appointment booked', 'success')
            return redirect(url_for('patient.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('Selected slot is already booked for the doctor. Choose another time.', 'danger')
    return render_template('patient/book.html', form=form)


@patient_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
@role_required('patient')
def cancel(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('patient.dashboard'))
    appt.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled', 'info')
    return redirect(url_for('patient.dashboard'))
