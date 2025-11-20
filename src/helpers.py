def validate_new_username(username, users: dict) -> bool:
    return (len(username) > 4) and username not in users

def validate_new_password(password, users: dict) -> bool:
    return (len(password) > 4)

def validate_login(username, password, users: dict) -> bool:
    return (username in users) and users[username]['password'] == password

def validate_new_user(username, password, users: dict) -> bool:
    return validate_new_username(username, users) and validate_new_password(password, users)