# Spectra - A Socratic Problem-Solving Tutor

## 1. Problem:
Most AI tools give students *answers* too quickly. That makes homework look easier in the moment but quietly destroys problem-solving skills and confidence, especially in STEM subjects like **math, computer science, and physics**. Students learn to copy solutions instead of learning how to think: breaking down problems, checking assumptions, manipulating equations, and debugging code.

We need a tool that refuses to be a shortcut and instead *trains* the student’s thinking — in the exact environments where that thinking happens:  
- a **math workspace** with LaTeX for real equations, and  
- a **coding workspace** that feels like a lightweight IDE.

---

## 2. How (Technology):
Spectra is built from the ground up to act like a strict Socratic tutor: it guides with questions and hints, not full solutions (unless the student is truly stuck), with special support for **math, CS, and physics** workflows.

**Frontend:**  
- HTML, CSS, JavaScript  
- Simple “problem workspace” focused on STEM:
  - Left side: **Problem & Work Area**
    - Rich text input with **inline LaTeX** (`\( ... \)` / `$$ ... $$`) for math and physics.
    - A **built-in code editor** (lightweight IDE) for CS problems using Monaco or CodeMirror:
      - Syntax highlighting (Python, C++, Java, JavaScript)
      - Line numbers, indentation, basic error highlighting
  - Right side: **Tutor Dialogue**
    - Chat-style dialogue showing the tutor’s questions and the student’s answers
    - Clearly marked steps like *“Understand → Plan → Execute → Check”*  
- Math & Code UX:
  - LaTeX is auto-rendered via MathJax/KaTeX so equations look like a real math notebook.
  - Code editor supports copy/paste of student attempts and quick “Run/Check” for supported languages (e.g., Python, JS) via backend runners or sandboxed execution.
- Progress indicators:
  - Stage tracker: *Understand problem → Plan → Execute → Check*
  - Gentle badges like:
    - “You identified all givens”
    - “You set up the correct formula”
    - “You tested an edge case”
    - “You debugged your own code without a direct answer”

**Backend:**  
- Lightweight Flask server that:
  - Stores minimal session state:
    - Current problem
    - Subject type (math, CS, physics)
    - Current step and student answers so far
  - Enforces a **Socratic policy**:
    - The model must ask questions first, not give solutions.
    - It can reference student LaTeX or code and respond with targeted questions:
      - For math/physics: ask about units, givens, formulas, algebra steps.
      - For CS: ask about loop bounds, conditions, data structures, test cases.
  - Solution reveal logic:
    - Only reveals full or partial solutions after multiple failed attempts or explicit user request (“I’m stuck. Show me.”)
    - For math/physics: may show a *setup* first (equation, free-body diagram description) before the final numeric answer.
    - For CS: may show a *fixed algorithm outline* before giving a full code snippet.

**NLP / LLM logic (pluggable):**  
- Uses an LLM with a strict system prompt plus metadata (subject type, current step) to:
  - Classify the student’s current step:
    - Understanding the problem
    - Planning a strategy/formula/algorithm
    - Executing computation or writing code
    - Checking and interpreting the result
  - Generate **targeted questions** instead of answers:
    - Math/Physics examples:
      - “What are the knowns and unknowns?”
      - “Which conservation law or formula might apply here?”
      - “Can you isolate \( x \) in this equation?”
    - CS examples:
      - “What input does your function expect and what should it return?”
      - “What happens when the list is empty?”
      - “Can you trace your loop for the first 3 iterations?”
  - Decide when to escalate from:
    - “Hint” → “Outline of solution” → “Full solution”
- Model options:
  - Local models via **Ollama** for low-cost experimentation and offline use.
  - Cloud APIs such as **OpenAI** for higher-quality and multi-domain reasoning across math, CS, and physics.
  - Optional lightweight text/code processing (regex, static checks) to detect:
    - When the student is just pasting the model’s previous output.
    - Common math mistakes (sign errors, unit mistakes).
    - Common CS bugs (off-by-one, wrong comparison, un-initialized variables).

**Example flow (Math):**  
User writes in the math workspace:  
> “Find the derivative of \( f(x) = x^3 - 3x^2 + 5 \).”  

Spectra responds *not* with the derivative, but with questions like:  
- “What rule do we usually use to differentiate powers of \( x \)?”  
- “Can you differentiate just \( x^3 \) first?”  
- “What is the derivative of \( -3x^2 \)?”

**Example flow (CS):**  
User types code in the IDE panel:  
```python
for i in range(1, 5):
    print(i)