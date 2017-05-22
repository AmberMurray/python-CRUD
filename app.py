from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask import jsonify
from flask import Response
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask_movie'
app.debug = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    #initializes the User object
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    myUser = User.query.all()
    return render_template('index.html', myUser=myUser)

@app.route('/add')
def add():
    return render_template('add_user.html')

@app.route('/profile/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()
    return render_template('profile.html', user=user)

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    user = User.query.filter_by(id=id).first()
    return render_template('update.html', user=user)

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    formInfo = User(request.form['username'], request.form['email'])
    user = User.query.filter_by(id=id).first()
    user.username = formInfo.username
    user.email = formInfo.email
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index.html'))


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
