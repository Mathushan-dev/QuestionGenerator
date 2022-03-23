# QuestionGenerator

Requirements:

Use the following link to help you - https://akrabat.com/creating-virtual-environments-with-pyenv/

1. Install Pyenv
2. Create python virtual environment (Python version must be 3.7.12)
3. Activate python virtual environment with - pyenv activate nameofvirtualenvironment

Required Pip Packages:

1. pyenv exec pip install -r requirements.txt

Required External Packages:

1. wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
2. tar -xvf  s2v_reddit_2015_md.tar.gz
3. pyenv exec python -m spacy download en_core_web_sm

Final Execution:

1. pyenv exec python wsgi.py

Test:

1. pyenv exec coverage run --source=paths-to-test-coverage --module pytest --verbose tests && coverage report --show-missing
2. pyenv exec mutmut run --paths-to-mutate application 
3. pyenv exec mutmut html

Docker:

1. docker build --tag python-docker .
2. docker run -d -p 5000:5000 python-docker

API POST:

1. http://40.87.57.232:5000/generateMCQuestionAPI?context=[context]&numberOptions=[numberOfOptions]
Example: http://40.87.57.232:5000/generateMCQuestionAPI?context=Harry%20walked%20to%20the%20park%20&numberOptions=4
2. http://40.87.57.232:5000/generateTFQuestionAPI?context=[context]
Example : http://40.87.57.232:5000/generateTFQuestionAPI?context=Harry%20walked%20to%20the%20park