
import getpass
import sys

from module.auth import create_user, load_users


def main():
    print("\n=== LeaveSync | Initial Admin Setup ===\n")

    try:
        data = load_users()
    except (OSError, ValueError) as exc:
        print(f"Could not read users.json: {exc}")
        sys.exit(1)

    if any(
        user.get("role") == "admin"
        for user in data["users"]
    ):
        print("An Admin account already exists. Setup cancelled.")
        return

    username = input("Choose Admin username: ").strip()
    password = getpass.getpass("Choose Admin password (12+ characters): ")
    confirm = getpass.getpass("Confirm Admin password: ")

    if password != confirm:
        print("Passwords do not match. No account was created.")
        return

    try:
        create_user(username, password, "admin")
    except (ValueError, OSError) as exc:
        print(f"Account creation failed: {exc}")
        sys.exit(1)

    print("\nAdmin account created successfully.")
    print("Keep your credentials private.")
    print("You can now proceed to login integration.")


if __name__ == "__main__":
    main()
