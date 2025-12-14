# Reflection 
# Lists and dictionaries both store data, but they solve different problems. Lists are great for keeping
# items in order and looping through multiple records, but they don’t clearly describe what each value
# represents unless you track indexes carefully. Dictionaries solve that issue by allowing data to be
# stored as key-value pairs, which keeps related information connected and readable.
#
# The most challenging part for me was working with dictionaries inside a list. While dictionaries are
# more powerful, they require accuracy with keys and structure. One small typo or mismatch in field
# names can cause logic errors, especially during editing and searching. That strictness made them more
# difficult than lists alone, but also more reliable once implemented correctly.
#
# I can see myself using lists of dictionaries in future projects like tracking inventory, logging
# expenses, managing study data, or building simple databases. This structure allows data to scale
# without becoming disorganized. One thing I want to explore further is saving and loading data using
# JSON files so information can persist between program runs and be reused later.

import json
from datetime import datetime

# Initialize database (list of dictionaries)
database = []


def add_item():
    item = {}
    item["Book"] = input("Enter name of Book: ").strip()
    item["Author"] = input("Enter name of Author: ").strip()
    item["Genre"] = input("Enter name of Genre: ").strip()

    if not item["Book"]:
        print("Book title cannot be empty.")
        return

    database.append(item)
    print("Book added successfully!")


def view_all():
    if not database:
        print("No books yet!")
        return

    for i, item in enumerate(database, 1):
        print(f"\n--- Book {i} ---")
        print(f"Book: {item.get('Book')}")
        print(f"Author: {item.get('Author')}")
        print(f"Genre: {item.get('Genre')}")


def search_items():
    if not database:
        print("No books in the database yet!")
        return

    search_term = input("Search for (title / author / genre): ").strip().lower()
    found = False

    for item in database:
        combined = f"{item.get('Book')} {item.get('Author')} {item.get('Genre')}".lower()
        if search_term in combined:
            print(f"- {item['Book']} by {item['Author']} ({item['Genre']})")
            found = True

    if not found:
        print("No items found.")


def _find_matches_by_title(search_title):
    matches = []
    for i, item in enumerate(database):
        if search_title in item.get("Book", "").lower():
            matches.append((i, item))
    return matches


def edit_item():
    if not database:
        print("No books to edit yet!")
        return

    search_title = input("Enter the Book title to edit: ").strip().lower()
    matches = _find_matches_by_title(search_title)

    if not matches:
        print("No books found with that title.")
        return

    print("\nMatching books:")
    for idx, (i, item) in enumerate(matches, 1):
        print(f"{idx}. {item['Book']} by {item['Author']} ({item['Genre']})")

    try:
        choice = int(input("\nEnter the number of the book to edit: ").strip())
        if not (1 <= choice <= len(matches)):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    index_to_edit, book = matches[choice - 1]

    print("\nWhich field do you want to edit?")
    for key in book.keys():
        print(f"- {key}")

    field_input = input("Enter field name exactly as shown: ").strip()

    if field_input not in book:
        print("Invalid field name.")
        return

    new_value = input(
        f"Enter new value for {field_input} (current: {book[field_input]}): "
    ).strip()

    if new_value:
        book[field_input] = new_value
        database[index_to_edit] = book
        print("Book updated successfully!")
    else:
        print("No change made.")


def delete_item():
    if not database:
        print("No books to delete yet!")
        return

    search_title = input("Enter the title of the Book to delete: ").strip().lower()
    matches = _find_matches_by_title(search_title)

    if not matches:
        print("No books found with that title.")
        return

    print("\nMatching books:")
    for idx, (i, item) in enumerate(matches, 1):
        print(f"{idx}. {item['Book']} by {item['Author']} ({item['Genre']})")

    try:
        choice = int(input("\nEnter the number of the book to delete: ").strip())
        if not (1 <= choice <= len(matches)):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    index_to_delete = matches[choice - 1][0]
    item_to_delete = database[index_to_delete]

    confirm = input(
        f"Type YES to confirm delete '{item_to_delete['Book']}': "
    ).strip().upper()

    if confirm == "YES":
        del database[index_to_delete]
        print("Book deleted successfully!")
    else:
        print("Delete cancelled.")


def search_by_genre():
    if not database:
        print("No books in the database yet!")
        return

    genre_search = input("Enter the Genre to search for: ").strip().lower()
    found = False

    print(f"\nBooks in Genre '{genre_search}':")
    for item in database:
        if genre_search in item.get("Genre", "").lower():
            print(f"- {item['Book']} by {item['Author']}")
            found = True

    if not found:
        print("No books found in that Genre.")


def export_to_file():
    if not database:
        print("No books to export yet!")
        return

    filename = f"books_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=2)
        print(f"Export complete: {filename}")
    except Exception as e:
        print(f"Export failed: {e}")


def main():
    while True:
        print("\n=== My Personal Database ===")
        print("1. Add new Book")
        print("2. View all Books")
        print("3. Search Book")
        print("4. Edit Book")
        print("5. Delete Book")
        print("6. Search by Genre")
        print("7. Export to file")
        print("8. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_items()
        elif choice == "4":
            edit_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_by_genre()
        elif choice == "7":
            export_to_file()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
