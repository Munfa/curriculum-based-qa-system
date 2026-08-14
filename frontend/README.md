# Bangla Study Assistant Frontend

Bangla Study Assistant is a browser based study interface designed around the NCTB 2026 curriculum data used in this project.

The frontend allows a student to select a class, group when applicable, subject, chapter, and study mode.

The current interface supports:

1. Ask Question
2. MCQ Practice
3. CQ Practice
4. Class 6 curriculum selection
5. Class 7 curriculum selection
6. Class 8 curriculum selection
7. Class 9 Science, Commerce, and Arts selection
8. Class 10 Science, Commerce, and Arts selection
9. Subject based chapter selection
10. All Chapters selection
11. Easy, Medium, and Hard difficulty levels for MCQ and CQ
12. Mock API mode for frontend development
13. Real backend API mode for future integration


# Project Status

The frontend is implemented with plain HTML, CSS, and JavaScript.

No Node.js, npm, React, Vue, Angular, or frontend build framework is required.

Python is used for two purposes:

1. Generating the curriculum JSON file from the NCTB SchoolText dataset.
2. Running a local HTTP server so the browser can load the curriculum JSON correctly.

The Python version currently used for this project is:

```text
Python 3.9.0
```


# Main Technology Stack

```text
HTML5
CSS3
Vanilla JavaScript
Python 3.9.0
JSON
Python HTTP Server
```

The frontend itself does not require any external JavaScript package.


# Project Folder

The current Windows project location is:

```text
C:\D drive\bangla-study-assistant
```


# Project Structure

```text
bangla-study-assistant
│
├── index.html
│
├── README.md
│
├── css
│   └── styles.css
│
├── js
│   ├── config.js
│   ├── mockApi.js
│   ├── api.js
│   └── app.js
│
├── data
│   └── nctb_curriculum_2026.json
│
├── tools
│   └── build_curriculum.py
│
└── NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip
```

Depending on how the dataset ZIP was extracted, the project folder may also contain the extracted NCTB SchoolText directory.

The extracted raw dataset directory is not required when the frontend is running.

The frontend only needs:

```text
data\nctb_curriculum_2026.json
```

The original dataset ZIP is required only when the curriculum JSON needs to be rebuilt.


# File Responsibilities

## index.html

`index.html` contains the main frontend page structure.

It includes:

1. Application sidebar
2. Class dropdown
3. Group dropdown
4. Subject dropdown
5. Chapter dropdown
6. Study mode buttons
7. Main notebook content area
8. JavaScript file loading

The Group selector is displayed only for Class 9 and Class 10.


## css/styles.css

`styles.css` contains all visual styling.

The current design uses:

1. Green navigation sidebar
2. Notebook inspired main content area
3. Responsive layout
4. Mobile layout handling
5. Form styling
6. Dropdown styling
7. MCQ styling
8. CQ styling
9. Answer feedback styling
10. Loading states
11. Error states
12. Reduced motion support


## js/config.js

`config.js` contains frontend configuration.

The most important setting is:

```javascript
USE_MOCK: true
```

When:

```javascript
USE_MOCK: true
```

the frontend uses:

```text
js/mockApi.js
```

When:

```javascript
USE_MOCK: false
```

the frontend sends HTTP requests to the backend configured by:

```javascript
BASE_URL
```

Current development configuration uses mock mode.


## js/mockApi.js

`mockApi.js` provides the local frontend API implementation.

Curriculum metadata is loaded from:

```text
data/nctb_curriculum_2026.json
```

This includes:

1. Classes
2. Groups
3. Subjects
4. Chapters

There is no fake chapter fallback.

If a subject does not have chapter metadata in the generated curriculum JSON, the frontend reports that verified chapters are unavailable.

The QA, MCQ, and CQ answer generation inside `mockApi.js` is still mock functionality.

This means:

