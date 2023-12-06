import ast
import copy

_users_file_path = 'data/users.dat'
_administrators_file_path = 'data/administrators.dat'

_users = dict()
_administrators = set()


def get_users():
    return copy.deepcopy(_users)


def get_administrators():
    return _administrators.copy()


def save_to_file():
    with open(_administrators_file_path, 'w') as file:
        file.write(str(_administrators))
    with open(_users_file_path, 'w') as file:
        file.write(str(_users))


def load_from_file():
    global _administrators, _users
    try:
        with open(_administrators_file_path, 'r') as file:
            _administrators = ast.literal_eval(file.read())
    except FileNotFoundError:
        _administrators = set()

    try:
        with open(_users_file_path, 'r') as file:
            _users = ast.literal_eval(file.read())
    except FileNotFoundError:
        _users = dict()


def add_user(user_chat_id: int, name: str, username: str):
    _users[user_chat_id] = {'name': name, 'username': username}
    save_to_file()


def remove_user(user_chat_id: int):
    del _users[user_chat_id]
    save_to_file()


def add_admin(admin_chat_id: int):
    _administrators.add(admin_chat_id)
    save_to_file()


def remove_admin(admin_chat_id: int):
    _administrators.remove(admin_chat_id)
    save_to_file()


def is_admin_set():
    return len(_administrators) != 0


def is_user_exist(user_chat_id: int):
    return user_chat_id in _users


def is_admin_exist(admin_chat_id: int):
    return admin_chat_id in _administrators
