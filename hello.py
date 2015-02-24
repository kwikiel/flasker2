from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required
from flask.ext.bootstrap import Bootstrap
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.jsontools import jsonapi
from sqlalchemy.ext.declarative import declarative_base
import chartkick



Base = declarative_base()

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=chartkick.js(), static_url_path='/static')
app.config['SECRET_KEY'] = 'cykuvhibjhvkucjx'
app.jinja_env.add_extension("chartkick.ext.charts")
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


class Measure(db.Model):
    __tablename__ = 'measures'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    def __repr__(self):
        return '%r' % self.value

class WeirdForm(Form):
    measure =IntegerField('Reasult from measurment? ', validators=[Required()])
    submit = SubmitField('Submit')


class NameForm(Form):
    name = StringField('What is your name? ', validators=[Required()])
    post_name = StringField('What is your favourite color?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/measure', methods=['GET','POST'])
def measure():
    form = WeirdForm()
    wholedata = Measure.query.all()
    if form.validate_on_submit():
        current_value = form.measure.data
        current = Measure(value=current_value)
        form.measure.data = ''
        db.session.add(current)
        db.session.commit()
        return redirect(url_for('charts'))
    return render_template('data_input.html', form=form, msu=wholedata)

@app.route('/', methods=['GET','POST'])
def index():
    #Post.query.delete()
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
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=names)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/api/add_name/<name>')
def api_add(name):
    temp_data = Post(name=name, post_body='Added from api')
    db.session.add(temp_data)
    db.session.commit()
    return 'Added'

@app.route('/api/read/<id>')
def read_api(id):
    sauce = Post.query.all()
    return str(sauce[int(id)].name)

@app.route('/api/read/json')
def read_api_json():
    all_data = Post.query.all()
    return render_template('data.json', posts = all_data )

@app.route('/charts')
def charts():
    data = [('Sunday', 10), ('Monday', 27), ('Tuesday', 32), ('Wednesday', 42),('Thursday', 38), ('Friday', 45), ('Saturday', 52), ('Potato', 33)]
    data2 = Measure.query.all()
    return render_template('template.html', data=data2)

@app.route('/charts2')
def charts2():
    return render_template('charts.html')

@app.route('/chartkick')
def kickchart():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('charts3.html', data=data)

@app.route('/charts4')
def charts4(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('charts4.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0") #prod
    #manager.run()
