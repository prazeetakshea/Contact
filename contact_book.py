import sqlite3

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


# ---------------- Contact Operations ----------------
def add_contact():
    print("\n--- Add New Contact ---")
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    email = input("Enter email (optional): ").strip()

    if not name or not phone:
        print("Error: Name and phone are required!\n")
        return

    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email or None)
        )
        conn.commit()
        print("Contact added successfully!\n")
    except sqlite3.IntegrityError:
        print("Error: Phone number already exists or invalid data.\n")
    finally:
        conn.close()


def list_all_contacts():
    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone, email FROM contacts ORDER BY name")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No contacts found.\n")
        return

    print("\n--- All Contacts ---")
    for row in rows:
        email = row[3] if row[3] else "(no email)"
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {email}")
    print()


def search_contacts():
    keyword = input("\nEnter name, phone, or email to search: ").strip()
    if not keyword:
        print("Search keyword cannot be empty.\n")
        return

    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    search_term = f"%{keyword}%"
    cur.execute("""
        SELECT id, name, phone, email FROM contacts 
        WHERE LOWER(name) LIKE LOWER(?) 
           OR LOWER(phone) LIKE LOWER(?) 
           OR LOWER(email) LIKE LOWER(?)
        ORDER BY name
    """, (search_term, search_term, search_term))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No contacts found matching your search.\n")
        return

    print(f"\n--- {len(rows)} Contact(s) Found ---")
    for row in rows:
        email = row[3] if row[3] else "(no email)"
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {email}")
    print()


def update_contact():
    list_all_contacts()  # Show contacts first to help user pick ID
    contact_id = input("\nEnter contact ID to update (or press Enter to cancel): ").strip()
    if not contact_id.isdigit():
        print("Invalid or cancelled.\n")
        return

    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    cur.execute("SELECT name, phone, email FROM contacts WHERE id = ?", (contact_id,))
    contact = cur.fetchone()

    if not contact:
        print("Contact ID not found.\n")
        conn.close()
        return

    print(f"\nCurrent: Name: {contact[0]}, Phone: {contact[1]}, Email: {contact[2] or '(none)'}")
    print("Leave field blank to keep current value.")

    new_name = input(f"New name [{contact[0]}]: ").strip()
    new_phone = input(f"New phone [{contact[1]}]: ").strip()
    new_email = input(f"New email [{contact[2] or '(none)'}]: ").strip()

    final_name = new_name if new_name else contact[0]
    final_phone = new_phone if new_phone else contact[1]
    final_email = new_email if new_email else contact[2]

    if final_name == contact[0] and final_phone == contact[1] and final_email == contact[2]:
        print("No changes made.\n")
        conn.close()
        return

    if not final_name or not final_phone:
        print("Error: Name and phone cannot be empty!\n")
        conn.close()
        return

    cur.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
        (final_name, final_phone, final_email or None, contact_id)
    )
    conn.commit()
    conn.close()
    print("Contact updated successfully!\n")


def delete_contact():
    list_all_contacts()
    contact_id = input("\nEnter contact ID to delete (or press Enter to cancel): ").strip()
    if not contact_id.isdigit():
        print("Invalid or cancelled.\n")
        return

    confirm = input("Are you sure you want to delete this contact? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.\n")
        return

    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    if cur.rowcount > 0:
        print("Contact deleted successfully!\n")
    else:
        print("Contact ID not found.\n")
    conn.commit()
    conn.close()


# ---------------- Main Menu ----------------
def main():
    init_db()
    print("Welcome to Contact Book!")

    while True:
        print("\n" + "="*30)
        print("1. Add Contact")
        print("2. Search Contacts")
        print("3. List All Contacts")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("="*30)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            list_all_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye! Thanks for using Contact Book.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.\n")


if __name__ == "__main__":
    main()