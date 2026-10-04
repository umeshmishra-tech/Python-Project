import csv
from datetime import datetime
import os

FILENAME = "subjects_data.csv"

def load_data():
    subjects = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['units'] = int(row['units'])
                row['difficulty'] = int(row['difficulty'])
                row['logged_hours'] = float(row['logged_hours'])
                subjects.append(row)
    return subjects

def save_data(subjects):
    with open(FILENAME, mode='w', newline='') as file:
        fieldnames = ['name', 'exam_date', 'units', 'difficulty', 'logged_hours']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(subjects)

def add_subject(subjects):
    name = input("\nEnter subject name: ").strip()
    
    while True:
        date_str = input("Enter exam date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            
    while True:
        try:
            units = int(input("Enter number of syllabus units: "))
            if units <= 0:
                print("Units must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            difficulty = int(input("Enter difficulty rating (1-10): "))
            if 1 <= difficulty <= 10:
                break
            else:
                print("Difficulty must be between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

    subjects.append({
        'name': name,
        'exam_date': date_str,
        'units': units,
        'difficulty': difficulty,
        'logged_hours': 0.0
    })
    print(f"\nSuccess: Subject '{name}' added successfully.")

def generate_schedule(subjects):
    if not subjects:
        print("\nNo subjects available. Please add subjects first.")
        return

    while True:
        try:
            available_hours = float(input("\nEnter available daily study hours: "))
            if available_hours > 0:
                break
            print("Error: Study hours must be greater than 0 to generate a schedule.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    today = datetime.today()
    total_priority = 0
    priorities = []

    # COMPUTATIONAL FEATURE: Ranking & Proportional Allocation
    for sub in subjects:
        exam_date = datetime.strptime(sub['exam_date'], "%Y-%m-%d")
        days_remaining = (exam_date - today).days
        
        # Prevent dividing by zero if the exam is today or in the past
        days_remaining = max(days_remaining, 1) 
        
        # Priority algorithm: Higher difficulty + closer exam = higher priority
        priority_score = sub['difficulty'] + (30 / days_remaining)
        priorities.append((sub['name'], priority_score))
        total_priority += priority_score

    print("\n--- Smart Daily Schedule ---")
    print(f"{'Subject':<15} | {'Allocated Time'}")
    print("-" * 35)
    
    for name, p_score in priorities:
        allocated_time = (p_score / total_priority) * available_hours
        print(f"{name:<15} | {allocated_time:.2f} hours")
    print("-" * 35)

def log_hours(subjects):
    if not subjects:
        print("\nNo subjects available.")
        return

    print("\nAvailable Subjects:")
    for i, sub in enumerate(subjects, 1):
        print(f"{i}. {sub['name']}")
        
    while True:
        try:
            choice = int(input("\nSelect a subject number to log hours: "))
            if 1 <= choice <= len(subjects):
                selected_sub = subjects[choice - 1]
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            hours = float(input(f"Enter hours studied for {selected_sub['name']}: "))
            if hours > 0:
                selected_sub['logged_hours'] += hours
                print(f"Success: {hours} hours logged for {selected_sub['name']}. File updated.")
                break
            print("Hours must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

def view_report(subjects):
    if not subjects:
        print("\nNo subjects available.")
        return

    print("\n--- Progress Report ---")
    print(f"{'Subject':<15} | {'Units':<5} | {'Logged Hours':<15} | {'Status'}")
    print("-" * 55)
    
    for sub in subjects:
        # Simple analysis: Assumes 2 hours of study needed per syllabus unit
        target_hours = sub['units'] * 2
        
        if sub['logged_hours'] < (target_hours / 2):
            status = "Behind Schedule"
        elif sub['logged_hours'] >= target_hours:
            status = "Ahead of Schedule"
        else:
            status = "On Track"
            
        print(f"{sub['name']:<15} | {sub['units']:<5} | {sub['logged_hours']:<15.1f} | {status}")
    print("-" * 55)

def main():
    subjects = load_data()
    
    while True:
        print("\n=== Smart Revision and Exam Planner ===")
        print("1. Add Subject")
        print("2. Generate Smart Schedule")
        print("3. Log Study Hours")
        print("4. View Progress Report")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_subject(subjects)
        elif choice == '2':
            generate_schedule(subjects)
        elif choice == '3':
            log_hours(subjects)
        elif choice == '4':
            view_report(subjects)
        elif choice == '5':
            save_data(subjects)
            print("\nData saved successfully. Exiting the program. Good luck with your exams!")
            break
        else:
            print("\nInvalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    main()