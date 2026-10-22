
from getpass import getpass
from module.auth import create_user, load_users


def main():
    print("\n===== LeaveSync Staff Account Setup =====")
    print("1. Create Admin account")
    print("2. Create Manager account")

    choice = input("Choose account type (1/2): ").strip()

    if choice == "1":
        role = "admin"
    elif choice == "2":
        role = "manager"
    else:
        print("Invalid choice.")
        return

    # Prevent accidental duplicate staff accounts
    users = load_users()["users"]
    existing = [u for u in users if u.get("role") == role]

    if role == "admin" and existing:
        print("An Admin account already exists.")
        print("Use the existing account or create another Admin only if permitted.")
        return

    username = input("Enter username: ").strip()
    password = getpass("Enter password (minimum 12 characters): ")
    confirm = getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    try:
        create_user(username, password, role)
        print(f"\n{role.title()} account created successfully.")
        print("You can now log in through the matching LeaveSync portal.")
    except (ValueError, OSError) as error:
        print(f"Could not create account: {error}")


if __name__ == "__main__":
    main()
