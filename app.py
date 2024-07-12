from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zorin:1234@localhost/notes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '86bf24b30959a323bfcd899fee6606d6'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    new_note = Note(user_id=session['user_id'], content=content)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    note = Note.query.get(note_id)
    if note.user_id == session['user_id']:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete_profile')
def delete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)
    return redirect(url_for('register'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
