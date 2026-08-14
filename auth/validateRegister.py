from modelDB.User import User


def validate_register_data(data,db):
    if not data.username or not data.email or not data.password:
        return False, "All fields are required."
    if len(data.password) < 6:
        return False, "Password must be at least 6 characters long."
    if "@" not in data.email:
        return False, "Invalid email address."
    user = User(
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role
    )
    if db.query(User).filter_by(email=user.email).first():
        return False, "Email already registered."
    return True, "Validation successful."