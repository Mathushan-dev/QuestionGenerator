from flask import Flask, redirect, url_for, request, render_template, request, jsonify

app = Flask(__name__)


# Mock Data for questions

questions = {
        "question": "What is your name?",
        "no": 1,
        "type": "MC",
        "options": ["Utku", "Mathushan", "Orhun", "David"],
        "answer": "Utku",
        "no_opt": 4
    }

# Routes
# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Automatic Question Generation API</h1>
<p>A prototype API for question generation.</p>'''

# A route to enter the text input
@app.route('/input', methods=['POST', 'GET'])
def text():
    if request.method == 'GET':
        return render_template('input.html')
    else:
        text = request.form['txt']
        # Use the question matching algorithm and pass the question to it returns question id with information
        id = questions['no']
        return redirect(url_for("display", id = id))

# A route to display the question returned from the database
@app.route('/input/<id>', methods=['GET'])
def display(id):
    q = questions['question']
    no_opt = questions['no_opt']
    options = questions['options']
    return render_template('display.html', question = q, no_opt = no_opt, options = options)

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