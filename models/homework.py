from app import db

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