```text
Class metadata       Dataset based
Group metadata       Local curriculum configuration
Subject metadata     Dataset based curriculum configuration
Chapter metadata     Dataset based
QA answer            Mock
MCQ question         Mock
MCQ grading          Mock
CQ question          Mock
CQ grading           Mock
```

This separation allows the complete frontend workflow to be tested before the real backend is connected.


## js/api.js

`api.js` is the API boundary between the user interface and the data source.

`app.js` does not directly call the backend.

Instead it calls functions such as:

```javascript
Api.getClasses()
Api.getGroups()
Api.getSubjects()
Api.getChapters()
Api.askQuestion()
Api.generateMcq()
Api.gradeMcq()
Api.generateCq()
Api.gradeCq()
```

If mock mode is enabled, these functions use `MockApi`.

If mock mode is disabled, these functions use HTTP requests to the configured backend.


## js/app.js

`app.js` controls the application state and user interaction.

It handles:

1. Initial application loading
2. Class selection
3. Group selection
4. Subject selection
5. Chapter selection
6. All Chapters option
7. Mode selection
8. Ask Question interface
9. MCQ generation
10. MCQ answer submission
11. MCQ grading result
12. CQ generation
13. CQ answer submission
14. CQ grading result
15. Difficulty selection
16. Progress indicators
17. Loading messages
18. Error messages
19. HTML escaping
20. UI rendering


# Curriculum Selection Flow

For Class 6, Class 7, and Class 8:

```text
Class
  ↓
Subject
  ↓
Chapter
  ↓
Study Mode
```

For Class 9 and Class 10:

```text
Class
  ↓
Group
  ↓
Subject
  ↓
Chapter
  ↓
Study Mode
```

Available groups are:

```text
Science
Commerce
Arts
```


# Chapter Selection

Each subject receives a chapter list from:

```text
data\nctb_curriculum_2026.json
```

The first chapter option is:

```text
All Chapters
```

Therefore the user can either study one chapter or select all available chapters.


# Science Subjects

For Class 9 and Class 10 Science, the curriculum configuration includes subjects such as:

```text
পদার্থবিজ্ঞান
রসায়ন
জীববিজ্ঞান
উচ্চতর গণিত
বাংলাদেশ ও বিশ্বপরিচয়
```

With the corrected curriculum builder, the current dataset validation expects:

```text
পদার্থবিজ্ঞান: 12 chapters
রসায়ন: 12 chapters
জীববিজ্ঞান: 14 chapters
উচ্চতর গণিত: 14 chapters
```


# Study Modes

## Ask Question

The student can type a question related to the selected textbook chapter.

In mock mode the frontend receives a placeholder answer and source information.

Expected request structure:

```json
{
  "class": "Class 9",
  "group": "Science",
  "subject": "জীববিজ্ঞান",
  "chapter": "6. জীবে পরিবহণ",
  "question": "Explain the main concept of this chapter."
}
```

Expected response structure:

```json
{
  "answer": "Generated answer",
  "sources": [
    {
      "chapter": "6. জীবে পরিবহণ",
      "chunk_id": "example_chunk"
    }
  ]
}
```


# MCQ Practice

MCQ Practice supports three difficulty levels:

```text
Easy
Medium
Hard
```

Default difficulty:

```text
Medium
```

Expected generation request:

```json
{
  "class": "Class 9",
  "group": "Science",
  "subject": "জীববিজ্ঞান",
  "chapter": "6. জীবে পরিবহণ",
  "difficulty": "Medium"
}
```

Expected generation response:

```json
{
  "question_id": "mcq_1",
  "question": "Question text",
  "options": [
    "Option A",
    "Option B",
    "Option C",
    "Option D"
  ]
}
```

Expected grading request:

```json
{
  "question_id": "mcq_1",
  "selected_option": "Option A"
}
```

Expected grading response:

```json
{
  "question_id": "mcq_1",
  "correct": true,
  "correct_option": "Option A",
  "feedback": "Correct."
}
```


# CQ Practice

CQ Practice also supports:

```text
Easy
Medium
Hard
```

Expected generation request:

