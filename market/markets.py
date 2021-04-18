'''
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
'''

'''
class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=100), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
'''



''''
@app.route('/markets')
def markets():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 700},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 200}
    ]
    return render_template('markets.html', items=items)

@app.route('/')
def homepage():
    return render_template('homepage.html')
    
'''

'''
if __name__ == '__main__':
    app.run(debug=True)
'''
