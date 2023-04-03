from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email_or_username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password to Confirm Changes', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class UpvoteForm(FlaskForm):
    submit = SubmitField()

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
        field.data.seek(0)
    return file_length_check

class UploadForm(FlaskForm):
    classes = ["1 G-B"]
    matieres = ["Français", "Histoire Géographie", "Espagnol", "Anglais", "Sport", "Spé NSI", "Spé Maths", "Spé Physique", "ES Physique", "ES Maths", "ES Svt"]
    profs = ["MARCHINI", "MALPELLI", "CABARCOS", "MUSSI", "RIGAUX", "BRUNINI", "AVENOSO", "CASTELLO", "CHAPUIS", "MURACCIOLES"]
    title = StringField('Titre', validators=[DataRequired()])
    content = StringField('Contenu', validators=[DataRequired()])
    file = FileField('file', validators=[
        FileAllowed(['txt'], 'Text files only!'),
    ])

    due_date = DateField('Date Limite', format='%d-%m-%Y')
    teacher = SelectField('Professeur', choices=profs)
    subject = SelectField('Matière', choices=matieres)
    classe = SelectField('Classe', choices=classes)
    submit = SubmitField('Envoyer')

