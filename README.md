Spectra - A Conversational Coding Assistant
# 1. Problem:
Coding still relies heavily on memorizing syntax and precise typing — barriers that make programming intimidating for beginners and inaccessible for users with disabilities. In a world where technology is increasingly voice-driven, programming should evolve to be just as conversational and intuitive.

# 2. How (Technology):
Frontend: Built with HTML, CSS, and JavaScript, featuring the Web Speech API for real-time voice input and live code rendering through a modern code editor (CodeMirror or Prism.js).
Backend: A lightweight Flask server running Natural Language Processing (NLP) models that interpret spoken commands and generate accurate, runnable code snippets.
Example: A user says, “Make a loop that prints numbers one to five,” and the NLP system understands the intent, outputting:
for i in range(1, 6):
    print(i)
NLP Models: Options include spaCy, Ollama, OpenAI API, or a fine-tuned lightweight transformer for local use, balancing cost and performance.

# 3. Monetize:
Spectra can be offered as a freemium educational platform or browser extension:
Free Tier: Access to a locally hosted distilled model (via Ollama) for basic code generation and syntax explanations
Premium Tier ($10/month): Unlocks cloud-based APIs (e.g., OpenAI) for enhanced accuracy, multi-language support (Python, C++, Java, JavaScript), and “Explain Mode,” which teaches coding logic behind each output.

### Siddharth's Run Notes Below
### windows setup (py may have to replaced with python3):
```
py -m venv .venv
.venv\Scripts\activate.ps1
pip install requirements.txt
```
### to run:

make sure the venv is active (u should see .venv next to the command line prompt)
if not active, run `.venv\Scripts\activate.ps1 `

then run `py src/app.py`

- Siddharth Kakumanu
- Nikhil Verma
