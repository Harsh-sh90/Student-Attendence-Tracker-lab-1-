# Name: Harsh Sharma
# Roll No: 2501940054
# Date: 09-11-2025
# Assignment: 01 - Python-based Command-Line Attendance Tracker

import datetime

def main():

    print("===========================================")
    print("         K.R. Mangalam University")
    print("===========================================")
    print("         Welcome to Attendance Tracker     \n")

    attendance_data = {}    # Number of student will be added here

    while True:                                                     # checks the entry if its empty will show invalid
        try:
            students = int(input(" Total number of students in the class: "))
            if students < 0:
                print("Total students cannot be negative.")
            else:
                break
        except ValueError:
            print("Invalid entry.")

    while True:                      # checks if student is present or not
        try:
            num_entries = int(input("Number of students present today? "))
            if num_entries < 0:
                print("present student cant be negative.")
            elif num_entries > students:
                print(f"You entered more than the class strength ({students}).")
            else:
                break
        except ValueError:
            print("Invalid number.")

    print(f"\n Let’s record attendance for {num_entries} student(s).")

    for i in range(num_entries):
        print(f"\nStudent {i + 1}:")
        
        while True:
            name = input("Enter student name: ").strip().title()
            if not name:
                print("Name cannot be empty")
            elif name in attendance_data:
                print("student is already present.")     # will show if the student is already present
            else:
                break
        
        while True:
            time_s = input("Enter arrival (e.g., 09:10 AM): ").strip().upper()
            if not time_s:
                print(" Time cannot be blank.")
            else:
                break
        
        attendance_data[name] = time_s

    print("\n===========================================")
    print("              Attendance Summary")
    print("===========================================")
    print(f"Student Name\t\tCheck-in Time")
    print("-------------------------------------------")

    for name, time in attendance_data.items():
        if len(name) < 16:
            print(f"{name}\t\t{time}")
        else:
            print(f"{name}\t{time}")

    present = len(attendance_data)
    absent = students - present

    print("\n-------------------------------------------")
    print(f"Total Present : {present}")                               # will return how many present or absent
    print(f"Total Absent  : {absent}")
    print("===========================================\n")

    while True:
        save_choice = input("Do you want to save this report? (yes/no): ").strip().lower()
        if save_choice in ["yes", "y", "no", "n"]:
            break
        print("Please answer yes or no.")

    if save_choice in ["yes", "y"]:
        try:
            report_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")    # to save the report in csv file
            with open("attendance_log.txt", "w") as f:
                f.write("============= Attendance Report =============\n")
                f.write(f"Generated On: {report_time}\n\n")
                f.write("Student Name\t\tCheck-in Time\n")
                f.write("-------------------------------------------\n")
                for name, time in attendance_data.items():
                    if len(name) < 16:
                        f.write(f"{name}\t\t{time}\n")
                    else:
                        f.write(f"{name}\t{time}\n")
                f.write("\n-------------------------------------------\n")
                f.write(f"Total Present: {present}\n")
                f.write(f"Total Absent:  {absent}\n")
                f.write(f"Class Strength: {students}\n")
                f.write("=============================================\n")

            print("\n Report successfully saved as 'attendance_log.txt'\n")
        except:
            print("\n This report can't be saved.\n")

    print("Thank you for using the Attendance Tracker! ")

if __name__ == "__main__":
    main()

