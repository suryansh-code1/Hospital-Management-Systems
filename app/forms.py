from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, DateField, TimeField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    email_or_username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PatientRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female'),('Other','Other')], validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')


class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    specialization_id = SelectField('Specialization', coerce=int, validators=[DataRequired()])
    is_active = BooleanField('Active')
    password = PasswordField('Password (set/reset)', validators=[Optional()])
    submit = SubmitField('Save')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save')


class AppointmentForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Book')


class TreatmentForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', validators=[Optional()])
    prescription = TextAreaField('Prescription', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Treatment')
