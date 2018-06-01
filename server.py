from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_mail import Mail, Message

import subprocess

app = Flask(__name__)
Bootstrap(app)
mail = Mail(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'


def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(), Email(message="Bad Email")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5), AnyOf(['secret', 'password'])])


class AjaxForm(Form):
    repo_url = StringField('repourl', validators=[InputRequired()])

class EmailForm(Form):
    repo_url = StringField('repourl', validators=[InputRequired()])
    email_id = StringField('emailid', validators=[InputRequired()])


@app.route('/', methods=['GET'])
def index():
    # return render_template('index.html')
    # form = AjaxForm()
    # if form.validate_on_submit():
    #     return "Form submitted successfully!"

    # return render_template("ajax.html", form=form)
    return render_template("base.html")


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    form = AjaxForm()
    # if form.validate_on_submit():
    #     return "Form submitted successfully!"

    return render_template("ajax.html", form=form)


@app.route('/healthcheck', methods=['POST'])
def healthcheck():
    print(request)
    repo_url = request.form['url']
    subprocess_cmd('cd /tmp; git clone {}'.format(repo_url))
    op = subprocess_cmd('source /tmp/req_venv/bin/activate; cd /tmp/tenacity/tenacity; pep257')
    print("output from healthcheck --> {}".format(op))

    # return jsonify({"url" : url})
    return jsonify({"op" : str(op)})

@app.route('/coverage', methods=['POST'])
def coverage():
    test = request.form['test']

    return jsonify({"text" : test})

@app.route('/unittest', methods=['POST'])
def unittest():
    test = request.form['test']

    return jsonify({"text" : test})

@app.route('/email', methods=['GET', 'POST'])
def email():
    form = EmailForm()
    if form.validate():
        return 'form submitted successfully!'
    return render_template("email.html", form=form)




if __name__ == "__main__":
    app.run(debug=True)