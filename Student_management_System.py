import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier 
class StudentManager:
    def __init__(self):
        try:
            with open("StudentData.json", "r") as f:
                self.students = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = []
    def save_data(self):
        with open("StudentData.json", "w") as f:
            json.dump(self.students, f, indent=4)
    def find_student(self, roll):
        for s in self.students:
            if s["roll"] == roll:
                return s
        return None
    def calculate_grade(self, marks):
        if marks >= 90:
            return "A"
        elif marks >= 75:
            return "B"
        elif marks >= 50:
            return "C"
        else:
            return "Fail"
    def add_student(self):
        name = input("Enter name: ").strip()
        try:
            roll = int(input("Enter roll number: "))
        except ValueError:
            print("Invalid roll number")
            return
        if self.find_student(roll):
            print("Roll already exists")
            return
        try:
            marks = int(input("Enter marks: "))
        except ValueError:
            print("Invalid marks")
            return
        if not (0 <= marks <= 100):
            print("Marks must be between 0-100")
            return
        self.students.append({
            "name": name,
            "roll": roll,
            "marks": marks
        })
        self.save_data()
        print("Student added successfully")
    def view_students(self):
        if not self.students:
            print("No data available")
            return
        print("\n--- Student List ---")
        for s in self.students:
            print(f"{s['name']} | Roll: {s['roll']} | Marks: {s['marks']}")
    def search_student(self):
        try:
            roll = int(input("Enter roll number: "))
        except ValueError:
            print("Invalid input")
            return
        s = self.find_student(roll)
        if s:
            print(f"Name: {s['name']:<10} | Roll: {s['roll']:<5} | Marks: {s['marks']}")
        else:
            print("Student not found")
    def update_marks(self):
        try:
            roll = int(input("Enter roll number: "))
        except ValueError:
            print("Invalid input")
            return
        s = self.find_student(roll)
        if not s:
            print("Student not found")
            return
        try:
            new_marks = int(input("Enter new marks: "))
        except ValueError:
            print("Invalid marks")
            return
        if not (0 <= new_marks <= 100):
            print("Marks must be between 0-100")
            return
        s["marks"] = new_marks
        self.save_data()
        print("Marks updated successfully")
    def delete_student(self):
        try:
            roll = int(input("Enter roll number: "))
        except ValueError:
            print("Invalid input")
            return
        s = self.find_student(roll)
        if not s:
            print("Student not found")
            return
        self.students.remove(s)
        self.save_data()
        print("Student deleted successfully")
    def analytics(self):
        if not self.students:
            print("No data available")
            return
        df = pd.DataFrame(self.students)
        print("\n--- Analytics ---")
        print("Total Students:", len(self.students))
        print(f"Average Marks: {df['marks'].mean():.2f}")
        print(f"Max: {df['marks'].max()} | Min: {df['marks'].min()}")
        df['grade'] = df['marks'].apply(self.calculate_grade)
        print("\n--- Grades ---")
        print(df[['name', 'marks', 'grade']].to_string(index=False))
        counts = df['grade'].value_counts().sort_index()
        counts.plot(kind="bar")
        plt.title("Grade Distribution")
        plt.xlabel("Grades")
        plt.ylabel("Number of Students")
        plt.show()
    def predict_grade(self):
        if len(self.students) < 2:
            print("Not enough data")
            return
        df = pd.DataFrame(self.students)
        df['grade'] = df['marks'].apply(self.calculate_grade)
        X = df[['marks']]
        y = df['grade']
        model = DecisionTreeClassifier()
        model.fit(X, y)
        try:
            marks = int(input("Enter marks: "))
        except ValueError:
            print("Invalid input")
            return
        input_df = pd.DataFrame([[marks]], columns=['marks'])
        prediction = model.predict(input_df)
        print("Predicted Grade:", prediction[0])
    def menu(self):
        while True:
            print("\n1. Add Student")
            print("2. View Students") 
            print("3. Search Student") 
            print("4. Update Marks") 
            print("5. Delete Student") 
            print("6. Analytics") 
            print("7. Predict Grade") 
            print("8. Exiting program. Thank you!")
            choice = input("Enter choice: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_marks()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                self.analytics()
            elif choice == "7":
                self.predict_grade()
            elif choice == "8":
                print("Exiting program")
                break
            else:
                print("Invalid choice")
if __name__ == "__main__":
    std = StudentManager()
    std.menu()