import os, json

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_codemirror import CodeMirror

from editor import Editor
from helpers import *

from datetime import datetime, timedelta

SECRET_KEY = os.urandom(32)
CODEMIRROR_LANGUAGES = ['python', 'html']
CODEMIRROR_THEME = 'material'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'r') as f:
    users = json.load(f)
    f.close()

with open(os.path.join(os.path.dirname(__file__), "db", "assignments.json"), 'r') as f:
    assignments = json.load(f)

    
with open(os.path.join(os.path.dirname(__file__), "db", "classrooms.json"), 'r') as f:
    classrooms = json.load(f)
    f.close()

def add_minutes(username, minutes):
    user = users.get(username)
    if user:
        user['daily_minutes'] = user.get('daily_minutes', 0) + minutes
        with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'w') as f:
            json.dump(users, f, indent=4)

@app.route('/')
def main():
    return render_template('index.html', user = session.get('user',''))

@app.route('/editor', methods = ['GET', 'POST'])
def editor():
    form = Editor()
    if form.validate_on_submit():
        text = form.source_code.data
        username = session.get('user', '')
        if username:
            add_minutes(username, 10)
    return render_template('editor.html', form=form, user = session.get('user',''))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (validate_login(username, password, users)):
            session['user'] = username
            
            user = users[username]
            today = datetime.today().date()
            last_active_str = user.get('last_active')
            last_active = datetime.strptime(last_active_str, "%Y-%m-%d").date() if last_active_str else None
             # Only count streak if student worked >=30 min today
            if user.get('daily_minutes', 0) >= 30:
                if last_active == today - timedelta(days=1):
                    user['streak'] = user.get('streak', 0) + 1
                elif last_active != today:
                    user['streak'] = 1  # reset streak if missed a day

                # Update total minutes and days worked
                user['total_minutes'] = user.get('total_minutes', 0) + user['daily_minutes']
                user['days_worked'] = user.get('days_worked', 0) + 1

            # Reset daily minutes for today
            user['daily_minutes'] = 0
            user['last_active'] = today.strftime("%Y-%m-%d")

            # Save users.json
            with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'w') as f:
                json.dump(users, f, indent=4)

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

    # Build list of classroom dicts for template
    detailed_classes = []
    for cname in user_classes:
        classroom_info = classrooms.get(cname, {})
        assignments = classroom_info.get("assignments", [])
        detailed_classes.append({
            "name": cname,        # key used in template as c.name
            "assignments": assignments
        })

    return render_template('profile.html',
                           user=username,
                           classrooms=detailed_classes)

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

@app.route('/classroom/<classname>')
def classroom_page(classname):
    classroom_info = classrooms.get(classname)
    if not classroom_info:
        flash("Classroom not found.", "danger")
        return redirect(url_for('profile'))

    # Build detailed assignment list
    
    with open(os.path.join(os.path.dirname(__file__), "db", "assignments.json"), 'r') as f:
        assignments = json.load(f)
    assignment_list = []
    for aid in classroom_info.get("assignments", []):
        if str(aid) in assignments:
            assignment_list.append(assignments[str(aid)])

    return render_template(
        'classroom.html',
        classname=classname,
        assignments=assignment_list,
        user=session.get('user','')
    )

@app.route('/assignment/<int:aid>')
def assignment_page(aid):
    aid_str = str(aid)
    if aid_str not in assignments:
        flash("Assignment not found.", "danger")
        return redirect(url_for('profile'))

    a = assignments[aid_str]

    # Render appropriate workspace
    if a["type"] == "math":
        return render_template("workspace_math.html",
                               assignment=a,
                               user=session.get('user',''))

    elif a["type"] == "cs":
        return render_template("workspace_cs.html",
                               assignment=a,
                               user=session.get('user',''))

    else:
        flash("Invalid assignment type.", "danger")
        return redirect(url_for('profile'))


@app.route('/streaks')
def streaks():
    username = session.get('user', '')
    user_info = users.get(username, {})
    user_classes = user_info.get('classrooms', [])

    class_streaks = {}
    for cname in user_classes:
        class_users = classrooms.get(cname, {}).get('students', [])
        streak_data = []
        for u in class_users:
            udata = users.get(u, {})
            streak = udata.get('streak', 0)
            days = udata.get('days_worked', 1)  # avoid division by zero
            total_minutes = udata.get('total_minutes', 0)
            avg_minutes = total_minutes / days if days > 0 else 0

            streak_data.append({
                'username': u,
                'streak': streak,
                'avg_minutes': avg_minutes
            })

        # Sort: first by streak descending, then by avg_minutes descending
        streak_data.sort(key=lambda x: (-x['streak'], -x['avg_minutes']))
        class_streaks[cname] = streak_data

    return render_template('streaks.html', user=username, class_streaks=class_streaks)


if __name__ == '__main__':
    app.run(debug=True)
    