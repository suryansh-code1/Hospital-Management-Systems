from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..utils import role_required
from ..models import Appointment, Treatment
from ..forms import TreatmentForm
from .. import db
from datetime import date


doctor_bp = Blueprint('doctor', __name__, template_folder='../templates/doctor')


@doctor_bp.route('/dashboard')
@login_required
@role_required('doctor')
def dashboard():
    today = date.today()
    appts = Appointment.query.filter_by(doctor_id=current_user.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('doctor/dashboard.html', appointments=appts, today=today)


@doctor_bp.route('/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def appointment_detail(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.doctor_id != current_user.id:
        flash('Unauthorized appointment access', 'danger')
        return redirect(url_for('doctor.dashboard'))
    form = TreatmentForm(obj=appt.treatment)
    if form.validate_on_submit():
        if not appt.treatment:
            appt.treatment = Treatment(appointment_id=appt.id)
        appt.treatment.diagnosis = form.diagnosis.data
        appt.treatment.prescription = form.prescription.data
        appt.treatment.notes = form.notes.data
        appt.status = request.form.get('status', appt.status)
        db.session.commit()
        flash('Treatment updated', 'success')
        return redirect(url_for('doctor.dashboard'))
    return render_template('doctor/appointment_detail.html', appointment=appt, form=form)
