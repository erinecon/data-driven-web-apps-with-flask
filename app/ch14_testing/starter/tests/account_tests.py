from flask import Response

from pypi_org.data.users import User
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from tests.test_client import flask_app, client
import unittest.mock

def test_example():
    print("Test example...")
    assert 1 + 2 == 3

def test_register_validation_when_valid():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    form_data = {
        'name': 'Michael',
        'email': 'a@b.com',
        'password': 'abcde'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is None

def test_register_validation_for_existing_user():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    form_data = {
        'name': 'Michael',
        'email': 'a@b.com',
        'password': 'abcde'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    test_user = User(email=form_data.get('email'))
    with unittest.mock.patch(target, return_value=test_user):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'already exists' in vm.error

def test_register_validation_view_new_user():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    from pypi_org.views.account_views import register_post
    form_data = {
        'name': 'Michael',
        'email': 'a@b.com',
        'password': 'abcde'
    }

    target = 'pypi_org.services.user_service.find_user_by_email'
    find_user = unittest.mock.patch(target, return_value=None)
    target = 'pypi_org.services.user_service.create_user'
    create_user = unittest.mock.patch(target, return_value=User())
    request = flask_app.test_request_context(path='/account/register', data=form_data)

    with find_user, create_user, request:
        # Act
        resp: Response = register_post()

    # Assert
    assert resp.location == '/account'

def test_register_validation_for_short_password():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    form_data = {
        'name': 'Michael',
        'email': 'a@b.com',
        'password': 'abc'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    test_user = User(email=form_data.get('email'))
    with unittest.mock.patch(target, return_value=test_user):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'at least 5 characters' in vm.error

def test_register_validation_for_no_name_specified():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    form_data = {
        'email': 'a@b.com',
        'password': 'abc'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a name' in vm.error

def test_register_validation_for_no_email_specified():
    # 3 A's of testing: Arrange, Act, Assert

    # Arrange
    form_data = {
        'name': 'Michael',
        'password': 'abc'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify an email' in vm.error

def test_int_account_home_no_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    with unittest.mock.patch(target, return_value=None):
        resp: Response = client.get('/account')

    assert resp.status_code == 302
    assert resp.location == '/account/login'

def test_int_account_home_with_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    test_user = User(name='Erin', email='a@b.c')
    with unittest.mock.patch(target, return_value=test_user):
        resp: Response = client.get('/account')

    assert resp.status_code == 200
    assert b'Erin' in resp.data