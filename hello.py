from flask import Flask, render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cykuvhibjhvkucjx'
bootstrap = Bootstrap(app)


class NameForm(Form):
    name = StringField('What is your name? ', validators=[Required()])
    submit = StringField('Submit')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
