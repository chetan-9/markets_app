from market import app
from flask import render_template, redirect, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/markets', methods=['GET', 'POST'])
@login_required
def markets():
    '''
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 700},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 200}
    ]
    return render_template('markets.html', items=items)
    '''

    purchaseform = PurchaseItemForm()
    sellform = SellItemForm()
    if request.method == 'POST':
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f'Congratulations you purchases item {p_item_obj.name}', category='success')
            else:
                flash(f'You do not have enough money to purchase {p_item_obj.name}', category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_obj = Item.query.filter_by(name=sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f'Congratulations you sold item {s_item_obj.name}', category='success')
            else:
                flash(f'You do not have item {s_item_obj.name} to sell', category='danger')

        return redirect('/markets')

    if request.method == 'GET':
        #items = Item.query.all()
        items = Item.query.filter_by(owner_id=None)
        owned_items = Item.query.filter_by(owner_id=current_user.id)
        return render_template('markets.html', items=items, purchaseform=purchaseform, owned_items=owned_items, sellform=sellform)


@app.route('/')
@login_required
def homepage():
    return render_template('homepage.html')


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully. You are now logged in as {user_to_create.username}', category='success')
        return redirect('/markets')
    if form.errors:
        for err in form.errors.values():
            flash(f'There was an error creating account: {err}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exist and if exists if password is matching
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success, you logged in as {attempted_user.username}',category='success')
            return redirect('/markets')
        else:
            flash(f'Username and Password does not match. Please try again.',category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect('/markets')






