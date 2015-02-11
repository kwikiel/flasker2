from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.bootstrap import Bootstrap
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cykuvhibjhvkucjx'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
manager=Manager(app)

class Post(db.Model):
    __tablename__ ='posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return '<Post %r>' % self.name

class NameForm(Form):
    name = StringField('What is your name? ', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    names = Post.query.all()
    form = NameForm() #This things lives in template?
    if form.validate_on_submit():
        name_input = form.name.data
        form.name.data = ''
        msg = Post(name=name_input) #Magic
        db.session.add(msg)
        db.session.commit()
    else:
        return render_template('index.html',form=form, name=names)
    return render_template('index.html', form=form, name=names)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(500):
    def internal_server_error(e):
        return render_template('500.html'),500
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
