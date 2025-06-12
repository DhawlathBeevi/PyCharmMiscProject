import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
import mysql.connector
import os  # Added for file path handling

# Function to validate phone number using API
def validate_phone_number(api_key, phone_number):
    try:
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={phone_number}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("API Response:", data)

        if 'valid' in data and data['valid']:
            return {
                "phone": data['phone'],
                "country": data['country']['name'],
                "location": data['location'],
                "carrier": data['carrier'],
                "line_type": data['type']
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to reach the API.\n{str(e)}"

# Function to insert validated data into the database
def insert_into_database(phone_data):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phone_validation"
        )
        cursor = connection.cursor()
        query = """
        INSERT INTO phone_record (phone_number, country, location, carrier, line_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            phone_data['phone'],
            phone_data['country'],
            phone_data['location'],
            phone_data['carrier'],
            phone_data['line_type']
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return "Phone number data inserted into the database successfully."
    except mysql.connector.Error as e:
        return f"Database Error: {e}"

# Function to display the main app page after successful login
def open_main_app():
    root.destroy()
    main_app = tk.Tk()
    main_app.title("Phone Number Validator")
    main_app.geometry("1275x1275")

    try:
            bg_image = PhotoImage(file=r"C:\Users\jahab\Desktop\Python\Track.png")
            bg_label = tk.Label(main_app, image=bg_image)
            bg_label.image = bg_image  # Prevent garbage collection
            bg_label.place(relheight=1, relwidth=1)
    except Exception as e:
        bg_label = tk.Label(main_app, text=f"Background Image Missing: {str(e)}", font=('Arial', 14), bg='#D9D9D9')
        bg_label.place(relheight=1, relwidth=1)

    text_label = tk.Label(main_app, text='Welcome to My App', font=('Georgia', 14), bg='#D9D9D9', fg='black')
    text_label.pack(pady=20)

    tk.Label(main_app, text="Enter Phone Number:", font=('Arial', 12), bg='#D9D9D9').pack(pady=10)
    phone_entry = tk.Entry(main_app, font=('Arial', 12))
    phone_entry.pack(pady=5)

    result_label = tk.Label(main_app, text="", font=('Arial', 12), bg='#D9D9D9', fg='black', wraplength=600)
    result_label.pack(pady=20)

    def handle_phone_validation():
        phone_number = phone_entry.get().strip()
        if not phone_number.startswith('+'):
            result_label.config(text="Error: Phone number must start with '+'.")
            return

        api_key = "608dccbff47447ccbcd78f125061bad6"  # Replace with your API key
        phone_data = validate_phone_number(api_key, phone_number)

        if isinstance(phone_data, dict):
            db_result = insert_into_database(phone_data)
            result_label.config(text=f"Phone validation successful:\n"
                                     f"Phone Number: {phone_data['phone']}\n"
                                     f"Country: {phone_data['country']}\n"
                                     f"Location: {phone_data['location']}\n"
                                     f"Carrier: {phone_data['carrier']}\n"
                                     f"Line Type: {phone_data['line_type']}\n\n"
                                     f"{db_result}")
        else:
            result_label.config(text="Invalid phone number or no data available.")

    validate_button = tk.Button(main_app, text="Validate Phone", command=handle_phone_validation,
                                font=('Arial', 12), bg='#4CAF50', fg='white')
    validate_button.pack(pady=10)

    main_app.mainloop()

# Function to handle the login action
def login_action():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if username == "dh" and password == "26":
        open_main_app()
    else:
        messagebox.showwarning("Login Failed", "Invalid Username or Password")

# Create the main window (Login Page)
root = tk.Tk()
root.title("Login Page")
root.geometry("1275x1275")

frame = tk.Frame(root, bg='#1c1c1c', padx=20, pady=20)
frame.pack(expand=True)

label_style = {"bg": "#1c1c1c", "fg": "#ffffff", "font": ("Arial", 12)}
entry_style = {"bg": "#3a3a3a", "fg": "#ffffff", "font": ("Arial", 12)}

tk.Label(frame, text="Username:", **label_style).grid(row=0, column=0, sticky='w', pady=10)
username_entry = tk.Entry(frame, **entry_style)
username_entry.grid(row=0, column=1)

tk.Label(frame, text="Password:", **label_style).grid(row=1, column=0, sticky='w', pady=10)
password_entry = tk.Entry(frame, show='*', **entry_style)
password_entry.grid(row=1, column=1)

login_button = tk.Button(frame, text="Login", bg="#4CAF50", fg="#ffffff", font=("Arial", 12),
                         padx=10, pady=5, command=login_action)
login_button.grid(row=2, columnspan=2, pady=20)

root.mainloop()