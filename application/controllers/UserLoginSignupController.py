from flask import render_template, request, make_response
from application.models.UserLoginSignupModel import UserLoginSignup
from application.models.UserLoginSignupModel import db
from application.controllers.UserQuestionHandlerController import load_current_questions
from application.functions.ProfileStatsCalculator import get_profile_stats
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
import json

DEBUG = __import__('config').Config.DEBUG
TEST = __import__('config').Config.TEST
firstLaunch = True


def index():
    """
    This method directs to the index.html . if it is the first launch ,
    clear the database and set the user as logged_on and direct to the lauchpage
    :return: a python flask rendered template, which renders the html page and pass
    parameter to it
    """
    if DEBUG:
        print("index called")
        global firstLaunch
        if firstLaunch:
            clear_table()
            firstLaunch = False
    logged_on = 1
    if request.cookies.get('LoggedOnUserId') is None:
        logged_on = 0
    return render_template('launchpage.html', loggedOn=logged_on)


def login_signup_form(message=""):
    """
    :return: a python flask rendered template, which renders the html page and pass
    parameter to it
    """
    if DEBUG:
        print("loginForm called", message)
    return render_template('signup-login.html', loginErrorMessage=message)


def load_enter_text():
    """
    This method directs to the question trial page
    :return:  a python flask rendered template, which renders the html page and pass
    parameter to it
    """
    if DEBUG:
        print("try-input-passage page called")
    logged_on = 1
    if request.cookies.get('LoggedOnUserId') is None:
        logged_on = 0
    return render_template('try-input-passage.html', loggedOn=logged_on)


def sign_up(user_id="test_email", f_name="test_first_name", l_name="test_last_name", password="test_password"):
    """
    This method handles the user sign up process.The passwords are hashed and stored in database,
    if the users are already registered direct to login page.After sign up,direct to question trial page.
    :return:
    if user exist,a python flask rendered template.
    If not , return a self-defined response object

    """
    if DEBUG:
        print("signUp called")

    if TEST:
        clear_table()
    else:
        user_id = request.form.get("email")
        f_name = request.form.get("fName")
        l_name = request.form.get("lName")
        password = request.form.get("password")

    password_hash = UserLoginSignup.make_password_hash(password)
    user = UserLoginSignup(user_id, f_name, l_name, password_hash)

    try:
        db.session.add(user)
        db.flush()
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        db.flush()
        return login_signup_form(message="Those records already exist on the server, please log in instead.")
    db.session.commit()
    db.flush()
    resp = make_response(load_enter_text())
    resp.set_cookie('LoggedOnUserId', user_id)
    return resp


