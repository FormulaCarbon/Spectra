import os, json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_codemirror import CodeMirror
from editor import Editor
from helpers import *
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from google import generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

from datetime import datetime, timedelta

SECRET_KEY = os.urandom(32)
CODEMIRROR_LANGUAGES = ['python', 'html']
CODEMIRROR_THEME = 'material'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

# Load users
with open(os.path.join(os.path.dirname(__file__), "./db/users.json"), 'r') as f:
    users = json.load(f)

# Load assignments
with open(os.path.join(os.path.dirname(__file__), "./db/assignments.json"), 'r') as f:
    assignments = json.load(f)

# Load classrooms
with open(os.path.join(os.path.dirname(__file__), "./db/classrooms.json"), 'r') as f:
    classrooms = json.load(f)


def add_minutes(username, minutes):
    user = users.get(username)
    if user:
        user['daily_minutes'] = user.get('daily_minutes', 0) + minutes
        with open(os.path.join(os.path.dirname(__file__), ".\\db\\users.json"), 'w') as f:
            json.dump(users, f, indent=4)

@app.route('/')
def main():
    return render_template('index.html', user=session.get('user',''))


@app.route('/editor', methods=['GET','POST'])
def editor():
    form = Editor()
    if form.validate_on_submit():
        text = form.source_code.data
        username = session.get('user', '')
        if username:
            add_minutes(username, 10)
    return render_template('editor.html', form=form, user = session.get('user',''))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if validate_login(username, password, users):
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

        return redirect(url_for("main"))

    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if validate_new_user(username, password, users):
            users[username] = {"password": password}

            with open(os.path.join(os.path.dirname(__file__), "./db/users.json"), 'w') as f:
                json.dump(users, f)
        else:
            flash("invalid username or password", "danger")

        return redirect(url_for("main"))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
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


@app.route('/classroom/<classname>')
def classroom_page(classname):
    if classname not in classrooms:
        return "Classroom not found", 404

    classroom = classrooms[classname]
    assignment_list = []

    for aid in classroom.get("assignments", []):
        aid_str = str(aid)
        if aid_str in assignments:
            assignment_list.append(assignments[aid_str])

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
        return "Assignment not found", 404

    a = assignments[aid_str]

    if a["type"] == "math":
        return render_template("workspace_math.html", assignment=a)
    if a["type"] == "cs":
        return render_template("workspace_code.html", assignment=a)


# ⭐ SOCratic AI Backend
@app.route('/tutor')
def tutor_page():
    return render_template("tutor.html", user=session.get('user',''))

@app.route('/tutor_api', methods=['POST'])
def tutor_api():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    SYSTEM_PROMPT = (
        "You are SpectraGuide, a Socratic tutoring assistant. "
        "You NEVER give direct answers. Instead you respond only with guiding "
        "questions that help the student think through the problem. "
        "Keep messages short, helpful, and focused on reasoning steps."
    )

    # Use the correct Gemini model
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # Build contents list in proper Gemini format
    contents = []

    # System prompt MUST be a model-role message
    contents.append({
        "role": "model",
        "parts": [SYSTEM_PROMPT]
    })

    # Add conversation history
    for msg in history:
        contents.append({
            "role": msg["role"],     # "user" or "model"
            "parts": [msg["content"]]
        })

    # Add new user message
    contents.append({
        "role": "user",
        "parts": [user_message]
    })

    try:
        # Generate content with the new Gemini API format
        response = model.generate_content(
            contents=contents
        )

        bot_reply = response.text

        # Wrap and return clean JSON
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"reply": "There was an error with the AI request."}), 500

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

@app.route('/newassignment/<classname>', methods=['GET', 'POST'])
def newassignment(classname):
    # Ensure classroom exists
    if classname not in classrooms:
        flash("Classroom not found.", "danger")
        return redirect(url_for('profile'))

    if request.method == "POST":
        title = request.form.get("title")
        problem = request.form.get("problem")
        question = request.form.get("question", "")
        atype = request.form.get("type")

        # Generate next assignment ID
        next_id = max([int(k) for k in assignments.keys()] + [0]) + 1

        # Create assignment object
        new_assignment = {
            "id": next_id,
            "title": title,
            "type": atype,
            "problem": problem,
            "question": question,
            "classroom": classname
        }

        assignments[str(next_id)] = new_assignment

        # Save assignments.json
        with open(os.path.join(os.path.dirname(__file__), "db", "assignments.json"), "w") as f:
            json.dump(assignments, f, indent=4)

        # Add assignment ID to classroom
        classrooms[classname]["assignments"].append(next_id)

        # Save classrooms.json
        with open(os.path.join(os.path.dirname(__file__), "db", "classrooms.json"), "w") as f:
            json.dump(classrooms, f, indent=4)

        flash("Assignment created!", "success")
        return redirect(url_for('classroom_page', classname=classname))

    return render_template("newassignment.html", classname=classname, user=session.get('user', ''))


if __name__ == '__main__':
    app.run(debug=True)
