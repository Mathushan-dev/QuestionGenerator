# QuestionGenerator

X5GON is an industry leading Open Education Resource Provider. This project aims to help both students and teachers that may not have the resources to create questions for certain educational material. For teachers it can be difficult to invent questions from scratch on new educational material. Also, for students there might not have the resources for them to self-test themselves on educational material without teacher supervision. Our software solves both of these problems.

In this project, we worked on developing a system that can generate question from educational material by applying Natural Language Processing (NLP) techniques, and used a database to keep track of the user's performance. We chose to generate multiple choice (MC) and true or false questions since it is one of the fastest methods to check user's understanding and it is easy to keep track of performance. Our system is open source so that everyone can make the most out of it.

We achieved the generation of multiple MC and true or false questions out of general educational material successfully. All the generated questions were up to very high standards and there were no non-sensical questions that might confuse the users.

# Manual Deployment
## Requirements

Use the following link to help you - https://akrabat.com/creating-virtual-environments-with-pyenv/

1. Install Pyenv
2. Create python virtual environment (Python version must be 3.7.12)
3. Activate python virtual environment with - pyenv activate nameofvirtualenvironment

## Required Pip Packages

1. pyenv exec pip install -r requirements.txt

## Required External Packages

1. wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
2. tar -xvf  s2v_reddit_2015_md.tar.gz
3. pyenv exec python -m spacy download en_core_web_sm

## Final Execution

1. pyenv exec python wsgi.py

# Docker Deployment

1. docker build --tag python-docker .
2. docker run -d -p 5000:5000 python-docker

# Test

1. pyenv exec coverage run --source=paths-to-test-coverage --module pytest --verbose tests && coverage report --show-missing
2. pyenv exec mutmut run --paths-to-mutate application 
3. pyenv exec mutmut html

# API POST

1. http://40.87.57.232:5000/generateMCQuestionAPI?context=[context]&numberOptions=[numberOfOptions]
Example: http://40.87.57.232:5000/generateMCQuestionAPI?context=Harry%20walked%20to%20the%20park%20&numberOptions=4
2. http://40.87.57.232:5000/generateTFQuestionAPI?context=[context]
Example : http://40.87.57.232:5000/generateTFQuestionAPI?context=Harry%20walked%20to%20the%20park