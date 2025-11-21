import os, json

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_codemirror import CodeMirror

from editor import Editor
from helpers import *

SECRET_KEY = os.urandom(32)
CODEMIRROR_LANGUAGES = ['python', 'html']
CODEMIRROR_THEME = 'material'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'r') as f:
    users = json.load(f)
    f.close()
    
with open(os.path.join(os.path.dirname(__file__), "db", "classrooms.json"), 'r') as f:
    classrooms = json.load(f)
    f.close()

@app.route('/')
def main():
    return render_template('index.html', user = session.get('user',''))

@app.route('/editor', methods = ['GET', 'POST'])
def editor():
    form = Editor()
    if form.validate_on_submit():
        text = form.source_code.data
    return render_template('editor.html', form=form, user = session.get('user',''))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (validate_login(username, password, users)):
            session['user'] = username
            
        else:
            flash("invalid username or password", "danger")
            print("invalid login")
            
        return redirect(url_for("main"))
    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (validate_new_user(username, password, users)):
            users[username] = { "password" : password }
            print("valid")
            
            with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'w') as f:
                json.dump(users, f)
                f.close()
        else:
            flash("invalid username or password", "danger")
            print("invalid sign up")
            
        return redirect(url_for("main"))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the username from session
    flash("You have been logged out.", "info")
    return redirect(url_for('main'))

@app.route('/profile')
def profile():
    username = session.get('user', '')
    user_info = users.get(username, {})
    user_classes = user_info.get("classrooms", [])

    return render_template('profile.html',
                           user=username,
                           classrooms=user_classes)

@app.route('/newclass', methods = ['GET', 'POST'])
@app.route('/newclass', methods=['GET', 'POST'])
def newclass():
    if request.method == "POST":
        cname = request.form.get('classname')
        students = request.form.get('students').split(', ')
        teachers = request.form.get('teachers').split(', ')
        admins = request.form.get('admins').split(', ')

        classrooms[cname] = {
            'students': students,
            'teachers': teachers,
            'admins': admins,
            'assignments': []
        }

        # Update each user's classroom list
        for uname in students + teachers + admins:
            if uname in users:
                users[uname].setdefault("classrooms", [])
                users[uname]["classrooms"].append(cname)

        # Save updated users.json and classrooms.json
        with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), "w") as f:
            json.dump(users, f, indent=4)
        with open(os.path.join(os.path.dirname(__file__), ".\\db\\classrooms.json"), "w") as f:
            json.dump(classrooms, f, indent=4)

    return render_template('newclass.html', user=session.get('user',''))

if __name__ == '__main__':
    app.run(debug=True)
    