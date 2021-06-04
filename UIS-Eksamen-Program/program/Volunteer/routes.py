from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask.helpers import total_seconds
from numpy.lib.utils import source
from program import app, con, bcrypt
from program.forms import AdjustAccountForm, setWeekdayForm, regionForm, setScalaForm, setFirstShiftForm, scalaForm, harProgramForm, storeDataForm
from flask_login import current_user
from program.sqllibrary import Volunteer, getWeekdayV, getFirstShiftV,changePassword, checkPassword,getScalaV, findStoresV, updateScale, getName, updateFirstshift, updateWeekday

Volunteer = Blueprint('Volunteer', __name__)

@Volunteer.route("/setscala", methods = ['GET', 'POST'])
def setScala():
    ID = current_user.get_id()
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    form = setScalaForm()
    Shop = findStoresV(ID)
    form.sourceShop.choices = Shop
    drp_scale = []
    for i in range(1,11):
        drp_scale.append(i)
    form.sourceScala.choices = drp_scale
    if form.validate_on_submit():
        storeToUpdate = form.sourceShop.data
        print("StoreID: {}".format(storeToUpdate))
        newScale = form.sourceScala.data
        print("New Scala: {}".format(newScale))
        updateScale(newScale, storeToUpdate)
        storeName = getName(storeToUpdate)
        toScreen = str(storeName[0]) + ' has been updated with a scala of ' + str(newScale)
        form.targetScala.data = toScreen
        flash('Update succeed!', 'success')
    return render_template('setScala.html', form = form)

@Volunteer.route("/storeData", methods = ['GET', 'POST'])
def storeData():
    ID = current_user.get_id()
    if not current_user.is_authenticated or ID == 6000:
        flash('Your are the Coordinator, you are not connected to a specific store','Success')
        return redirect(url_for('Login.login'))
    form = storeDataForm()
    Weekday = getWeekdayV(ID)
    form.targetWeekday.choices = Weekday
    firstShifts = getFirstShiftV(ID)
    form.targetFirstShift.choices = firstShifts
    scala = getScalaV(ID)
    form.targetScala.choices = scala
    return render_template('storeData.html', form = form)

@Volunteer.route("/setfirstshift", methods = ['GET', 'POST'])
def setFirstShift():
    ID = current_user.get_id()
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    form = setFirstShiftForm()
    Shop = findStoresV(ID)
    form.sourceShop.choices = Shop
    FirstShift = form.sourceFirstShift.data 
    if form.validate_on_submit():
        storeToUpdate = form.sourceShop.data
        print("StoreID: {}".format(storeToUpdate))
        print("First shifts amount: {}".format(FirstShift))
        updateFirstshift(FirstShift, storeToUpdate)
        storeName = getName(storeToUpdate)
        toScreen = str(storeName[0]) + ' has been updated with ' + str(FirstShift) + ' of first shifts'
        form.targetFirstShift.data = toScreen
        flash('Update succeed!', 'success')
    return render_template('setFirstshift.html', form = form)

@Volunteer.route("/Setweekday", methods = ['GET', 'POST'])
def setWeekday():
    ID = current_user.get_id()
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    form = setWeekdayForm()
    Shop = findStoresV(ID)
    form.sourceShop.choices = Shop
    drp_weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    form.sourceWeekday.choices = drp_weekday
    Weekday = form.sourceWeekday.data 
    if form.validate_on_submit():
        storeToUpdate = form.sourceShop.data
        print("StoreID: {}".format(storeToUpdate))
        print("New weekday {}".format(Weekday))
        updateWeekday(Weekday, storeToUpdate)
        storeName = getName(storeToUpdate)
        toScreen = str(storeName[0]) + ' has been updated with ' + str(Weekday) + ' as the new weekday'
        form.targetWeekday.data = toScreen
        flash('Update succeed!', 'success')
    return render_template('setWeekday.html', form = form)




