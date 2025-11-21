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


@app.route('/')
def main():
    return render_template('index.html', user=session.get('user',''))


@app.route('/editor', methods=['GET','POST'])
def editor():
    form = Editor()
    if form.validate_on_submit():
        text = form.source_code.data
    return render_template('editor.html', form=form, user=session.get('user',''))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if validate_login(username, password, users):
            session['user'] = username
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
    return render_template('profile.html', user=session.get('user',''))


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


if __name__ == '__main__':
    app.run(debug=True)
