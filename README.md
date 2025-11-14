Spectra – A Socratic STEM Classroom Platform
1. Problem

AI tools now give students answers instantly, which makes assignments seem easier while quietly weakening real learning—especially in math, computer science, and physics. Teachers have no visibility into how students use AI, what steps they attempted, or where they get stuck. Existing classroom platforms (Google Classroom, Khan Academy, etc.) do not integrate AI in a way that reinforces learning through inquiry instead of answer-giving.

Spectra solves this by offering a Socratic AI tutor that guides with questions, not solutions, while giving teachers visibility into student reasoning.

2. Solution Overview

Spectra is a lightweight, classroom-oriented web app designed for STEM learning. It combines:

• A teacher dashboard for assignments and student monitoring
• A LaTeX math editor and simple in-browser coding area
• A Socratic AI assistant that refuses to give answers directly
• Basic user accounts with login, roles, and session tracking
• A minimal database suitable for fast prototyping

Everything is designed to fit within a 2-week development window.

3. Key Features (Built for a Demo)
User Accounts & Login System

• Simple email + password login
• Three roles: admin, teacher, student
• Session-based authentication (no OAuth required)
• Admins create teachers and classrooms; teachers enroll students

Database for demo can use:
• SQLite (single file, minimal setup) or
• JSON files for users, classes, assignments, and logs

Classrooms & Assignments

• Admins create classroom shells
• Teachers add students and create small assignments
• Problems can include math (LaTeX) or code prompts

Student Workspace

• Left side: math text area with LaTeX rendering OR a simple code textbox
• Right side: Socratic tutor chat
• AI only asks questions and guides steps (no direct answers unless enabled)
• Tracks steps like “Understand → Plan → Execute → Check”

Teacher Dashboard

• See student progress on each assignment
• View key stats: time on task, number of hints used, step completion
• View a transcript of the student’s interaction with the tutor
• Identify common misconceptions

Socratic AI Behavior

• AI asks guiding questions based on student input
• Only provides hints or conceptual guidance, not direct solutions
• Mode settings allow:

Full socratic (no answers ever)

Hints allowed

Exam mode (strict, no hints)

Anti-Shortcut Signals (Simple)

• Detects if student pastes long blocks of code or LaTeX
• Flags skipped steps
• Shows all AI/student messages to teachers

4. Education Plan (Demo-Ready)

Spectra is structured for classrooms, not individual use.

• Education Tier (prototype):
– Up to 30 student accounts
– One or more teachers per classroom
– Assignment creation, progress tracking, and transcript viewing

This plan is fully implemented in the demo version as basic classroom management.

5. Technology Stack
Backend

• Python + Flask
• SQLite or JSON files for data (keeps demo simple)
• Basic password hashing
• Routes for login, classes, assignments, sessions

Frontend

• HTML, CSS, Bootstrap, and JavaScript
• MathJax or KaTeX for LaTeX rendering
• Simple code input box (no full IDE needed for demo)
• Chat-style UI for Socratic tutor

AI / NLP

• Ollama for local model OR
• OpenAI API for high-quality reasoning
• Strict “Socratic mode” system prompt layer
• Thin wrapper that logs student-AI turns to database

6. Setup Instructions (Simple)

Create a virtual environment
py -m venv .venv

Install dependencies
pip install -r requirements.txt

Start Flask
py src/app.py

Navigate to the provided local URL to access:
• Login page
• Teacher dashboard
• Student workspace

7. Project Structure

src
– app.py
– templates (HTML pages)
– static (CSS, JS)
– data (SQLite DB or JSON files)
– utils (auth, database helpers)

(Exact structure can be adjusted easily during development.)

8. Team Members

• Siddharth Kakumanu – @FormulaCarbon
• Ansh Kapadia – @AnshVKapadia
• Aanya Kotla – @aak-222735
• Nikhil Verma – @socials-nick
• Sriprajnav Koduri – @pkoduri14

9. License

GNU GPLv3