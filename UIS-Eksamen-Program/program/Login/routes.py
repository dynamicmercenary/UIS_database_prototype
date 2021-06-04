from types import MethodType
from flask import render_template, url_for, flash, redirect, request, Blueprint
from program import app, con, bcrypt
from program.forms import CoordinatorLoginForm, VolunteerLoginForm, AdjustAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from program.sqllibrary import select_Volunteer, select_Coordinator, changePassword, checkPassword,checkPasswordC, changePasswordC

Login = Blueprint('Login', __name__)

posts = [{}]

@Login.route("/")
@Login.route("/home")
def home():
    return render_template('home.html', posts=posts)

@Login.route("/about")
def about():
    return render_template('about.html', title='About')

@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    is_coordinator = True if request.args.get('is_coordinator') == 'true' else False
    print(is_coordinator)
    form = CoordinatorLoginForm() if is_coordinator else VolunteerLoginForm()
    print(form)
    if form.validate_on_submit():
        user = select_Coordinator(form.id.data) if is_coordinator else select_Volunteer(form.id.data)
        if user != None and bcrypt.check_password_hash(user[2], form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Volunteer.storeData'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')
    return render_template('login.html', title='Login', is_coordinator=is_coordinator, form=form)

@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.home'))

@Login.route("/account", methods = ['GET', 'POST'])
def account():
    ID = current_user.get_id()
    user = current_user
    if not current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = AdjustAccountForm()
    print(ID)
    if form.validate_on_submit():
        oldPassword = bcrypt.generate_password_hash(form.sourcePassword.data).decode('utf-8')
        if not ID == 6000:
            if bcrypt.check_password_hash(user[2], form.sourcePassword.data):
                hashed_password = bcrypt.generate_password_hash(form.targetPassword.data).decode('utf-8')
                newPassword=hashed_password
                changePassword(ID, newPassword)
                flash('Password has been changed', 'success')
                return redirect(url_for('Login.account'))
            else: 
                flash('Something went wrong, please doublecheck', 'danger')
                return redirect(url_for('Login.account'))
        elif ID == 6000:
            if  bcrypt.check_password_hash(user[2], form.sourcePassword.data):
                hashed_password = bcrypt.generate_password_hash(form.targetPassword.data).decode('utf-8')
                newPassword=hashed_password
                changePasswordC(ID, newPassword)
                flash('Password has been changed', 'success')
                return redirect(url_for('Login.account'))
            else: 
                flash('Something went wrong, please doublecheck', 'danger')
                return redirect(url_for('Login.account'))
        else: 
            flash('Something went wrong, please doublecheck', 'danger')
            return redirect(url_for('Login.account'))
    return render_template('account.html', title='Account', form = form)