```json
{
  "class": "Class 9",
  "group": "Science",
  "subject": "জীববিজ্ঞান",
  "chapter": "6. জীবে পরিবহণ",
  "difficulty": "Medium"
}
```

Expected response:

```json
{
  "question_id": "cq_1",
  "stimulus": "Stimulus text",
  "ka": "ক question",
  "kha": "খ question",
  "ga": "গ question",
  "gha": "ঘ question"
}
```

Expected grading request:

```json
{
  "question_id": "cq_1",
  "student_answers": {
    "ka": "Student answer",
    "kha": "Student answer",
    "ga": "Student answer",
    "gha": "Student answer"
  }
}
```

Expected grading response:

```json
{
  "ka": {
    "score": 1,
    "feedback": "Feedback"
  },
  "kha": {
    "score": 2,
    "feedback": "Feedback"
  },
  "ga": {
    "score": 2,
    "feedback": "Feedback"
  },
  "gha": {
    "score": 3,
    "feedback": "Feedback"
  },
  "total": 8
}
```


# Curriculum Dataset

The curriculum metadata used by this project comes from the downloaded NCTB SchoolText archive:

```text
NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip
```

The archive contains chapter configuration files and processed chapter data.

The frontend does not parse the dataset directly.

Instead:

```text
Dataset ZIP
    ↓
tools\build_curriculum.py
    ↓
data\nctb_curriculum_2026.json
    ↓
js\mockApi.js
    ↓
js\api.js
    ↓
js\app.js
    ↓
Browser Interface
```


# Curriculum Builder

The curriculum builder is:

```text
tools\build_curriculum.py
```

Its job is to generate:

```text
data\nctb_curriculum_2026.json
```

The corrected builder reads chapter configuration JSON files from the dataset archive.

This avoids incorrectly detecting a class from chapter numbers such as:

```text
ch6
ch7
ch8
```

That distinction is important because those numbers represent chapter numbers and must not be interpreted as Class 6, Class 7, or Class 8.


# Python Version

The current development machine uses:

```text
Python 3.9.0
```

Verify it with:

```powershell
python --version
```

Expected output:

```text
Python 3.9.0
```


# Python Dependencies

No external Python package is required for the frontend or the curriculum builder.

The project uses Python standard library modules such as:

```text
argparse
json
re
sys
zipfile
collections
pathlib
typing
```

Therefore there is no required:

```text
requirements.txt
```

and no:

```text
pip install
```

step is needed for the current frontend.


# First Time Setup

Open PowerShell.

Move into the project directory:

```powershell
cd "C:\D drive\bangla-study-assistant"
```

Check Python:

```powershell
python --version
```

Expected:

```text
Python 3.9.0
```


# Check the Curriculum Builder

Before generating curriculum data, confirm that the corrected builder is being used.

Run:

```powershell
Select-String -Path ".\tools\build_curriculum.py" -Pattern "Chapter config files found"
```

A match should appear.

Then run:

```powershell
Select-String -Path ".\tools\build_curriculum.py" -Pattern "JSONL files found"
```

The corrected chapter configuration based builder should not print a matching old builder line.


# Check Python Syntax

Run:

```powershell
python -m py_compile ".\tools\build_curriculum.py"
```

If there is no output, Python syntax validation passed.


# Generate the Curriculum JSON

Make sure this dataset ZIP exists in the project directory:

```text
NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip
```

Then run:

```powershell
python -u ".\tools\build_curriculum.py" --zip ".\NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip"
```

The script should generate:

```text
data\nctb_curriculum_2026.json
```


# Expected Correct Builder Output

The corrected builder should begin with output similar to:

```text
Reading: C:\D drive\bangla-study-assistant\NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip
Archive files: 1668
Chapter config files found: 99
```

Expected curriculum summary for the current dataset:

```text
Class 6: 22 subjects, 215 chapters
Class 7: 22 subjects, 217 chapters
Class 8: 22 subjects, 226 chapters
Class 9-10: 33 subjects, 450 chapters
```

