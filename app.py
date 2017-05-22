from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask_movie'
app.debug = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

app.add_url_rule('/users/<id>', methods=['GET', 'PUT', 'DELETE'])

@app.route('/')
def index():
    myUser = User.query.all()
    oneItem = User.query.filter_by(username="cat").first()
    return render_template('index.html', myUser=myUser, oneItem=oneItem)

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

@app.route('/update/<id>', methods=['POST'])
def update(id):
    user = User.query.filter_by(id=id).first()
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
