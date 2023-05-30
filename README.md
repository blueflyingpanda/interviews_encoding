# Interviews Encoding
Encodes interview according to guideline.

## Quick Start

Create virtual environment

`python3 -m venv venv`

Activate virtual environment

`source venv/bin/activate`

Install dependencies

`pip install -r requirements`

After installing dependencies run

`python3 -m dostoevsky download fasttext-social-network-model`

Start a program

`python3 main.py`

## How it works

Program will analyze interviews in **interviews** directory 

and encodes them in **interview_code.xlsx** using **interview_code_template.xlsx** as base template
where first 7 columns are meta information and all other columns are questions with codes.

Every row apart from header represents a single interview. Every cell represents answer to the questions block.

In some cells you may find list of keywords from the answers. 

If cell's background is coloured red it means that author attitude is more likely negative,
else if it is green it is more likely positive. If it is white attitude is either neutral or uncertain.

## Interview Formatting

Examples can be found in **interviews** directory

Recommendations can be found in **Система_рекомендаций_для_полуструктурированных_интервью.docx**