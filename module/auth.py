import hashlib
import hmac
import json
import os
import re
import secrets
import tempfile
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
USERS_FILE = DATA_DIR / "users.json"

# PBKDF2 password hashing configuration
HASH_NAME = "sha256"
HASH_ITERATIONS = 600_000
SALT_BYTES = 16


def ensure_users_file():
    """Create the user file if it does not already exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_FILE.exists():
        save_users({"users": []})


def load_users():
    """Load registered accounts from JSON."""
    ensure_users_file()

    with USERS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or not isinstance(data.get("users"), list):
        raise ValueError("Invalid users.json format.")

    return data


def save_users(data):
    """Write users.json using a temporary file to reduce partial writes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_DIR,
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            json.dump(data, temp_file, indent=4)
            temp_file.write("\n")
            temp_path = temp_file.name

        os.replace(temp_path, USERS_FILE)
        return True

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def validate_username(username):
    """Allow simple usernames without spaces or special characters."""
    return bool(
        isinstance(username, str)
        and re.fullmatch(r"[A-Za-z0-9_.-]{3,40}", username)
    )


def hash_password(password, salt_hex=None, iterations=HASH_ITERATIONS):
    """Hash a password with PBKDF2-HMAC-SHA256."""
    if not isinstance(password, str) or len(password) < 12:
        raise ValueError("Password must contain at least 12 characters.")

    salt = (
        bytes.fromhex(salt_hex)
        if salt_hex is not None
        else secrets.token_bytes(SALT_BYTES)
    )

    password_hash = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        iterations,
    )

    return salt.hex(), password_hash.hex()


def create_user(username, password, role, employee_id=None):
    """Create an account with an explicitly assigned role."""
    if not validate_username(username):
        raise ValueError(
            "Username must be 3-40 characters: letters, numbers, ., _, or -."
        )

    if role not in {"admin", "manager", "employee"}:
        raise ValueError("Invalid role.")

    if role == "employee" and employee_id is None:
        raise ValueError("Employee accounts require an employee ID.")

    if role != "employee" and employee_id is not None:
        raise ValueError("Only employee accounts can have an employee ID.")

    data = load_users()
    normalized_username = username.casefold()

    if any(
        user.get("username", "").casefold() == normalized_username
        for user in data["users"]
    ):
        raise ValueError("That username already exists.")

    if employee_id is not None:
        from module.work_coverage import load_employees

        employees = load_employees()
        if not any(str(e.get("id")) == str(employee_id) for e in employees):
            raise ValueError("Employee ID does not exist in employees.json.")

        if any(
            user.get("role") == "employee"
            and str(user.get("employee_id")) == str(employee_id)
            for user in data["users"]
        ):
            raise ValueError("That employee already has a login account.")

    salt, password_hash = hash_password(password)

    data["users"].append(
        {
            "username": username,
            "role": role,
            "employee_id": employee_id,
            "salt": salt,
            "password_hash": password_hash,
            "iterations": HASH_ITERATIONS,
            "enabled": True,
        }
    )

    save_users(data)
    return True


def authenticate_user(username, password):
    """Return safe account details after successful verification."""
    if not isinstance(username, str) or not isinstance(password, str):
        return None

    try:
        data = load_users()
    except (OSError, json.JSONDecodeError, ValueError):
        return None

    user = next(
        (
            item
            for item in data["users"]
            if isinstance(item.get("username"), str)
            and item["username"].casefold() == username.strip().casefold()
        ),
        None,
    )

    if user is None or user.get("enabled") is not True:
        return None

    try:
        iterations = user["iterations"]
        salt = user["salt"]
        expected_hash = user["password_hash"]

        if (
            not isinstance(iterations, int)
            or isinstance(iterations, bool)
            or not 100_000 <= iterations <= 2_000_000
            or not isinstance(salt, str)
            or not isinstance(expected_hash, str)
            or not re.fullmatch(r"[0-9a-fA-F]{32}", salt)
            or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash)
        ):
            return None

        _, actual_hash = hash_password(password, salt, iterations)

        if not hmac.compare_digest(actual_hash, expected_hash):
            return None

    except (KeyError, ValueError, TypeError):
        return None

    # Never return the salt or password hash to the UI.
    return {
        "username": user["username"],
        "role": user["role"],
        "employee_id": user.get("employee_id"),
    }