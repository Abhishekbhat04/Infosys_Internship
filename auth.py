import pandas as pd
import hashlib
import os

USER_FILE = "users.csv"

# Create file if not exists
def init_user_file():
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register user
def register_user(username, password):
    df = pd.read_csv(USER_FILE)

    if username in df['username'].values:
        return False, "User already exists"

    hashed_pw = hash_password(password)
    new_user = pd.DataFrame([[username, hashed_pw]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

    return True, "User registered successfully"

# Login user
def login_user(username, password):
    df = pd.read_csv(USER_FILE)

    hashed_pw = hash_password(password)

    user = df[(df['username'] == username) & (df['password'] == hashed_pw)]

    if not user.empty:
        return True
    return False