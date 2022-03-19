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

1. pyenv exec coverage run --source=controllers,models,routes,functions --module pytest --verbose tests && coverage report --show-missing
2. pyenv exec mutmut run --paths-to-mutate application 
3. pyenv exec mutmut html