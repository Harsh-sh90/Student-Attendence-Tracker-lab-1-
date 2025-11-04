import json
import os
import csv
from datetime import date, datetime, timedelta
from collections import defaultdict

# --- Constants ---
DATA_FILE = "attendance_data.json"
BACKUP_FILE = "attendance_data_backup.json"
VALID_STATUSES = ["present", "absent", "late"]

# --- Classes for Better Organization ---

class Student:
    def __init__(self, name):
        self.name = name
        self.records = []  # List of {"date": "YYYY-MM-DD", "status": "present/absent/late"}

    def add_record(self, date_str, status):
        # Check if record already exists for the date
        for record in self.records:
            if record["date"] == date_str:
                record["status"] = status
                return True
        self.records.append({"date": date_str, "status": status})
        self.records.sort(key=lambda x: x["date"])
        return True

    def get_attendance_count(self, start_date=None, end_date=None):
        filtered_records = self.records
        if start_date and end_date:
            filtered_records = [r for r in self.records if start_date <= r["date"] <= end_date]
        counts = defaultdict(int)
        for record in filtered_records:
            counts[record["status"]] += 1
        total_days = len(filtered_records)
        return dict(counts), total_days

    def get_percentage(self, total_possible_days):
        present_count = sum(1 for r in self.records if r["status"] == "present")
        return (present_count / total_possible_days * 100) if total_possible_days > 0 else 0

class AttendanceTracker:
    def __init__(self):
        self.students = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    for name, info in data.items():
                        student = Student(name)
                        if "records" in info:
                            student.records = info["records"]
                        elif "attendance" in info:  # Backward compatibility
                            for d in info["attendance"]:
                                student.add_record(d, "present")
                        self.students[name] = student
                print("Data loaded successfully.")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading data: {e}. Attempting to load backup.")
                if os.path.exists(BACKUP_FILE):
                    try:
                        with open(BACKUP_FILE, "r") as f:
                            data = json.load(f)
                            # Similar loading logic
                            for name, info in data.items():
                                student = Student(name)
                                if "records" in info:
                                    student.records = info["records"]
                                self.students[name] = student
                        print("Backup data loaded.")
                    except:
                        print("Backup also corrupted. Starting fresh.")
                        self.students = {}
                else:
                    print("No backup found. Starting fresh.")
                    self.students = {}
        else:
            self.students = {}

    def save_data(self):
        try:
            data = {name: {"records": student.records} for name, student in self.students.items()}
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
            # Create backup
            with open(BACKUP_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print("Data saved successfully.")
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_student(self, name):
        if not name:
            print("Error: Name cannot be empty.")
            return False
        if name in self.students:
            print(f"Error: Student '{name}' already exists.")
            return False
        self.students[name] = Student(name)
        print(f"Student '{name}' added successfully.")
        self.save_data()
        return True

    def mark_attendance(self, name, date_str, status):
        if name not in self.students:
            print(f"Error: Student '{name}' not found.")
            return False
        if status not in VALID_STATUSES:
            print(f"Error: Invalid status. Choose from {VALID_STATUSES}.")
            return False
        try:
            date.fromisoformat(date_str)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return False
        if self.students[name].add_record(date_str, status):
            print(f"Attendance marked for '{name}' on {date_str} as {status}.")
            self.save_data()
            return True

    def search_student(self, name):
        if name in self.students:
            student = self.students[name]
            print(f"\n--- Attendance Record for {name} ---")
            if not student.records:
                print("No records found.")
                return
            counts, total = student.get_attendance_count()
            print(f"Total records: {total}")
            print(f"Present: {counts.get('present', 0)}, Absent: {counts.get('absent', 0)}, Late: {counts.get('late', 0)}")
            print("Records:")
            for record in student.records:
                print(f"  {record['date']}: {record['status']}")
        else:
            print(f"Student '{name}' not found.")

    def delete_student(self, name):
        if name not in self.students:
            print(f"Error: Student '{name}' not found.")
            return False
        confirm = input(f"Delete '{name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.students[name]
            print(f"Student '{name}' deleted.")
            self.save_data()
            return True
        print("Deletion cancelled.")
        return False

    def view_all_students(self):
        print("\n--- All Students Summary ---")
        if not self.students:
            print("No students.")
            return
        for name, student in self.students.items():
            counts, total = student.get_attendance_count()
            print(f"{name}: Total {total}, Present {counts.get('present', 0)}, Absent {counts.get('absent', 0)}, Late {counts.get('late', 0)}")

    def count_attendance(self, start_date=None, end_date=None):
        print("\n--- Attendance Count ---")
        total_present = total_absent = total_late = 0
        for student in self.students.values():
            counts, _ = student.get_attendance_count(start_date, end_date)
            total_present += counts.get('present', 0)
            total_absent += counts.get('absent', 0)
            total_late += counts.get('late', 0)
        print(f"Overall: Present {total_present}, Absent {total_absent}, Late {total_late}")
        if start_date and end_date:
            print(f"For period {start_date} to {end_date}")

    def view_by_date(self, date_str):
        print(f"\n--- Attendance on {date_str} ---")
        found = False
        for name, student in self.students.items():
            for record in student.records:
                if record["date"] == date_str:
                    print(f"{name}: {record['status']}")
                    found = True
                    break
        if not found:
            print("No records for this date.")

    def export_to_csv(self, filename="attendance_export.csv"):
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Student", "Date", "Status"])
                for name, student in self.students.items():
                    for record in student.records:
                        writer.writerow([name, record["date"], record["status"]])
            print(f"Data exported to {filename}")
        except IOError as e:
            print(f"Error exporting: {e}")

# --- Menu and Main Loop ---

def print_menu():
    print("\n===== Enhanced Student Attendance Tracker =====")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. View All Summary")
    print("6. Count Attendance")
    print("7. View by Date")
    print("8. Export to CSV")
    print("9. Exit")
    print("================================================")

def get_date_input(prompt, default_today=True):
    today_str = date.today().isoformat()
    date_str = input(f"{prompt} [default: {today_str}]: ").strip()
    if not date_str and default_today:
        return today_str
    return date_str

def main():
    tracker = AttendanceTracker()
    try:
        while True:
            print_menu()
            choice = input("Enter choice (1-9): ").strip()
            if choice == '1':
                name = input("Enter student's full name: ").strip().title()
                tracker.add_student(name)
            elif choice == '2':
                name = input("Enter student's name: ").strip().title()
                date_str = get_date_input("Enter date (YYYY-MM-DD)")
                status = input(f"Enter status ({'/'.join(VALID_STATUSES)}): ").strip().lower()
                tracker.mark_attendance(name, date_str, status)
            elif choice == '3':
                name = input("Enter student's name: ").strip().title()
                tracker.search_student(name)
            elif choice == '4':
                name = input("Enter student's name: ").strip().title()
                tracker.delete_student(name)
            elif choice == '5':
                tracker.view_all_students()
            elif choice == '6':
                start = get_date_input("Start date (YYYY-MM-DD)", default_today=False)
                end = get_date_input("End date (YYYY-MM-DD)", default_today=False)
                tracker.count_attendance(start or None, end or None)
            elif choice == '7':
                date_str = get_date_input("Enter date to view")
                tracker.view_by_date(date_str)
            elif choice == '8':
                filename = input("Enter filename [default: attendance_export.csv]: ").strip()
                if not filename:
                    filename = "attendance_export.csv"
                tracker.export_to_csv(filename)
            elif choice == '9':
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nInterrupted. Saving data...")
        tracker.save_data()
        print("Data saved. Exiting.")

if __name__ == "__main__":
    main()


