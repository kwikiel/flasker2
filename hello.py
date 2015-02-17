from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.bootstrap import Bootstrap
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cykuvhibjhvkucjx'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)
toolbar=DebugToolbarExtension(app)


class Post(db.Model):
    __tablename__ ='posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    post_body = db.Column(db.String(2048), unique=False)
   

    def __repr__(self):
        return '<Post %r>' % self.name

class NameForm(Form):
    name = StringField('What is your name? ', validators=[Required()])
    post_name = StringField('What is your favourite color?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    names = Post.query.all()
    form = NameForm() #This things lives in template?
    if form.validate_on_submit():
        name_input = form.name.data
        post_msg = form.post_name.data
        form.name.data = ''
        form.post_name.data=''
        msg = Post(name=name_input, post_body=post_msg) #Magic
        db.session.add(msg)
        db.session.commit()
        flash('Saved to website')
    else:
        return render_template('index.html',form=form, name=names)
    return render_template('index.html', form=form, name=names)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0") #prod
    #manager.run()