Expected Science chapter validation:

```text
পদার্থবিজ্ঞান: 12 chapters
রসায়ন: 12 chapters
জীববিজ্ঞান: 14 chapters
উচ্চতর গণিত: 14 chapters
```

If the terminal instead displays:

```text
JSONL files found: 1535
```

followed by:

```text
Unknown grade labels:
1
2
3
4
5
```

an older builder version is still being executed.

Replace:

```text
tools\build_curriculum.py
```

with the corrected builder before generating the curriculum again.


# Verify the Generated JSON

Check that the file exists:

```powershell
Get-Item ".\data\nctb_curriculum_2026.json" | Format-List FullName,Length
```

A valid result should show a nonzero file size.


# Verify Biology Chapters

Run:

```powershell
python -c "import json; d=json.load(open(r'.\data\nctb_curriculum_2026.json',encoding='utf-8')); print(len(d['chapters']['Class 9-10']['জীববিজ্ঞান'])); print(*[x['number'] + '. ' + x['title'] for x in d['chapters']['Class 9-10']['জীববিজ্ঞান']],sep='\n')"
```

The first line should be:

```text
14
```

The chapter numbers should continue from:

```text
1
2
3
4
5
6
7
8
9
10
11
12
13
14
```

There should be no missing 6, 7, or 8 chapters.


# How to Run the Frontend

Do not rely on opening `index.html` directly with a file URL.

For example, avoid using:

```text
file:///C:/D drive/bangla-study-assistant/index.html
```

The frontend loads:

```text
data/nctb_curriculum_2026.json
```

using the browser `fetch()` API.

Some browsers restrict local file requests.

The recommended method is to run a local HTTP server.


# Start the Local Server

Open PowerShell.

Run:

```powershell
cd "C:\D drive\bangla-study-assistant"
```

Then:

```powershell
python -m http.server 8000
```

Expected output:

```text
Serving HTTP on :: port 8000
```

Keep that PowerShell window open.


# Open the Application

Open a browser and visit:

```text
http://localhost:8000
```

The application should now load the curriculum JSON.


# Stop the Server

Return to the PowerShell window and press:

```text
Ctrl + C
```

The local server will stop.


# Restart the Server

Run:

```powershell
cd "C:\D drive\bangla-study-assistant"
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```


# Browser Cache

After changing JavaScript or rebuilding the curriculum JSON, perform a hard refresh:

```text
Ctrl + F5
```

This helps ensure the browser is displaying the latest files.


# Normal HTTP Server Messages

You may see:

```text
GET / HTTP/1.1 304
GET /css/styles.css HTTP/1.1 304
GET /js/config.js HTTP/1.1 304
GET /js/mockApi.js HTTP/1.1 304
GET /js/api.js HTTP/1.1 304
GET /js/app.js HTTP/1.1 304
```

HTTP status:

```text
304
```

is normally not an application error.

It means the browser already has a cached version of the file.


# Curriculum JSON Success Message

A useful server log is:

```text
GET /data/nctb_curriculum_2026.json HTTP/1.1 200
```

This means the curriculum JSON was successfully requested by the browser.


# favicon.ico 404

You may see:

```text
GET /favicon.ico HTTP/1.1 404
```

This does not stop the application.

It only means a favicon file has not been added to the project.


# Curriculum Data Unavailable Error

If the application displays:

```text
Curriculum data unavailable
```

check these items.

First confirm the JSON exists:

```powershell
Get-Item ".\data\nctb_curriculum_2026.json"
```

Then confirm you are inside:

```text
C:\D drive\bangla-study-assistant
```

Then run:

```powershell
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

Do not open the HTML page directly from Windows Explorer.


# Testing the Selection Workflow

For Class 6:

```text
Class 6
    ↓
Subject
    ↓
Chapter
    ↓
Mode
```

For Class 9 Science:

```text
Class 9
    ↓
Science
    ↓
জীববিজ্ঞান
    ↓
