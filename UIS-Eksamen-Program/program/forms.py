from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class regionForm(FlaskForm):
    sourceRegions = SelectField('Region:' , choices=[], coerce = str, validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetRegion = SelectField('Stores:', choices=[])
   

class VolunteerLoginForm(FlaskForm):
    id = IntegerField('Volunteer ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CoordinatorLoginForm(FlaskForm):
    id = IntegerField('Coordinator ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class scalaForm(FlaskForm):
    sourceRegions = SelectField('Region:' , choices=[], coerce = str, validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetScales = SelectField('Stores and their scales:', choices=[], coerce = str)

class contactinfoForm(FlaskForm):
    sourceRegions = SelectField('Region:' , choices=[], coerce = str, validators=[DataRequired()])
    targetRegion = SelectField('Stores:', choices=[], coerce = str)
    #sourceShop = StringField('Enter shop ID', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetInfo = StringField('Contract info: ')

class scalaForm(FlaskForm):
    sourceRegions = SelectField('Region:' , choices=[], coerce = str, validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetScales = SelectField('Scales:', choices=[], coerce = str)

class setScalaForm(FlaskForm):
    sourceShop = SelectField('Select new scala:', choices=[], coerce = int, validators=[DataRequired()])
    sourceScala = SelectField('Select new scala:', choices=[], coerce = int, validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetScala = StringField('New scala:')

class setFirstShiftForm(FlaskForm):
    sourceShop = SelectField('Stores:', choices=[], coerce = str, validators=[DataRequired()])
    sourceFirstShift = StringField('How many first shifts?:', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetFirstShift = StringField('New value:')

class AdjustAccountForm(FlaskForm):
    sourcePassword = StringField('Enter old Password')
    targetPassword = StringField('Enter new Password')
    submit = SubmitField('Confirm')

class setWeekdayForm(FlaskForm):
    sourceShop = SelectField('Stores:', choices=[], coerce = str, validators=[DataRequired()])
    sourceWeekday = SelectField('Which weekday?:', choices=[], coerce = str, validators=[DataRequired()])
    submit = SubmitField('Confirm')
    targetWeekday = StringField('New value:')

class harProgramForm(FlaskForm):
    sourceRegions = SelectField('Region:' , choices=[], coerce = str)
    sourceShop = SelectField('Stores:', choices=[], coerce = str)
    sourceVal = SelectField('Which value?:', choices=[], coerce = str)
    submit = SubmitField('Confirm')
    checker = StringField('Current Status: ')
    targetHarProgram = StringField('Update:')

class storeDataForm(FlaskForm):
    targetWeekday = SelectField('Current Weekday:' , choices=[], coerce = str)
    targetFirstShift = SelectField('Current First Shift:' , choices=[], coerce = str)
    targetScala = SelectField('Current scala:' , choices=[], coerce = str)