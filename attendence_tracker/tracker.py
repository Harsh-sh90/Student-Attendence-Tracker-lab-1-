# tracker.py
# Name: [Your Name]
# Date: 07-11-2025
# Assignment: 01 - Command-Line Attendance Tracker

import datetime

def main():
    """
    Main function to run the attendance tracker.
    """
    
    # Task 1: Welcome Message 
    print("===========================================")
    print(" K.R. Mangalam University Attendance Tracker")
    print("===========================================")
    print("This tool helps you record student attendance.\n")

    # Dictionary to store attendance 
    attendance_data = {}

    # Task 5: Absentee Validation (Optional)
    while True:
        try:
            total_students = int(input("Enter the total number of students in the class: "))
            if total_students < 0:
                print("Total students cannot be a negative number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Task 2: Input & Data Collection 
    while True:
        try:
            num_entries = int(input("How many students do you want to mark present? "))
            if num_entries < 0:
                print("Number of entries cannot be negative. Please try again.")
            elif num_entries > total_students:
                print(f"Entries cannot exceed total students ({total_students}). Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print(f"\nPlease enter data for {num_entries} student(s)...")

    # Use a loop to collect data
    for i in range(num_entries):
        print(f"\n--- Entry {i + 1} ---")
        
        # --- Task 3: Data Validation ---
        
        # Validate Name (Blank and Duplicate)
        while True:
            name = input("Enter student name: ").strip().title()
            
            if not name:
                print("! ERROR: Name cannot be empty. Please re-enter.")
            elif name in attendance_data:
                print("! ERROR: This student's attendance has already been recorded.")
            else:
                break
                
        # Validate Timestamp (Blank)
        while True:
            timestamp = input(f"Enter check-in time (e.g., 09:15 AM): ").strip().upper()
            
            if not timestamp:
                print("! ERROR: Timestamp cannot be missing. Please re-enter the time.")
            else:
                break
        
        # Store valid data in the dictionary 
        attendance_data[name] = timestamp

    # --- Task 4 & 5: Attendance Summary Generation --- [cite: 61, 67]
    
    print("\n\n===========================================")
    print("      *** Attendance Summary ***")
    print("===========================================")
    
    # Use f-strings and \t for formatting [cite: 63, 65]
    print(f"Student Name\t\tCheck-in Time\n{'-'*35}")
    
    for name, time in attendance_data.items():
        # Using \t for alignment. Assumes names are not excessively long.
        if len(name) < 16:
            print(f"{name}\t\t{time}")
        else:
            print(f"{name}\t{time}")

    print("\n-------------------------------------------")
    
    # Calculate present and absent counts [cite: 64, 69]
    present_count = len(attendance_data)
    absent_count = total_students - present_count
    
    print(f"Total Students Present:\t{present_count}")
    print(f"Total Students Absent:\t{absent_count}")
    print("===========================================\n")

    # --- Task 6 (Bonus): Save Attendance Report to File ---
    
    while True:
        save_choice = input("Do you wish to save this report to a file? (yes/no): ").strip().lower()
        if save_choice in ['yes', 'y', 'no', 'n']:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    if save_choice in ['yes', 'y']:
        try:
            # Use datetime module 
            report_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            
            with open("attendance_log.txt", "w") as f:
                f.write("=====================================\n")
                f.write("   KRMU ATTENDANCE LOG\n")
                f.write("=====================================\n")
                f.write(f"Report Generated: {report_time}\n\n")
                
                f.write("--- Present Students ---\n")
                f.write(f"Student Name\t\tCheck-in Time\n{'-'*35}\n")
                
                # Write student names and timestamps
                for name, time in attendance_data.items():
                    if len(name) < 16:
                        f.write(f"{name}\t\t{time}\n")
                    else:
                        f.write(f"{name}\t{time}\n")
                
                f.write("\n--- Summary Counts ---\n")
                # Write present and absent count
                f.write(f"Total Present:\t{present_count}\n")
                f.write(f"Total Absent:\t{absent_count}\n")
                f.write(f"Total Strength:\t{total_students}\n")
                f.write("=====================================\n")
            
            print(f"\nSuccessfully saved report to 'attendance_log.txt'.")
        except Exception as e:
            print(f"\n! ERROR: Could not save file. {e}")
            
    print("\nThank you for using the Attendance Tracker.")

if __name__ == "__main__":
    main()