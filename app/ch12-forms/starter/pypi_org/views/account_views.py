import flask

from pypi_org.infrastructure import request_dict
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service
import pypi_org.infrastructure.cookie_auth as cookie_auth

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    user = user_service.find_user_by_id(user_id)
    if not user:
        return flask.redirect('/account/login')
    return {
        'user': user
    }


# ################### REGISTER #################################


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    r = flask.request

    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': "Some required fields are missing."
        }

    # TODO: Create the user
    user = user_service.create_user(name, email, password)
    if not user:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': "A user with that email already exists."
        }

    # TODO: Log in browser as a session
    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGIN #################################


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    data = request_dict.create()
    email = data.email.lower().strip()
    password = data.password.strip()

    if not email or not password:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': "Some required fields are missing."
        }

    # TODO: Validate the user
    user = user_service.login_user(email, password)
    if not user:
        return {
            'email': email,
            'password': password,
            'error': "The account does not exist or the password is wrong."
        }

    # TODO: Log in browser as a session
    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGOUT #################################


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