def log_in(user_id="test_email", password="test_password"):
    """
    check whether a specific user is logged in
    :return:  rendered template
    """
    if DEBUG:
        print("logIn called")

    if not TEST:
        user_id = request.form.get("email")
        password = request.form.get("password")

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    db.flush()

    if len(users) == 0:
        return login_signup_form(message="Those records do not exist on the server, please sign up instead.")
    elif len(users) != 1:
        return login_signup_form(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        if users[0].is_password_valid(password):
            resp = make_response(load_enter_text())
            resp.set_cookie('LoggedOnUserId', user_id)
            return resp
        return login_signup_form(message="The password is incorrect.")


def log_out():
    """
    :return: Response
    """
    if DEBUG:
        print("logOut called")
    resp = make_response(load_enter_text())
    resp.set_cookie('LoggedOnUserId', 'None', expires=0)
    return resp


def load_home(user_id="test_email"):
    """
    This method direct to the user's profile page with user's information
    :return: rendered template
    """
    if DEBUG:
        print("logIn called")

    if not TEST:
        user_id = request.cookies.get('LoggedOnUserId')

    if request.cookies.get('LoggedOnUserId') is None:
        return login_signup_form("Please login or sign up for an account before viewing question results.")

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    db.flush()

    if len(users) != 1:
        return login_signup_form(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        f_name, l_name, total_right, total_wrong, questions, contexts, options, scores, attempts, dates = get_profile_stats(
            user_id)
        return render_template('profile.html', fName=f_name, lName=l_name, totalRight=total_right,
                               totalWrong=total_wrong,
                               questions=questions, contexts=contexts, options=options, scores=scores,
                               attempts=attempts, dates=dates, loggedOn=1)


def update_password():
    """
    :return: None
    """
    pass


def delete_account(user_id="test_email"):
    """
    This method removes the user from database
    :return:
    if the service is down(not likely happend),return the python flask rendered template.
    If not , return a self-defined response object
    """
    if not TEST:
        user_id = request.cookies.get('LoggedOnUserId')
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    db.flush()
    if len(users) == 0:
        return index()
    elif len(users) != 1:
        return login_signup_form(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        resp = make_response(index())
        resp.set_cookie('LoggedOnUserId', 'None', expires=0)
        try:
            stack_trace = db.session.delete(users[0])
            db.flush()
        except:
            print(stack_trace)
        return resp


def stringify_list(list_to_stringify):
    """
    This method concatenates every element in the string list ,add ',' at last
    :param list_to_stringify: this is a string list which contains user's a record.For example,
    number of attempts.
    :return: the transformed string list into string for further operations
    """
    output = ""
    for i in range(0, len(list_to_stringify)):
        element = str(list_to_stringify[i])
        if element.strip() == "":
            continue
        output += str(element)
        if i == len(list_to_stringify) - 1:
            break
        output += ","
    return output


def update_records(user, question_id_hash, score, tries):
    """
    This method fetch user's information of the specific question and update the string list.
    if the question has not been attempted, create a new one in the string list.
    :param user: user's id got from database
    :param question_id_hash: the question's id stored in hash
    :param score: the question's score
    :param tries: number of attempts to this question
    :return: return all the information of the question , to write back to the database
    """
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    attempted_date = d1
    attempted_time = now

    attempted_question_ids = user.attemptedQuestionIds.split(",")
    question_scores = user.questionScores.split(",")
    number_of_attempts = user.numberOfAttempts.split(",")
    attempted_dates = user.attemptedDates.split(",")
    attempted_times = user.attemptedTimes.split(",")

    for i in range(0, len(attempted_question_ids)):
        if attempted_question_ids[i].strip() == question_id_hash:
            question_scores[i] = score
            number_of_attempts[i] = tries
            attempted_dates[i] = attempted_date
            attempted_times[i] = attempted_time
            break

        if i == len(attempted_question_ids) - 1:
            attempted_question_ids.append(question_id_hash)
            question_scores.append(score)
            number_of_attempts.append(tries)
            attempted_dates.append(attempted_date)
            attempted_times.append(attempted_time)

    return stringify_list(attempted_question_ids), stringify_list(question_scores), stringify_list(
        number_of_attempts), stringify_list(attempted_dates), stringify_list(attempted_times)


def save_question_attributes(question_id_hash="test_question_id_hash", score="test_score", tries="test_tries"):
    """
    This method gets the records from update_records method and update in database
    :return: function call of load_current_question , which is a rendered template
    """
    if DEBUG:
        print("saveQuestionAttributes called")

    if not TEST:
        attributes_dump = json.dumps(request.get_json())
        attributes = json.loads(attributes_dump)
        question_id_hash = attributes["questionid"]
        score = attributes["score"]
        tries = attributes["tries"]

    user = db.session.query(UserLoginSignup).filter(
        UserLoginSignup.userId == request.cookies.get('LoggedOnUserId')).first()
    db.flush()

    if user is not None:
        user.attemptedQuestionIds, user.questionScores, user.numberOfAttempts, user.attemptedDates, user.attemptedTimes = update_records(
            user, question_id_hash, score, tries)
        db.session.commit()
        db.flush()

    return load_current_questions("mcq")


def clear_table():
    """
    in debug or test mode, clear the database
    :return: None
    """
    if DEBUG or TEST:
        users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId != "")
        db.flush()
        for user in users:
            db.session.delete(user)
            db.flush()
            db.session.commit()
            db.flush()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