Chapter
    ↓
Mode
```

For Class 10 Commerce:

```text
Class 10
    ↓
Commerce
    ↓
Subject
    ↓
Chapter
    ↓
Mode
```

For Class 10 Arts:

```text
Class 10
    ↓
Arts
    ↓
Subject
    ↓
Chapter
    ↓
Mode
```


# Mock Mode

Current configuration:

```javascript
const CONFIG = {
  USE_MOCK: true,
  BASE_URL: "https://person-c-api.example.com",
  MOCK_LATENCY_MS: 250,
};
```

With:

```javascript
USE_MOCK: true
```

the frontend uses local metadata and mock study responses.

This mode is useful for:

1. UI development
2. Dropdown testing
3. Curriculum testing
4. QA interface testing
5. MCQ workflow testing
6. CQ workflow testing
7. Backend independent demonstration


# Switching to the Real Backend

Open:

```text
js\config.js
```

Change:

```javascript
USE_MOCK: true
```

to:

```javascript
USE_MOCK: false
```

Then update:

```javascript
BASE_URL
```

Example:

```javascript
const CONFIG = {
  USE_MOCK: false,
  BASE_URL: "http://127.0.0.1:8001",
  MOCK_LATENCY_MS: 250,
};
```

The exact URL must match the real backend service.


# Backend Routes Expected by the Frontend

The current `api.js` expects these routes.

## Classes

```text
GET /metadata/classes
```


## Groups

```text
GET /metadata/groups?class=Class%209
```


## Subjects

For Class 6, 7, or 8:

```text
GET /metadata/subjects?class=Class%208
```

For Class 9 or 10:

```text
GET /metadata/subjects?class=Class%209&group=Science
```


## Chapters

Example:

```text
GET /metadata/chapters?class=Class%209&subject=জীববিজ্ঞান&group=Science
```


## Ask Question

```text
POST /qa
```


## Generate MCQ

```text
POST /mcq/generate
```


## Grade MCQ

```text
POST /mcq/grade
```


## Generate CQ

```text
POST /cq/generate
```


## Grade CQ

```text
POST /cq/grade
```


# Backend Integration Rule

The frontend uses this architecture:

```text
app.js
   ↓
api.js
   ↓
MockApi or Real Backend
```

Therefore UI code should not directly call:

```javascript
fetch()
```

for backend study requests.

Backend route changes should normally be handled inside:

```text
js\api.js
```

Configuration changes should normally be handled inside:

```text
js\config.js
```


# Class 9 and Class 10 Group Handling

For Class 9 and Class 10, the selected group is included in API requests.

Example:

```json
{
  "class": "Class 9",
  "group": "Science",
  "subject": "জীববিজ্ঞান"
}
```

For Class 6, Class 7, and Class 8, group is not required.


# All Chapters Handling

The chapter dropdown includes:

```text
All Chapters
```

At present the frontend sends the literal value:

```json
{
  "chapter": "All Chapters"
}
```

If the future backend requires `null`, an omitted value, or another convention, that behavior should be coordinated with the backend API.


# Data Flow

The curriculum side works like this:

```text
NCTB SchoolText ZIP
        ↓
build_curriculum.py
        ↓
nctb_curriculum_2026.json
        ↓
mockApi.js
        ↓
api.js
        ↓
app.js
        ↓
Student Interface
```

The future study generation side will work like this:

```text
Student Interface
        ↓
app.js
        ↓
api.js
        ↓
Real Backend
        ↓
Retrieval and Generation System
        ↓
Answer or Question
        ↓
Frontend
```


# Frontend Scope

This repository is responsible for the browser interface and curriculum navigation.

The frontend currently handles:

1. User interface
2. Curriculum navigation
3. User input
4. API request preparation
5. API response rendering
6. MCQ interaction
7. CQ interaction
8. Loading states
9. Error states
10. Selection state

The frontend does not implement the production retrieval or language model pipeline.


# Important Development Rule

Curriculum chapter metadata should not be manually replaced with fake chapter names when a dataset chapter cannot be found.

The application intentionally reports unavailable verified chapter metadata instead of silently inventing chapter content.


# Rebuild Workflow

When the curriculum builder or dataset changes, use this sequence:

```powershell
cd "C:\D drive\bangla-study-assistant"

