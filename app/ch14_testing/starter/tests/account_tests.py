from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from tests.test_client import flask_app

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
    vm.validate()

    # Assert
    assert vm.error is None