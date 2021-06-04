from flask import render_template, url_for, flash, redirect, request, Blueprint
from program import app, con, bcrypt
from program.forms import regionForm, scalaForm, contactinfoForm, harProgramForm
from flask_login import current_user
from program.sqllibrary import Coordinator, createUser, findStores, getRegions, getScala, deleteUser, getInfo, checkForProgram, deleteEntityHarProgram, updateHarProgramToTrue, getName

Coordinator = Blueprint('coordinator', __name__)

@Coordinator.route("/findstores", methods = ['GET', 'POST'])
def findStoresInRegion():
    ID = current_user.get_id()
    if not current_user.is_authenticated or not ID == 6000:
        flash('Please Login as Coordinator.','danger')
        return redirect(url_for('Login.login'))
    form = regionForm()
    sourceRegions = getRegions()
    drp_sourceRegions = []
    for drp_r in sourceRegions:
        drp_sourceRegions.append(drp_r[0])
    form.sourceRegions.choices = drp_sourceRegions
    print(drp_sourceRegions)
    region = form.sourceRegions.data
    dropdown_regions = findStores(region)
    drp_regions = []
    for drp in dropdown_regions:
        drp_regions.append((str(drp[0])+' '+ str(drp[1])))
        print(drp_regions)
    form.targetRegion.choices = drp_regions
    return render_template('findstores.html', form = form)

@Coordinator.route("/findscala", methods = ['GET', 'POST'])
def getScales():
    ID = current_user.get_id()
    if not current_user.is_authenticated or not ID == 6000:
        flash('Please Login as Coordinator.','danger')
        return redirect(url_for('Login.login'))
    form = scalaForm()
    sourceRegions = getRegions()
    drp_sourceRegions = []
    for drp_r in sourceRegions:
        drp_sourceRegions.append(drp_r[0])
    form.sourceRegions.choices = drp_sourceRegions
    print(drp_sourceRegions)
    region = form.sourceRegions.data
    dropdown_scales = getScala(region)
    drp_scales = []
    for drp in dropdown_scales:
        drp_scales.append((str(drp[1]) + ': ' +str(drp[0]) + ' with ' + str(drp[2]) + ' as weekday'))
        print(drp_scales)
    form.targetScales.choices = drp_scales
    return render_template('findscales.html', form = form)

@Coordinator.route("/findcontactinfo", methods = ['GET', 'POST'])
def getContactinfo():
    ID = current_user.get_id()
    if not current_user.is_authenticated or not ID == 6000:
        flash('Please Login as Coordinator.','danger')
        return redirect(url_for('Login.login'))
    form = contactinfoForm()
    sourceRegions = getRegions()
    drp_sourceRegions = []
    for drp_r in sourceRegions:
        drp_sourceRegions.append(drp_r[0])
    form.sourceRegions.choices = drp_sourceRegions
    print(drp_sourceRegions)
    region = form.sourceRegions.data
    dropdown_regions = findStores(region)
    drp_regions = []
    for drp in dropdown_regions:
        drp_regions.append((drp[0], str(drp[0])+' '+ str(drp[1])))
        print(drp_regions)
    form.targetRegion.choices = drp_regions
    bID = form.targetRegion.data
    if form.validate_on_submit():
        InfoShop = getInfo(bID)
        toScreen = 'Store: ' + InfoShop[0] + ' - Email: ' + InfoShop[1] + ' - Phone: ' + InfoShop[2]
        print(InfoShop)
        print(toScreen)
        form.targetInfo.data = toScreen

    return render_template('findcontactinfo.html', form = form)

@Coordinator.route("/UpdateHarProgram", methods = ['GET', 'POST'])
def UpdateHarProgram():
    ID = current_user.get_id()
    if not current_user.is_authenticated or not ID == 6000:
        flash('Please Login as Coordinator.','danger')
        return redirect(url_for('Login.login'))
    form = harProgramForm()
    sourceRegions = getRegions()
    drp_sourceRegions = []
    for drp_r in sourceRegions:
        drp_sourceRegions.append(drp_r[0])
    form.sourceRegions.choices = drp_sourceRegions
    print(drp_sourceRegions)
    region = form.sourceRegions.data
    dropdown_regions = findStores(region)
    drp_shops = []
    for drp in dropdown_regions:
        drp_shops.append((drp[0], drp[1]))
    print(drp_shops)
    form.sourceShop.choices = drp_shops
    boolVals = ['True', 'False']
    form.sourceVal.choices = boolVals
    if form.validate_on_submit():
        storeToUpdate = form.sourceShop.data
        print("StoreID: {}".format(storeToUpdate))
        updateBool = form.sourceVal.data
        print("Bool: {}".format(updateBool))
        check = checkForProgram(storeToUpdate)
        print(check)
        if (updateBool == 'True' and check):
            toScreen = "Store already has program"
            form.targetHarProgram.data = toScreen
            return render_template('updateHarProgram.html', form = form)
        elif (updateBool == 'False' and check):
            storeName = getName(storeToUpdate)
            deleteEntityHarProgram(storeToUpdate)
            deleteUser(storeToUpdate)
            checkdelete = checkForProgram(storeToUpdate)
            print(checkdelete)
            toScreen = 'Program has been removed from ' + str(storeName[0])
            form.targetHarProgram.data = toScreen
            return render_template('updateHarProgram.html', form = form)
        elif (updateBool == 'True' and not check):
            storeName = getName(storeToUpdate)
            updateHarProgramToTrue(updateBool, storeToUpdate)
            createUser(storeToUpdate, storeName)
            checkcreate = checkForProgram(storeToUpdate)
            print(checkcreate)
            toScreen = str(storeName[0]) + ' has been updated with ' + str(updateBool) + ' to indicate program'
            form.targetHarProgram.data = toScreen
            flash('Update succeed!', 'success')
        else:
            storeName = getName(storeToUpdate)
            toScreen = str(storeName[0]) + ' does not have a program yet'
            form.targetHarProgram.data = toScreen
            return render_template('updateHarProgram.html', form = form)
    return render_template('updateHarProgram.html', form = form)
