# Spectrometry - A Conversational Coding Assistant

## 1. Problem:
Coding still relies heavily on memorizing syntax and precise typing — barriers that make programming intimidating for beginners and inaccessible for users with disabilities. In a world where technology is increasingly voice-driven, programming should evolve to be just as conversational and intuitive.

## 2. How (Technology):
Frontend: Built with HTML, CSS, and JavaScript, featuring the Web Speech API for real-time voice input and live code rendering through a modern code editor (CodeMirror or Prism.js).
Backend: A lightweight Flask server running Natural Language Processing (NLP) models that interpret spoken commands and generate accurate, runnable code snippets.
Example: A user says, “Make a loop that prints numbers one to five,” and the NLP system understands the intent, outputting:
for i in range(1, 6):
    print(i)
NLP Models: Options include spaCy, Ollama, OpenAI API, or a fine-tuned lightweight transformer for local use, balancing cost and performance.

## 3. Monetize:
Spectra can be offered as a freemium educational platform or browser extension:
Free Tier: Access to a locally hosted distilled model (via Ollama) for basic code generation and syntax explanations
Premium Tier ($10/month): Unlocks cloud-based APIs (e.g., OpenAI) for enhanced accuracy, multi-language support (Python, C++, Java, JavaScript), and “Explain Mode,” which teaches coding logic behind each output.

## Team Members
- **Siddharth Kakumanu** - GitHub: @FormulaCarbon
- **Ansh Kapadia** - GitHub: @AnshVKapadia
- **Aanya Kotla** - Github: @aak-222735
- **Nikhil Verma** - Github: @socials-nick
- **Sriprajnav Koduri** - Github: @pkoduri14

## Setup Instructions
How to run your project locally:
Note: `py` may have to be replaced by `python`
1. Create virtual environment (if you do not have one yet): `py -m venv .venv`
2. Install packages (if you have not done so yet): `pip install -r requirements.txt`
3. Start flask by running `py src/app.py`

## Technologies Used
- Language: Python + Flask
- Bootstrap

## Project Structure
`/src`: all project files
`/src/templates`: HTML files
`/src/static`: CSS files

## License
GNU GPLv3