import mysql.connector
from datetime import date

# ---------- DATABASE CONFIG ----------
DB_HOST = "localhost"                           #SELECT Host FROM mysql.user;
DB_USER = "root"                                #SELECT User FROM mysql.user;
DB_PASSWORD = "22446688"
DB_NAME = "hotel"

# ---------- CONNECT TO MYSQL ----------
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ---------- SETUP DATABASE AND TABLE ----------
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(15),
            room_no INT,
            check_in DATE,
            check_out DATE
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database and table are ready!\n")

# ---------- CRUD FUNCTIONS ----------
def add_guest():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter guest name: ")
    phone = input("Enter phone number: ")
    room_no = input("Enter room number: ")
    check_in = input("Enter check-in date (YYYY-MM-DD): ")
    check_out = input("Enter check-out date (YYYY-MM-DD): ")

    query = """INSERT INTO guests (name, phone, room_no, check_in, check_out)
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (name, phone, room_no, check_in, check_out))
    conn.commit()
    conn.close()
    print("✅ Guest added successfully!\n")


def view_guests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No guests found.\n")
        return

    print("\n--- Guest List ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Room: {row[3]}, Check-in: {row[4]}, Check-out: {row[5]}")
    print()


def update_guest():
    conn = get_connection()
    cursor = conn.cursor()
    guest_id = input("Enter Guest ID to update: ")

    name = input("New name (leave blank to skip): ")
    phone = input("New phone (leave blank to skip): ")
    room_no = input("New room number (leave blank to skip): ")

    fields = []
    values = []
    if name:
        fields.append("name=%s")
        values.append(name)
    if phone:
        fields.append("phone=%s")
        values.append(phone)
    if room_no:
        fields.append("room_no=%s")
        values.append(room_no)

    if not fields:
        print("⚠ No fields to update.\n")
        conn.close()
        return

    query = f"UPDATE guests SET {', '.join(fields)} WHERE id=%s"
    values.append(guest_id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    print("✅ Guest updated successfully!\n")


def delete_guest():
    conn = get_connection()
    cursor = conn.cursor()
    guest_id = input("Enter Guest ID to delete: ")

    cursor.execute("DELETE FROM guests WHERE id=%s", (guest_id,))
    conn.commit()
    conn.close()
    print("🗑 Guest deleted successfully!\n")

# ---------- MAIN MENU ----------
def main():
    setup_database()

    while True:
        print("=== Hotel Management System ===")
        print("1. Add Guest")
        print("2. View Guests")
        print("3. Update Guest")
        print("4. Delete Guest")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_guest()
        elif choice == "2":
            view_guests()
        elif choice == "3":
            update_guest()
        elif choice == "4":
            delete_guest()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()

