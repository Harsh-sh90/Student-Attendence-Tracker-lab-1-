# Name: Harsh Sharma
# Date: 18-11-2025
# Project Title: Contact Book
# Course: Programming for Problem Solving Using Python (ETCCPP171)

import csv
from importlib.resources import as_file
import json
import os
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
LOG_FILE = "error_log.txt"
FIELDS = ["name", "phone", "email"]
def write_error_log(task_name, problem_details):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now()}] Task: {task_name}\nProblem: {problem_details}\n{'-'*30}\n")
    except:
        print("Couldn't even write the error log file")
def get_contacts():
    if not os.path.exists(CSV_FILE):
        return []

    my_contacts = []
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                my_contacts.append(row)
    except Exception as e:
        print("Had a problem reading the contacts", e)
        write_error_log("Reading CSV File", str(e))
    return my_contacts
def save_contacts(current_contacts):
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader() 
            writer.writerows(current_contacts) 
    except Exception as e:
        print("couldn't save the contacts", e)
        write_error_log("Saving CSV File", str(e))


def add_contact():
    print("\n--- Add a Contact! ---")
    name = input("Type the Name: ").strip()
    phone = input("Type the Phone Number: ").strip()
    email = input("Type the Email: ").strip()

   
    if not name or not phone or not email:
        print(" fill in ALL the details")
        return

    new_contact = {"name": name, "phone": phone, "email": email}

    try:
        file_is_empty = not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if file_is_empty:
                writer.writeheader() 
            writer.writerow(new_contact)
        print(f"Contact '{name}' is saved.")
    except Exception as e:
        print("couldn't add the contact right now.")
        write_error_log("Adding Contact", str(e))
def show_contacts():
    print("\n--- Here is Your Contact List ---")
    all_contacts = get_contacts() 

    if not all_contacts:
        print("Your contact book is empty,Add some contact")
        try:
            result = 1 / 0 
        except Exception as e:
            write_error_log("Showing Contacts (Intentional Test)", str(e))
        return
    
def find_contact():
    print("\n--- search for a Contact ---")
    name_to_find = input("Type the name you want to find: ").strip().lower()
    all_contacts = get_contacts()

    found_one = False 

    for c in all_contacts:
        if c["name"].lower() == name_to_find:
            print(f"Found them Name: {c['name']}, Phone: {c['phone']}, Email: {c['email']}")
            found_one = True

    if not found_one:
        print("no contact was found with that name.")

def change_contact():
    print("\n--- Time to Update a Contact ---")
    name_to_update = input("Type the name to update: ").strip().lower()
    all_contacts = get_contacts()

    contact_updated = False 
    for c in all_contacts:
        if c["name"].lower() == name_to_update:
            print(f"found this contact: {c['name']} | {c['phone']} | {c['email']}")
            new_phone = input("New Phone (Hit Enter to keep the old one): ").strip()
            new_email = input("New Email (Hit Enter to keep the old one): ").strip()

            if new_phone:
                c["phone"] = new_phone
            if new_email:
                c["email"] = new_email
            save_contacts(all_contacts)
            print("Contact info has been successfully updated")
            contact_updated = True
            break 

    if not contact_updated:
        print("couldn't find a contact with that name to update")
def remove_contact():
    print("\n---Delete a Contact ---")
    name_to_delete = input("Type the name to delete: ").strip().lower()
    all_contacts = get_contacts()

    initial_count = len(all_contacts)
    new_contact_list = [c for c in all_contacts if c["name"].lower() != name_to_delete]

    final_count = len(new_contact_list) 

    if final_count == initial_count:
        print(" I couldn't find a contact with that name to delete")
    else:
        save_contacts(new_contact_list)
        print("Contact deleted successfully.")
def backup_to_json():
    all_contacts = get_contacts()
    if not all_contacts:
        print("The list is empty.")
        return
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(all_contacts, f, indent=4)
        print(f"Contacts saved as a backup to {JSON_FILE}.")
    except Exception as e:
        print("Error while trying to backup to JSON.")
        write_error_log("Backup to JSON", str(e))
def restore_from_json():
    print("\n--- Try to Load Contacts from JSON Backup ---")
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            contacts_from_json = json.load(f)

        if not contacts_from_json:
            print("The JSON file is empty, nothing to load.")
            return

        print("--- Contacts found in the JSON file: ---")
        for c in contacts_from_json:
            print(f"Name: {c['name']}, Phone: {c['phone']}, Email: {c['email']}")
        print(f"Total Contacts loaded from JSON: {len(contacts_from_json)}")

    except FileNotFoundError:
        print("I can't find the JSON backup file.")
    except Exception as e:
        print("Something went wrong while reading the JSON file.")
        write_error_log("Restoring from JSON", str(e))
        
def start_main():
    print("-" * 45)
    print("Welcome to My Contact Book App")
    print("-" * 45)

    while True:
        print("\nWhat do you want to do?")
        print("1. Add a New Contact")
        print("2. Show My Contacts List")
        print("3. Search for a Contact")
        print("4. Change a Contact's Info")
        print("5. Delete a Contact")
        print("6. Backup Contacts to JSON")
        print("7. View JSON Backup") 
        print("8. Exit the Program")

        choice = input("Type your choice number (1-8): ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            find_contact()
        elif choice == "4":
            change_contact()
        elif choice == "5":
            remove_contact()
        elif choice == "6":
            backup_to_json()
        elif choice == "7":
            restore_from_json()
        elif choice == "8":
            print("Thanks for using the Contact Book!")
            break 
        else:
            print("That's not a valid number. Pick a number from 1 to 8")
if __name__ == "__main__":
    start_main()