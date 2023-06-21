Vetter
======

This is a project for the candidate vetting [bounty][] on Replit. It is still
in progress and at the moment only includes a chat bot that can interact with
GPT.

[bounty]: https://replit.com/bounties/@GoodFellas2/coachingbuddy

Problem Description
-------------------

I need your help as a skilled Python developer to create a Minimal Viable
Product (MVP) for a web-based AI tool. The purpose of this tool is to automate
the assessment of job candidates through conversational interactions using
OpenAI's GPT-4. The prompts and questions for the assessments will be provided.
Your task will be to integrate these prompts and ensure a smooth conversation
flow with the job candidates. Once the assessments are completed, the tool
should automatically email me, the hiring manager, with the results.

Acceptance Criteria
-------------------

* The application will initiate when a user defined code is entered
* The application will verify the code
* The application will collect the users (job candidates) name and email
  address which will be passed to ChatGPT
* ChatGPT will initiate a text-based conversation with the job candidate, using
  the provided pre-defined prompts.
* ChatGPT will email a summary and recommend follow up actions to the
  administrator (me)
* It should conclude the assessment once all necessary information is collected.
* The application should have basic error handling capabilities for unexpected
  inputs or system issues.

Development Environment
-----------------------

### Prerequisites

* Python 3.9
* An [OpenAI][] API key stored in the environment variable `OPENAI_API_KEY`.
* [Poetry](https://python-poetry.org/)

[OpenAI]: https://platform.openai.com/

### Setup

To install all required Python packages.

```bash
poetry install
```

Then start a virtual environment in your terminal.

```bash
poetry shell
```

### Run

To start the program from a poetry shell:

```bash
streamlit run vetter/chat.py
```

If it does not automatically open, point your browser to http://localhost:8502/.

### Tests

From within a poetry shell:

```bash
pytest
```

### Technology Reference

* [Streamlit](https://docs.streamlit.io/) -- frontend rendering.
* [Streamlit Cheatsheet](https://daniellewisdl-streamlit-cheat-sheet-app-ytm9sg.streamlit.app/)
* [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
* [Streamlit Chat](https://github.com/AI-Yash/st-chat/blob/main/examples/chatbot.py) -- example chatbot program.
* [OpenAI][] -- AI generated messages.
* [openai/openai-quickstart-python](https://github.com/openai/openai-quickstart-python) -- an example program using Flask.
* [OpenAI Cookbook > How to handle rate limits](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb)
