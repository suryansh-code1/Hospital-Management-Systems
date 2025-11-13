from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from ..utils import role_required
from ..models import Doctor, Patient, Department, Appointment
from ..forms import DoctorForm, DepartmentForm
from .. import db

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    counts = {
        'doctors': Doctor.query.count(),
        'patients': Patient.query.count(),
        'appointments': Appointment.query.count(),
    }
    latest_appts = Appointment.query.order_by(Appointment.id.desc()).limit(10).all()
    return render_template('admin/dashboard.html', counts=counts, latest_appts=latest_appts)


@admin_bp.route('/doctors')
@login_required
@role_required('admin')
def doctors():
    docs = Doctor.query.all()
    return render_template('admin/doctors.html', doctors=docs)


@admin_bp.route('/add_doctor', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_doctor():
    form = DoctorForm()
    form.specialization_id.choices = [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    if form.validate_on_submit():
        if Doctor.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already exists', 'warning')
            return redirect(url_for('admin.add_doctor'))
        doc = Doctor(
            name=form.name.data,
            email=form.email.data.lower(),
            specialization_id=form.specialization_id.data,
            is_active=form.is_active.data,
            password_hash=generate_password_hash(form.password.data if form.password.data else 'doctor123')
        )
        db.session.add(doc)
        db.session.commit()
        flash('Doctor created', 'success')
        return redirect(url_for('admin.doctors'))
    return render_template('admin/doctor_form.html', form=form, action='Add')


@admin_bp.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_doctor(doctor_id):
    doc = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=doc)
    form.specialization_id.choices = [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    if form.validate_on_submit():
        doc.name = form.name.data
        doc.email = form.email.data.lower()
        doc.specialization_id = form.specialization_id.data
        doc.is_active = form.is_active.data
        if form.password.data:
            doc.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Doctor updated', 'success')
        return redirect(url_for('admin.doctors'))
    return render_template('admin/doctor_form.html', form=form, action='Edit')


@admin_bp.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_doctor(doctor_id):
    doc = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doc)
    db.session.commit()
    flash('Doctor deleted', 'info')
    return redirect(url_for('admin.doctors'))


@admin_bp.route('/departments', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department(name=form.name.data, description=form.description.data)
        db.session.add(dept)
        db.session.commit()
        flash('Department saved', 'success')
        return redirect(url_for('admin.departments'))
    depts = Department.query.order_by(Department.name).all()
    return render_template('admin/departments.html', form=form, departments=depts)


@admin_bp.route('/appointments')
@login_required
@role_required('admin')
def appointments():
    appts = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('admin/appointments.html', appointments=appts)


@admin_bp.route('/search')
@login_required
@role_required('admin')
def search():
    q = request.args.get('q', '').strip()
    doctors = []
    patients = []
    if q:
        doctors = Doctor.query.filter(Doctor.name.ilike(f"%{q}%")).all()
        patients = Patient.query.filter(Patient.name.ilike(f"%{q}%")).all()
    return render_template('admin/search.html', q=q, doctors=doctors, patients=patients)
