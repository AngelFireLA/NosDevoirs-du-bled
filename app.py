import io

from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user, login_required
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, session, send_file, abort

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False)
    status = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, unique=True)
    content = db.Column(db.String(2000))
    due_date = db.Column(db.String(50))
    teacher = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    class_id = db.Column(db.String(100))
    user_id = db.Column(db.String(200))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #homework_id is the id of the homework it answers
    homework_id = db.Column(db.Integer)
    title = db.Column(db.String(200), index=True, unique=True)
    content = db.Column(db.String(2000))
    user_id = db.Column(db.String(200))
    due_date = db.Column(db.String(50))
    file_data = db.Column(db.LargeBinary, nullable=True)
    file_name = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()


@app.route('/homeworks/', defaults={'homework_id': None, 'answer_id': None}, methods=['GET'])
@app.route('/homeworks/<int:homework_id>/', defaults={'answer_id': None}, methods=['GET'])
@app.route('/homeworks/<int:homework_id>/<int:answer_id>', methods=['GET'])
def homeworks(homework_id=None, answer_id=None):
    if homework_id:
        homework = Homework.query.get(int(homework_id))
        answers = Answer.query.filter_by(homework_id=homework_id).all()
        if homework:
            if answer_id:
                answer = Answer.query.get(int(answer_id))
                if answer:
                    return render_template('answer.html', homework=homework, ans=answer)
                else:
                    session.pop('_flashes', None)
                    flash('Answer not found.')
                    return redirect(url_for('homeworks')+str(homework_id))

            else:
                return render_template('homework_answers.html', homework=homework, answers=answers)
        else:
            session.pop('_flashes', None)
            flash('Homework not found.')
            return redirect(url_for('homeworks'))
    else:
        homework_list = Homework.query.all()
        return render_template('homeworks.html', homework_list=homework_list)

def change_user_status(email, status):
    user = User.query.filter_by(email=email).first()
    if user is None:
        print(f"User with email '{email}' not found.")
        return

    user.status = status
    db.session.commit()
    print(f"User with email '{email}' status changed to '{status}'.")



@app.route('/envoyer_devoir', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.status == "admin":
        abort(403)
    form = UploadHomeworkForm()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        due_date = request.form['due_date']
        teacher = request.form['teacher']
        subject = request.form['subject']
        class_id = request.form['classe']

        # check if there is already a homework with the same title
        existing_homework = Homework.query.filter_by(title=title).first()
        if existing_homework:
            session.pop('_flashes', None)
            flash('Un devoir avec le même titre existe déja', 'error')
            return redirect(url_for('upload_error'))
        if not current_user:
            homework = Homework(title=title, content=content, due_date=due_date, teacher=teacher,
                            subject=subject, class_id=class_id)
        else:
            homework = Homework(title=title, content=content, due_date=due_date, teacher=teacher,
                                subject=subject, class_id=class_id, user_id=current_user.username)
            current_user.username
        db.session.add(homework)
        db.session.commit()
        session.pop('_flashes', None)
        flash('Devoir envoyé correctement.', 'success')
        return redirect(url_for('homeworks'))
    else:
        return render_template('upload_hw.html', form=form)


@app.route('/envoyer_reponse/<int:homework_id>', methods=['GET', 'POST'])
@login_required
def upload_answer(homework_id):
    homework = Homework.query.filter_by(id=homework_id).first()
    if not homework:
        flash("L'identifiant de devoir est invalide, veuillez ne pas toucher à l'identifiant de l'url la prochaine fois.")
        return redirect(url_for('home'))
    if not current_user.status == "admin":
        abort(403)
    form = UploadAnswerForm()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        due_date = homework.due_date
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_data = file.read()
            # Check if file exists and is less than or equal to 1 MB
            if len(file_data) > 1024 * 1024 * 5:
                session.pop('_flashes', None)
                flash('Le fichier ne doit pas faire plus de 5 mo.', 'error')
                return redirect(url_for('upload_error'))
            # Check if file type is allowed
            allowed_extensions = ['txt', 'odt', 'docx', '.txt', '.odt', '.docx']
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in allowed_extensions:
                session.pop('_flashes', None)
                flash('Type de fichier non autorisé: txt, odt, docx', 'error')
                return redirect(url_for('upload_error'))
        else:
            filename = None
            file_data = None

        # check if there is already an answer with the same title for this homework
        existing_answer = Answer.query.filter_by(homework_id=homework_id, title=title).first()
        if existing_answer:
            session.pop('_flashes', None)
            flash('Une réponse avec le même titre existe déjà pour ce devoir', 'error')
            return redirect(url_for('upload_error'))

        # create a new answer object
        answer = Answer(homework_id=homework_id, title=title, content=content, user_id=current_user.username,
                        due_date=due_date,
                        file_data=file_data, file_name=filename)
        db.session.add(answer)
        db.session.commit()

        session.pop('_flashes', None)
        flash('Réponse envoyée avec succès', 'success')
        return redirect(url_for('homeworks') + str(homework_id))

    else:
        return render_template('upload_answer.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session.pop('_flashes', None)
        flash('Vous avez bien été enregistré!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_or_username.data).first()
        if user is None or not user.check_password(form.password.data):
            session.pop('_flashes', None)
            flash('Email ou mot de passe invalide.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    session.pop('_flashes', None)
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            user = User.query.filter_by(id=current_user.id).first()
            if user.email != form.email.data and User.query.filter_by(email=form.email.data).first():
                session.pop('_flashes', None)
                flash('Cet email est déja utilisée.')
            else:
                user.email = form.email.data
                user.username = form.name.data
                db.session.commit()
                return redirect(url_for('profile'))
        else:
            session.pop('_flashes', None)
            flash('Mot de passe incorrect.')
    return render_template('profile.html', form=form, current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('Vous avez été déconnecté.')
    return redirect(url_for('login'))

@app.route('/upload_error')
def upload_error():
    return render_template('upload_error.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/download_file/<int:answer_id>')
def download_file(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    file_data = answer.file_data
    response = make_response(file_data)
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(answer.file_name)
    return response

class RegistrationForm(FlaskForm):
    name = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField("S'inscrire")



class LoginForm(FlaskForm):
    email_or_username = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')


class UpdateProfileForm(FlaskForm):
    name = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Entrer le mot de passe pour confirmer les changements.', validators=[DataRequired()])
    submit = SubmitField('Sauvegarder les changements.')

class UploadHomeworkForm(FlaskForm):
    classes = ["1 G-B"]
    matieres = ["Français", "Histoire Géographie", "Espagnol", "Anglais", "Sport", "ES Physique", "ES Maths", "ES Svt"]
    profs = ["MARCHINI", "MALPELLI", "CABARCOS", "MUSSI", "RIGAUX", "BRUNINI", "AVENOSO", "CASTELLO", "CHAPUIS", "MURACCIOLES", "ROMEO"]
    title = StringField('Titre', validators=[DataRequired()])
    content = StringField('Contenu', validators=[DataRequired()])
    due_date = DateField('Date Limite', format='%d-%m-%Y')
    teacher = SelectField('Professeur', choices=profs)
    subject = SelectField('Matière', choices=matieres)
    classe = SelectField('Classe', choices=classes)
    submit = SubmitField('Envoyer')


class UploadAnswerForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = StringField('Contenu', validators=[DataRequired()])
    file = FileField('file', validators=[])
    submit = SubmitField('Envoyer')

if __name__ == "__main__":
    start = input("Waiting for command : ")
    if start == "start":
        app.run()
    else:
        with app.app_context():
            exec('change_user_status("lysandre@mail.com", "admin")')
