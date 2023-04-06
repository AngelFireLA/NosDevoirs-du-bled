from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, ValidationError


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


class UpvoteForm(FlaskForm):
    submit = SubmitField()


class UploadForm(FlaskForm):
    classes = ["1 G-B"]
    matieres = ["Français", "Histoire Géographie", "Espagnol", "Anglais", "Sport", "ES Physique", "ES Maths", "ES Svt"]
    profs = ["MARCHINI", "MALPELLI", "CABARCOS", "MUSSI", "RIGAUX", "BRUNINI", "AVENOSO", "CASTELLO", "CHAPUIS", "MURACCIOLES", "ROMEO"]
    title = StringField('Titre', validators=[DataRequired()])
    content = StringField('Contenu', validators=[DataRequired()])
    file = FileField('file', validators=[])

    due_date = DateField('Date Limite', format='%d-%m-%Y')
    teacher = SelectField('Professeur', choices=profs)
    subject = SelectField('Matière', choices=matieres)
    classe = SelectField('Classe', choices=classes)
    submit = SubmitField('Envoyer')

