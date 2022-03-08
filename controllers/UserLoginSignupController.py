from flask import render_template, request, make_response
from models.UserLoginSignupModel import UserLoginSignup
from models.UserLoginSignupModel import db
from controllers.UserQuestionHandlerController import load_current_questions
from functions.profileStatsCalculator import get_profile_stats
from sqlalchemy.exc import IntegrityError
from config import DEBUG
from datetime import date, datetime
import json

firstLaunch = True


def index():
    """
    todo
    :rtype: object
    """
    if DEBUG:
        print("index called")
        global firstLaunch
        if firstLaunch:
            clear_table()
            firstLaunch = False
    logged_on: int = 1
    if request.cookies.get('LoggedOnUserId') is None:
        logged_on = 0
    return render_template('launchpage.html', loggedOn=logged_on)


def login_signup_form(message=""):
    """
    todo
    :rtype: object
    """
    if DEBUG:
        print("loginForm called", message)
    return render_template('signup-login.html', loginErrorMessage=message)


def load_enter_text():
    """
    todo
    :rtype: object
    """
    if DEBUG:
        print("try-input-passage page called")
    logged_on = 1
    if request.cookies.get('LoggedOnUserId') is None:
        logged_on = 0
    return render_template('try-input-passage.html', loggedOn=logged_on)


def sign_up():
    """
    todo
    :rtype: object
    """
    if DEBUG:
        print("signUp called")
    user_id = request.form.get("email")
    f_name = request.form.get("fName")
    l_name = request.form.get("lName")
    password = request.form.get("password")

    password_hash = UserLoginSignup.make_password_hash(password)
    user = UserLoginSignup(user_id, f_name, l_name, password_hash)

    try:
        db.session.add(user)
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return login_signup_form(message="Those records already exist on the server, please log in instead.")
    db.session.commit()
    resp = make_response(load_enter_text())
    resp.set_cookie('LoggedOnUserId', user_id)
    return resp


def log_in():
    """
    todo
    :return: Union[object, Response]
    """
    if DEBUG:
        print("logIn called")
    user_id = request.form.get("email")
    password = request.form.get("password")

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()

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
    todo
    :return: Response
    """
    if DEBUG:
        print("logOut called")
    resp = make_response(load_enter_text())
    resp.set_cookie('LoggedOnUserId', 'None', expires=0)
    return resp


def load_home():
    """
    todo
    :return: Union[object, str]
    """
    if DEBUG:
        print("logIn called")

    user_id = request.cookies.get('LoggedOnUserId')

    if request.cookies.get('LoggedOnUserId') is None:
        return login_signup_form("Please login or sign up for an account before viewing question results.")

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()

    if len(users) != 1:
        return login_signup_form(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        f_name, l_name, total_right, total_wrong, questions, contexts, options, scores, attempts = get_profile_stats(
            user_id)
        return render_template('profile.html', fName=f_name, lName=l_name, totalRight=total_right,
                               totalWrong=total_wrong,
                               questions=questions, contexts=contexts, options=options, scores=scores,
                               attempts=attempts, loggedOn=1)


def update_password():
    """
    todo
    :return: None
    """
    pass


def delete_account():
    """
    todo
    :return: Union[object, Response]
    """
    user_id = request.cookies.get('LoggedOnUserId')
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    if len(users) == 0:
        return index()
    elif len(users) != 1:
        return login_signup_form(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        resp = make_response(index)
        resp.set_cookie('LoggedOnUserId', 'None', expires=0)
        try:
            stack_trace = db.session.delete(users[0])
        except:
            print(stack_trace)
        return resp


def stringify_list(list_to_stringify):
    """
    todo
    :param list_to_stringify:
    :return: str
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
    todo
    :param user:
    :param question_id_hash:
    :param score:
    :param tries:
    :return: Tuple[str, str, str, str, str]
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


def save_question_attributes():
    """
    todo
    :return: str
    """
    if DEBUG:
        print("saveQuestionAttributes called")

    attributes_dump = json.dumps(request.get_json())
    attributes = json.loads(attributes_dump)
    question_id_hash = attributes["questionid"]
    score = attributes["score"]
    tries = attributes["tries"]

    user = db.session.query(UserLoginSignup).filter(
        UserLoginSignup.userId == request.cookies.get('LoggedOnUserId')).first()

    if user is not None:
        user.attemptedQuestionIds, user.questionScores, user.numberOfAttempts, user.attemptedDates, user.attemptedTimes = update_records(
            user, question_id_hash, score, tries)
        db.session.commit()

    return load_current_questions("mcq")


def clear_table():
    """
    todo
    :return: None
    """
    if DEBUG:
        users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId != "")
        for user in users:
            db.session.delete(user)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
