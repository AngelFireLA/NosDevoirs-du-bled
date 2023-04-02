from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import app, db
from models import forms
from models.homework import Homework

@app.route('/homework', methods=['GET', 'POST'])
def homework():
    homework_list = Homework.query.all()
    form = forms.UpvoteForm()
    return render_template('homework.html', homework_list=homework_list, form=form)

@app.route('/upvote_homework/<int:homework_id>', methods=['POST'])
@login_required
def upvote_homework(homework_id):
    homework = Homework.query.get(homework_id)
    homework.upvotes += 1
    db.session.commit()
    return redirect(url_for('homework'))

@app.route('/upload')
def upload():
    return render_template('upload.html')



