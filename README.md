# Spectra - A Socratic Problem-Solving Tutor

## 1. Problem:
Most AI tools give students *answers* too quickly. That makes homework look easier in the moment but quietly destroys problem-solving skills and confidence. Students learn to copy solutions instead of learning how to think: breaking down problems, checking assumptions, and correcting their own reasoning. We need a tool that refuses to be a shortcut and instead *trains* the student’s thinking.

## 2. How (Technology):
Spectra is built from the ground up to act like a strict Socratic tutor: it guides with questions and hints, not full solutions (unless the student is truly stuck).

**Frontend:**  
- HTML, CSS, JavaScript  
- Simple “problem workspace”:
  - Left: problem input (text, screenshots transcribed, or pasted code/math)  
  - Right: chat-style dialogue showing the tutor’s questions and the student’s answers  
- Progress indicators:
  - Steps like *“Understand problem → Plan → Execute → Check”*  
  - Gentle badges like “You identified all givens” or “You tested an example case”

**Backend:**  
- Lightweight Flask server that:
  - Stores minimal session state (problem, step, student answers so far)
  - Enforces a **Socratic policy**: the model must ask questions first, not give solutions
  - Only reveals full or partial solutions after multiple failed attempts or explicit user request (“I’m stuck. Show me.”)

**NLP / LLM logic (pluggable):**  
- Uses an LLM with a strict system prompt to:
  - Classify the student’s current step (understanding, planning, executing, checking)
  - Generate **targeted questions** instead of answers
  - Decide when to escalate from “hint” → “outline of solution” → “full solution”
- Model options:
  - Local models via **Ollama** for low-cost experimentation
  - Cloud APIs such as **OpenAI** for higher quality and multi-domain reasoning (math, CS, physics, etc.)
  - Optional lightweight text processing (e.g., regex / simple heuristics) to detect when the student is just pasting the model’s own output back

**Example flow:**  
User pastes:  
> “Find the derivative of \( f(x) = x^3 - 3x^2 + 5 \).”

Spectra responds *not* with the derivative, but with questions like:  
- “What rule do we usually use to differentiate powers of x?”  
- “Can you differentiate just \( x^3 \) first?”  

Only after several exchanges, if the user is still stuck, Spectra may show a partial worked example.

## 3. Monetize:
Spectra can be offered as a freemium web app or browser-based learning companion:

**Free Tier:**
- Access to local / low-cost models (e.g., via Ollama)  
- Socratic tutoring for a limited number of problems per day  
- Basic progress tracking:
  - Recent problems
  - High-level tags (e.g., “calculus,” “loops,” “arrays,” “kinematics”)

**Premium Tier ($10/month):**
- Access to higher-accuracy cloud models (e.g., OpenAI)  
- Multi-domain & multi-step support:
  - Math (algebra → calculus)
  - Intro CS (Python, C++, Java, JavaScript)
  - Physics / other STEM word problems  
- Advanced learning analytics:
  - “Weak concept” map (e.g., chain rule, loop boundaries, absolute value)  
  - Session summaries with what the student did well and what to review  
- “Exam Mode”:
  - Strict hint throttling and no solutions until the end
  - Exportable session logs to share with teachers/tutors

**Education Tier ($50/month):** 
- Supports an educational environment allowing administrators to add up to 30 student accounts
- Teachers can assess growth, track student's time commitment, and assign specific practices

## Team Members
- **Siddharth Kakumanu** - GitHub: @FormulaCarbon  
- **Ansh Kapadia** - GitHub: @AnshVKapadia  
- **Aanya Kotla** - Github: @aak-222735  
- **Nikhil Verma** - Github: @socials-nick  
- **Sriprajnav Koduri** - Github: @pkoduri14  

## Setup Instructions
How to run your project locally:  
*Note: `py` may have to be replaced by `python` on some systems.*

1. Create virtual environment (if you do not have one yet):  
   `py -m venv .venv`
2. Install packages (if you have not done so yet):  
   `pip install -r requirements.txt`
3. Start Flask by running:  
   `py src/app.py`

## Technologies Used
- Language: Python + Flask  
- Frontend: HTML, CSS, Bootstrap, JavaScript  
- NLP / LLM: Local (Ollama) and/or cloud-based APIs (e.g., OpenAI)

## Project Structure
- `/src`: all project files  
- `/src/templates`: HTML files  
- `/src/static`: CSS files  

## License
GNU GPLv3
