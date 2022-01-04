from flask import Blueprint
from flask import Blueprint, render_template,send_file, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .WifiDB import WifiDB
import json

Wifi_DB = WifiDB()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/favicon.ico')
def favicon():
    return send_file("templates/favicon.png", mimetype='image/png')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, capturedlist = Wifi_DB.captured, BSSIDDict = Wifi_DB.BSSIDDict)

@main.route('/wifimap')
@login_required
def wifimap():
    return render_template('map.html', name=current_user.name, capturedlist = Wifi_DB.captured, BSSIDDict = Wifi_DB.BSSIDDict)

@main.route('/wifimapcracked')
@login_required
def wifimapcracked():
    return render_template('mapcracked.html', name=current_user.name, capturedlist = Wifi_DB.captured, BSSIDDict = Wifi_DB.BSSIDDict)

@main.route('/api/data')
@login_required
def data():
    return Wifi_DB.getJSONDictLocation()

@main.route('/api/datacracked')
@login_required
def datacracked():
    return Wifi_DB.getJSONDictAllKnown()

@main.route('/update', methods=['POST'])
@login_required
def update():
    Wifi_DB.initialise()
    flash('Update Ready')
    return redirect(url_for('main.profile'))

