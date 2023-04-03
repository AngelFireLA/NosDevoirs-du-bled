
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import forms
from flask_login import current_user, login_user, logout_user, login_required
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, url_for





app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"  #

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, unique=True)
    content = db.Column(db.String(2000))
    due_date = db.Column(db.String(50))
    teacher = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    class_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upvotes = db.Column(db.Integer, default=0)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

with app.app_context():
    db.create_all()


@app.route('/homework', methods=['GET', 'POST'])
def homework():
    homework_list = Homework.query.all()
    print(homework_list)
    form = forms.UpvoteForm()
    return render_template('homework.html', homework_list=homework_list, form=form)

@app.route('/upvote_homework/<int:homework_id>', methods=['POST'])
@login_required
def upvote_homework(homework_id):
    homework = Homework.query.get(homework_id)
    homework.upvotes += 1
    db.session.commit()
    return redirect(url_for('homework'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        due_date = request.form['due_date']
        teacher = request.form['teacher']
        subject = request.form['subject']
        class_id = request.form['class']

        # check if there is already a homework with the same title
        existing_homework = Homework.query.filter_by(title=title).first()
        if existing_homework:
            return redirect(url_for('upload_error'))

        homework = Homework(title=title, content=content, due_date=due_date, teacher=teacher,
                            subject=subject, class_id=class_id)
        db.session.add(homework)
        db.session.commit()
        return redirect(url_for('homework'))
    else:
        return render_template('upload.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_or_username.data).first()
        if user is None:
            user = User.query.filter_by(username=form.email_or_username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.UpdateProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.email = form.email.data
            current_user.username = form.name.data
            db.session.commit()
            flash('Profile updated')
            return redirect(url_for('profile'))
        else:
            flash('Incorrect password')
    return render_template('profile.html', form=form, current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/upload_error')
def upload_error():
    return render_template('upload_error.html')
if __name__ == "__main__":
    app.run()
