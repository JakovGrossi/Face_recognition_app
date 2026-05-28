import database as db
from recognizer import FaceRecognizer
from actions import register_user, run_recognition, delete_user

MENU = """
=== Face Recognition ===
  1  Register user
  2  Run live recognition
  3  Delete user
  4  Quit
"""

ACTIONS = {"1", "2", "3", "4"}


def main():
    db.init_db()
    model = FaceRecognizer()

    while True:
        print(MENU, end="")
        choice = input("Choice: ").strip()

        if choice not in ACTIONS:
            print("Invalid option.")
            continue

        if choice == "1":
            register_user(model)
        elif choice == "2":
            run_recognition(model)
        elif choice == "3":
            delete_user()
        elif choice == "4":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