python --version

python -m py_compile ".\tools\build_curriculum.py"

Remove-Item ".\data\nctb_curriculum_2026.json" -ErrorAction SilentlyContinue

python -u ".\tools\build_curriculum.py" --zip ".\NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip"

Get-Item ".\data\nctb_curriculum_2026.json" | Format-List FullName,Length

python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

Finally perform:

```text
Ctrl + F5
```


# Normal Daily Run

If `nctb_curriculum_2026.json` has already been generated correctly, there is no reason to rebuild it every time.

Normally only run:

```powershell
cd "C:\D drive\bangla-study-assistant"

python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```


# Port 8000 Already in Use

If port 8000 is already occupied, use another port:

```powershell
python -m http.server 8080
```

Then visit:

```text
http://localhost:8080
```


# Quick Troubleshooting

## Problem

```text
Curriculum data unavailable
```

Check:

```text
data\nctb_curriculum_2026.json
```

Then run the project through the HTTP server.


## Problem

Class dropdown does not load.

Check the browser developer console.

Also confirm:

```text
GET /data/nctb_curriculum_2026.json
```

returns status:

```text
200
```


## Problem

Physics, Chemistry, Biology, or Higher Mathematics has missing chapters.

Rebuild the curriculum using the corrected chapter configuration based builder.

Expected result:

```text
পদার্থবিজ্ঞান: 12
রসায়ন: 12
জীববিজ্ঞান: 14
উচ্চতর গণিত: 14
```


## Problem

Terminal shows:

```text
JSONL files found: 1535
```

This indicates the older JSONL based builder is still being used.

The corrected builder should display:

```text
Chapter config files found: 99
```


## Problem

Browser shows old frontend code.

Use:

```text
Ctrl + F5
```


## Problem

Server shows:

```text
favicon.ico 404
```

This can be ignored unless a favicon is required.


# Recommended Development Sequence

Use the project in this order:

```text
1. Verify Python 3.9.0

2. Verify build_curriculum.py

3. Build nctb_curriculum_2026.json

4. Verify chapter counts

5. Start Python HTTP server

6. Open localhost

7. Test Class selection

8. Test Group selection

9. Test Subject selection

10. Test Chapter selection

11. Test Ask Question

12. Test MCQ Practice

13. Test CQ Practice

14. Connect the real backend when available
```


# Current Runtime Requirement Summary

```text
Operating System:
Windows tested

Python:
3.9.0

Browser:
Modern Chrome, Edge, Firefox, or equivalent

Node.js:
Not required

npm:
Not required

pip packages:
Not required

Frontend framework:
None

Local web server:
Python http.server

Default port:
8000

Curriculum file:
data/nctb_curriculum_2026.json

Frontend mode:
Mock mode by default
```


# Quick Start

For an already prepared project:

```powershell
cd "C:\D drive\bangla-study-assistant"

python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

For curriculum regeneration:

```powershell
cd "C:\D drive\bangla-study-assistant"

python -m py_compile ".\tools\build_curriculum.py"

python -u ".\tools\build_curriculum.py" --zip ".\NCTB-SchoolText A Curriculum-Aligned BanglaEnglish.zip"

python -m http.server 8000
```

Open:

```text
http://localhost:8000
```


# Final Notes

The frontend is intentionally separated from the production backend.

Curriculum navigation can be developed and tested locally using the generated NCTB curriculum JSON.

QA, MCQ, and CQ interfaces can also be tested in mock mode.

When the real backend becomes available, switching from mock mode should mainly require changes to:

```text
js\config.js
```

and, when API route contracts differ:

```text
js\api.js
```

The remaining UI logic can stay independent of the backend implementation.