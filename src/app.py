import os

from flask import Flask, render_template
from flask_codemirror import CodeMirror

from editor import Editor

SECRET_KEY = os.urandom(32)
CODEMIRROR_LANGUAGES = ['python', 'html']
CODEMIRROR_THEME = 'material'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/editor', methods = ['GET', 'POST'])
def index():
    form = Editor()
    if form.validate_on_submit():
        text = form.source_code.data
    return render_template('editor.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)