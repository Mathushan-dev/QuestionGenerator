from flask import Flask, redirect, url_for, request
from flask import request, jsonify

app = Flask(__name__)


# Mock Data for questions

questions = [
    {
        "question": "What is your name?",
        "no": 1,
        "type": "MC",
        "options": ["Utku", "Mathushan", "Orhun", "David"],
        "answer": "Utku",
        "no opt": 4
    }
]

# Routes
# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Automatic Question Generation API</h1>
<p>A prototype API for question generation.</p>'''

# A route to enter the text input
@app.route('/input', methods=['GET'])
def text():
    return '''<h1>Text Input page</h1>'''

# A route to get the text input and matches it with a similar question from the database. Then redirects it to the display page
@app.route('/input/<question>', methods=['POST'])
def question(question):
    # Use the question matching algorithm and pass the question to it returns question id with information
    id = 1
    return redirect(url_for("input/question", question = id))

# A route to display the question returned from the database
@app.route('/input/question/<id>', methods=['GET'])
def display(id):
    return "The displayed question id is %s" % id

# A route to return all of the available entries in our database.
@app.route('/resources/questions', methods=['GET'])
def api_all():
    return jsonify(questions)

# Error handling page
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run(debug=True)