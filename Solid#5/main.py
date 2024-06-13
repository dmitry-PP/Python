from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import Markup
from _auth import auth,register
from consts import  error_message
from functions import *
from utils import get_type,get_status_estate,get_status_ad,get_time

app = Flask(__name__)
app.secret_key = 'secretkey'

#qaws!12fgT_09999hfgghGYUG#$
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET","POST"])
def register_user():
    if request.method == 'POST':
        password = request.form.get('password')

        public_key = register(password)
        if not public_key is None:
            return redirect(url_for('login',pubkey=public_key))
        flash(Markup(error_message),'danger')
    return render_template('register.html')

@app.route('/auth', methods=["GET","POST"])
def auth_user():
    if request.method == 'POST':
        public_key = request.form.get('public')
        password = request.form.get('password')

        if auth(public_key,password):
            return redirect(url_for('login',pubkey=public_key))
        flash(Markup("<b>Ошибка авторизации!</b>"),'danger')
    return render_template('auth.html')

@app.route('/login/<pubkey>')
def login(pubkey):
    return render_template('login.html', address=pubkey)

@app.route('/create_property', methods=["GET","POST"])
def create_property():
    address = request.args.get("address")
    if request.method == "POST":
        size = request.form.get('size')
        url = request.form.get('file')
        rooms = request.form.get('rooms')
        estate_type = request.form.get('estate_type')

        if createEstate(address, int(size), url,int(rooms), int(estate_type)):
            return redirect(url_for(f"login", pubkey=address))
    return render_template('create_property.html', address=address)

@app.route('/create_ad', methods=["GET","POST"])
def create_ad():
    address = request.args.get("address")
    estates_ids = map(lambda x:x[0],getEstates())
    if request.method == "POST":
        price = request.form.get('price')
        estate_id = request.form.get('estate_id')

        if createAd(address,int(estate_id),int(price)):
            return redirect(url_for(f"login", pubkey=address))
    return render_template('create_ad.html', address=address, ids=estates_ids)

@app.route('/change_ad', methods=["GET","POST"])
def change_ad():
    address = request.args.get("address")
    ads_ids = map(lambda x:x[0],enumerate(getAds()))
    if request.method == "POST":
        change_status = request.form.get('change_status')
        estate_id = request.form.get('estate_id')

        if updateAdStatus(address, int(estate_id), int(change_status)):
            return redirect(url_for(f"login", pubkey=address))
    return render_template('change_ad_status.html', address=address, ids=ads_ids)

@app.route('/change_property', methods=["GET","POST"])
def change_property():
    address = request.args.get("address")
    estates_ids = map(lambda x:x[0],getEstates())
    if request.method == "POST":
        change_status = request.form.get('change_status')
        estate_id = request.form.get('estate_id')

        if updateEstateStatus(address, int(estate_id), int(change_status)):
            return redirect(url_for(f"login", pubkey=address))
    return render_template('change_property_status.html', address=address, ids=estates_ids)

@app.route('/get_balance')
def get_balance():
    address = request.args.get("address")
    balance = getBalance(address)
    return render_template('get_balance.html', address=address, balance=balance)


@app.route('/withdraw', methods=["GET","POST"])
def withdraw():
    address = request.args.get("address")
    if request.method == "POST":
        amount = request.form.get('amount')
        if withDraw(address,int(amount)):
            return redirect(url_for(f"login",pubkey=address))
    return render_template('withdraw.html', address=address)

@app.route('/buy', methods=["GET","POST"])
def buy():
    address = request.args.get("address")
    ads_ids = map(lambda x: x[0], enumerate(getAds()))
    if request.method == "POST":
        price = request.form.get('price')
        ad_id = request.form.get('estate_id')

        if buyEstate(address, int(ad_id), int(price)):
            return redirect(url_for(f"login",pubkey=address))
    return render_template('buy.html', address=address,ids=ads_ids)

@app.route('/estates')
def get_estates():
    address = request.args.get("address")
    estates = getEstates()

    return render_template('get_properties.html', address=address, estates=estates,get_type=get_type,get_status=get_status_estate)

@app.route('/ads')
def get_ads():
    address = request.args.get("address")
    estates = enumerate(getAds())

    return render_template('get_ads.html', address=address, ads=estates,get_status=get_status_ad, get_time=get_time)



if __name__ == "__main__":
    app.run(debug=True)
    #w3.eth.wait_for_transaction_receipt(tx_hash)