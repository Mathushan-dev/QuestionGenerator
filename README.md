# QuestionGenerator

Requirements:

Use the following link to help you - https://akrabat.com/creating-virtual-environments-with-pyenv/

1. Install Pyenv
2. Create python virtual environment (Python version must be 3.7.12)
3. Activate python virtual environment with - pyenv activate nameofvirtualenvironment

Required Pip Packages:

Use following command to force Python version in virtual environment is used to download the pip packages below - pyenv exec pip install --quiet package_name==version. The required pip packages can be found in requirements.txt.

Required External Packages:

1. wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
   1b. tar -xvf  s2v_reddit_2015_md.tar.gz
2. python -m spacy download en_core_web_sm

Final Execution:

1. Execute Program with pyenv version of python

Test:

1. coverage run --source=controllers,models,routes,functions --module pytest --verbose tests && coverage report --show-missing