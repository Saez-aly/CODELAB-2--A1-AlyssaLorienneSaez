# -------------------------------------------------------------
# STUDENT MANAGER PROGRAM - EXTENDED VERSION
# Description:
# A comprehensive student record manager using Tkinter GUI.
# Features: View, Sort, Add, Delete, and Update student records
# -------------------------------------------------------------
# Sources/References:
# - Tkinter documentation: https://docs.python.org/3/library/tkinter.html
# - ComboBox style examples: https://tkdocs.com/tutorial/widgets.html
# - File I/O handling: https://docs.python.org/3/tutorial/inputoutput.html
# - Lambda functions for sorting: https://docs.python.org/3/howto/sorting.html
# - Toplevel windows: https://www.geeksforgeeks.org/python-tkinter-toplevel-widget/
# -------------------------------------------------------------
# honestly this took me forever to figure out but i got it working!!
# the hardest part was making sure the file saves properly every time
# -------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox

class StudentManager:
    def __init__(self, root):
        """Initialize window, data list, and setup the UI.
        
        This is the constructor - runs when you create a StudentManager object.
        I set the file path here as a class variable so I can use it anywhere.
        Source: https://docs.python.org/3/tutorial/classes.html#class-objects
        """
        self.root = root
        self.root.title("Student Manager - Extended")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1D252D")  # dark mode theme
        self.students = []  # list to store all student data as dictionaries
        
        # storing file path as instance variable - the 'r' prefix means raw string
        self.file_path = r"C:\Users\saeza\OneDrive\Desktop\A1 Advanced Programming\Exercise 3\database.txt"
        
        self.load_students()
        self.setup_ui()

    # -------------------------------------------------------------
    # Function: load_students
    # Purpose: Read student details from file and store in list
    # Source for file handling: https://www.w3schools.com/python/python_file_handling.asp
    # -------------------------------------------------------------
    def load_students(self):
        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
            
            # Skip header line if it contains a number
            if lines and lines[0].strip().isdigit():
                lines = lines[1:]
            
            self.students = []
            
            for line in lines:
                data = line.strip().split(',')  # split by comma
                
                if len(data) >= 6:
                    # using dict instead of list - easier to access by name
                    self.students.append({
                        'id': data[0],
                        'name': data[1],
                        'course_marks': list(map(int, data[2:5])),  # convert to int
                        'exam_mark': int(data[5])
                    })
        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

    # -------------------------------------------------------------
    # Function: save_students
    # Purpose: Write all student data back to file
    # This is CRITICAL for persistence - without this changes are lost!
    # Source: https://realpython.com/read-write-files-python/
    # -------------------------------------------------------------
    def save_students(self):
        try:
            with open(self.file_path, "w") as f:  # 'w' overwrites the file
                f.write(f"{len(self.students)}\n")
                
                for s in self.students:
                    marks = ','.join(map(str, s['course_marks']))
                    f.write(f"{s['id']},{s['name']},{marks},{s['exam_mark']}\n")
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save to file: {e}")
            return False

    # -------------------------------------------------------------
    # Function: calculate_results
    # Purpose: Compute total, percentage, and grade for a student
    # -------------------------------------------------------------
    def calculate_results(self, s):
        total_coursework = sum(s['course_marks'])  # max 60
        total = total_coursework + s['exam_mark']  # max 160
        percent = (total / 160) * 100
        
        # loop through grade boundaries from highest to lowest
        for limit, grade in [(70, 'A'), (60, 'B'), (50, 'C'), (40, 'D')]:
            if percent >= limit:
                break
        else:
            grade = 'F'  # runs if we never hit break
        
        return total_coursework, total, percent, grade

    # -------------------------------------------------------------
    # Function: create_button
    # Purpose: Create styled button with hover effect
    # Made this helper so I don't copy-paste button code everywhere (DRY principle)
    # Source for bind: https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    # -------------------------------------------------------------
    def create_button(self, parent, text, cmd, bg):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"),
                        bg=bg, fg="white", width=18, height=2,
                        relief="flat", cursor="hand2", command=cmd)
        
        hover = "#1F8A4A" if bg == "#26AD5E" else "#3A4A5C"
        
        # bind mouse events for hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn

    # -------------------------------------------------------------
    # Function: setup_ui
    # Purpose: Build all GUI elements and layout
    # -------------------------------------------------------------
    def setup_ui(self):
        # Header area
        tk.Label(self.root, text="Student Manager", font=("Segoe UI", 28, "bold"),
                 fg="white", bg="#2B3643").pack(fill="x", pady=20)
        
        self.count_label = tk.Label(self.root, text=f"Total Students: {len(self.students)}",
                                     font=("Segoe UI", 11), fg="#26AD5E", bg="#2B3643")
        self.count_label.pack()

        # Content frame
        content = tk.Frame(self.root, bg="#1D252D")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # --- BUTTONS ROW 1 ---
        btns1 = tk.Frame(content, bg="#1D252D")
        btns1.pack(fill="x", pady=5)
        self.create_button(btns1, "View All Records", self.view_all, "#26AD5E").pack(side="left", padx=3)
        self.create_button(btns1, "Highest Score", self.show_highest, "#2B3643").pack(side="left", padx=3)
        self.create_button(btns1, "Lowest Score", self.show_lowest, "#2B3643").pack(side="left", padx=3)
        self.create_button(btns1, "Sort Records", self.sort_records, "#4A5C6B").pack(side="left", padx=3)

        # --- BUTTONS ROW 2 (CRUD Operations) ---
        btns2 = tk.Frame(content, bg="#1D252D")
        btns2.pack(fill="x", pady=5)
        self.create_button(btns2, "Add Student", self.add_student, "#2E7D32").pack(side="left", padx=3)
        self.create_button(btns2, "Update Student", self.update_student, "#1976D2").pack(side="left", padx=3)
        self.create_button(btns2, "Delete Student", self.delete_student, "#C62828").pack(side="left", padx=3)

        # --- DROPDOWN ROW ---
        select = tk.Frame(content, bg="#2B3643")
        select.pack(fill="x", pady=10, ipady=10)
        tk.Label(select, text="View Individual Student:",
                 font=("Segoe UI", 11, "bold"), fg="white", bg="#2B3643").pack(side="left", padx=10)

        self.selected = tk.StringVar()
        self.student_combo = ttk.Combobox(select, textvariable=self.selected,
                                          state="readonly", width=35)
        self.student_combo.pack(side="left", padx=10)
        self.update_combo()
        self.create_button(select, "View Record", self.view_individual, "#26AD5E").pack(side="left", padx=10)

        # --- SCROLLABLE DISPLAY AREA ---
        disp = tk.Frame(content, bg="#1D252D")
        disp.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(disp, bg="#FFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(disp, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#FFF")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scroll
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    # -------------------------------------------------------------
    # Helper: update combo box and count label
    # -------------------------------------------------------------
    def update_combo(self):
        student_names = [f"{s['id']} - {s['name']}" for s in self.students]
        self.student_combo['values'] = student_names
        self.count_label.config(text=f"Total Students: {len(self.students)}")

    # -------------------------------------------------------------
    # Helper: get grade color for badge display
    # -------------------------------------------------------------
    def color(self, grade):
        return {'A': '#26AD5E', 'B': '#4CAF50', 'C': '#FF9800',
                'D': '#FF5722', 'F': '#D32F2F'}.get(grade, '#757575')

    # -------------------------------------------------------------
    # Helper: clear display area before new content
    # -------------------------------------------------------------
    def clear_display(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

    # -------------------------------------------------------------
    # Function: show_card
    # Purpose: Display a student's details (used for all views)
    # -------------------------------------------------------------
    def show_card(self, s, title):
        if title:
            self.clear_display()
            tk.Label(self.scroll_frame, text=title, font=("Segoe UI", 16, "bold"),
                     bg="#FFF").pack(pady=(20, 10), anchor="w", padx=30)
        
        c_total, total, percent, grade = self.calculate_results(s)
        card = tk.Frame(self.scroll_frame, bg="#F8F9FA", relief="solid", bd=1)
        card.pack(fill="x", padx=30, pady=10)

        # Show student info
        details = [
            ("Name", s['name']),
            ("Number", s['id']),
            ("Coursework Total", f"{c_total}/60"),
            ("Exam Mark", f"{s['exam_mark']}/100"),
            ("Overall %", f"{percent:.2f}%")
        ]
        for k, v in details:
            tk.Label(card, text=f"{k}: {v}", font=("Segoe UI", 11),
                     bg="#F8F9FA", anchor="w").pack(anchor="w", pady=2, padx=10)

        # Grade badge
        tk.Label(card, text=f"Grade: {grade}", font=("Segoe UI", 13, "bold"),
                 bg=self.color(grade), fg="white", width=10).pack(pady=10)

    # -------------------------------------------------------------
    # View Functions
    # -------------------------------------------------------------
    def view_all(self):
        """Display all students in scrollable list."""
        self.clear_display()
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        tk.Label(self.scroll_frame, text="All Student Records",
                 font=("Segoe UI", 16, "bold"), bg="#FFF").pack(pady=(20, 10), anchor="w", padx=20)
        for s in self.students:
            self.show_card(s, "")

    def view_individual(self):
        """Display the selected student's record."""
        if not self.selected.get():
            return messagebox.showwarning("Select", "Please select a student.")
        sid = self.selected.get().split(" - ")[0]
        s = next((x for x in self.students if x['id'] == sid), None)
        if s:
            self.show_card(s, "Individual Student Record")

    def show_highest(self):
        """Find and display the highest-scoring student."""
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        self.show_card(max(self.students, key=lambda s: self.calculate_results(s)[2]),
                       "Highest Scoring Student")

    def show_lowest(self):
        """Find and display the lowest-scoring student."""
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        self.show_card(min(self.students, key=lambda s: self.calculate_results(s)[2]),
                       "Lowest Scoring Student")

    # -------------------------------------------------------------
    # EXTENSION: Sort Records
    # This was pretty easy once I figured out lambda functions.
    # key parameter tells sort() what to sort by - lambda returns the percentage.
    # Source for sort with key: https://docs.python.org/3/howto/sorting.html
    # -------------------------------------------------------------
    def sort_records(self):
        """Sort student records by percentage."""
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Student Records")
        sort_window.geometry("400x200")
        sort_window.configure(bg="#2B3643")
        sort_window.grab_set()  # modal window
        
        tk.Label(sort_window, text="Choose Sort Order", font=("Segoe UI", 14, "bold"),
                 fg="white", bg="#2B3643").pack(pady=20)
        
        def sort_and_display(reverse):
            # THE MAGIC LINE - sorts by percentage
            self.students.sort(key=lambda s: self.calculate_results(s)[2], reverse=reverse)
            sort_window.destroy()
            self.clear_display()
            
            order = "Descending" if reverse else "Ascending"
            tk.Label(self.scroll_frame, text=f"Sorted Records ({order} Order)",
                     font=("Segoe UI", 16, "bold"), bg="#FFF").pack(pady=(20, 10), anchor="w", padx=20)
            
            for s in self.students:
                self.show_card(s, "")
        
        btn_frame = tk.Frame(sort_window, bg="#2B3643")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Ascending", font=("Segoe UI", 11, "bold"),
                  bg="#26AD5E", fg="white", width=15, height=2, 
                  command=lambda: sort_and_display(False)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Descending", font=("Segoe UI", 11, "bold"),
                  bg="#1976D2", fg="white", width=15, height=2, 
                  command=lambda: sort_and_display(True)).pack(side="left", padx=10)

    # -------------------------------------------------------------
    # EXTENSION: Add Student
    # This took AGES to get right - so many edge cases!
    # Using a dict called 'fields' to store all entry widgets makes validation easier.
    # Source for Entry widget: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
    # -------------------------------------------------------------
    def add_student(self):
        """Add a new student record."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Student")
        add_window.geometry("500x450")
        add_window.configure(bg="#2B3643")
        add_window.grab_set()
        
        tk.Label(add_window, text="Add New Student", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#2B3643").pack(pady=15)
        
        form = tk.Frame(add_window, bg="#2B3643")
        form.pack(pady=10, padx=30, fill="both", expand=True)
        
        fields = {}
        labels = [("Student ID:", "id"), ("Student Name:", "name"),
                  ("Coursework 1 (0-20):", "cw1"), ("Coursework 2 (0-20):", "cw2"),
                  ("Coursework 3 (0-20):", "cw3"), ("Exam Mark (0-100):", "exam")]
        
        # Create all labels and entry boxes using grid layout
        for i, (label, key) in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 11), fg="white",
                     bg="#2B3643", anchor="w").grid(row=i, column=0, sticky="w", pady=8)
            entry = tk.Entry(form, font=("Segoe UI", 11), width=25)
            entry.grid(row=i, column=1, pady=8, padx=10)
            fields[key] = entry
        
        def save_new_student():
            try:
                student_id = fields['id'].get().strip()
                name = fields['name'].get().strip()
                
                if not student_id or not name:
                    return messagebox.showerror("Error", "ID and Name are required!")
                
                # Check if ID already exists
                if any(s['id'] == student_id for s in self.students):
                    return messagebox.showerror("Error", "Student ID already exists!")
                
                cw1 = int(fields['cw1'].get())
                cw2 = int(fields['cw2'].get())
                cw3 = int(fields['cw3'].get())
                exam = int(fields['exam'].get())
                
                # Validate mark ranges
                if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                    return messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                if not (0 <= exam <= 100):
                    return messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                
                # Add student
                self.students.append({
                    'id': student_id,
                    'name': name,
                    'course_marks': [cw1, cw2, cw3],
                    'exam_mark': exam
                })
                
                if self.save_students():
                    messagebox.showinfo("Success", "Student added successfully!")
                    self.update_combo()
                    add_window.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")
        
        tk.Button(add_window, text="Save Student", font=("Segoe UI", 12, "bold"),
                  bg="#26AD5E", fg="white", width=20, height=2,
                  command=save_new_student).pack(pady=15)

    # -------------------------------------------------------------
    # EXTENSION: Delete Student
    # Simpler than add/update but I added confirmation because deleting is permanent!
    # Using next() with generator - stops as soon as it finds a match (more efficient).
    # Source for next(): https://www.w3schools.com/python/ref_func_next.asp
    # -------------------------------------------------------------
    def delete_student(self):
        """Delete a student record."""
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("500x250")
        delete_window.configure(bg="#2B3643")
        delete_window.grab_set()
        
        tk.Label(delete_window, text="Delete Student Record", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#2B3643").pack(pady=15)
        
        tk.Label(delete_window, text="Select Student to Delete:", font=("Segoe UI", 11),
                 fg="white", bg="#2B3643").pack(pady=10)
        
        selected_student = tk.StringVar()
        student_list = [f"{s['id']} - {s['name']}" for s in self.students]
        combo = ttk.Combobox(delete_window, textvariable=selected_student,
                            values=student_list, state="readonly", width=40)
        combo.pack(pady=10)
        
        def confirm_delete():
            if not selected_student.get():
                return messagebox.showwarning("Select", "Please select a student to delete.")
            
            sid = selected_student.get().split(" - ")[0]
            student = next((s for s in self.students if s['id'] == sid), None)
            
            if student:
                # Ask for confirmation before deleting
                confirm = messagebox.askyesno("Confirm Delete",
                                             f"Are you sure you want to delete:\n{student['name']} ({student['id']})?")
                if confirm:
                    self.students.remove(student)
                    if self.save_students():
                        messagebox.showinfo("Success", "Student deleted successfully!")
                        self.update_combo()
                        delete_window.destroy()
                        self.clear_display()
        
        tk.Button(delete_window, text="Delete Student", font=("Segoe UI", 12, "bold"),
                  bg="#C62828", fg="white", width=20, height=2,
                  command=confirm_delete).pack(pady=15)

    # -------------------------------------------------------------
    # EXTENSION: Update Student
    # Most complex one! Combines add and delete plus auto-loads current data.
    # The trace() method on StringVar is SUPER useful - it calls a function 
    # whenever the variable changes, so data loads automatically when you select!
    # Source for trace: https://www.pythontutorial.net/tkinter/tkinter-stringvar/
    # -------------------------------------------------------------
    def update_student(self):
        """Update an existing student record."""
        if not self.students:
            return messagebox.showinfo("No Data", "No student records found.")
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("500x550")
        update_window.configure(bg="#2B3643")
        update_window.grab_set()
        
        tk.Label(update_window, text="Update Student Record", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#2B3643").pack(pady=15)
        
        tk.Label(update_window, text="Select Student:", font=("Segoe UI", 11),
                 fg="white", bg="#2B3643").pack(pady=5)
        
        selected_student = tk.StringVar()
        student_list = [f"{s['id']} - {s['name']}" for s in self.students]
        combo = ttk.Combobox(update_window, textvariable=selected_student,
                            values=student_list, state="readonly", width=40)
        combo.pack(pady=5)
        
        form = tk.Frame(update_window, bg="#2B3643")
        form.pack(pady=15, padx=30)
        
        fields = {}
        labels = [("Student Name:", "name"),
                  ("Coursework 1 (0-20):", "cw1"), ("Coursework 2 (0-20):", "cw2"),
                  ("Coursework 3 (0-20):", "cw3"), ("Exam Mark (0-100):", "exam")]
        
        for i, (label, key) in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 10), fg="white",
                     bg="#2B3643", anchor="w").grid(row=i, column=0, sticky="w", pady=6)
            entry = tk.Entry(form, font=("Segoe UI", 10), width=25)
            entry.grid(row=i, column=1, pady=6, padx=10)
            fields[key] = entry
        
        # Auto-load data when student is selected
        def load_student_data(*args):
            if selected_student.get():
                sid = selected_student.get().split(" - ")[0]
                student = next((s for s in self.students if s['id'] == sid), None)
                
                if student:
                    # Clear and insert new data for each field
                    fields['name'].delete(0, tk.END)
                    fields['name'].insert(0, student['name'])
                    
                    fields['cw1'].delete(0, tk.END)
                    fields['cw1'].insert(0, student['course_marks'][0])
                    
                    fields['cw2'].delete(0, tk.END)
                    fields['cw2'].insert(0, student['course_marks'][1])
                    
                    fields['cw3'].delete(0, tk.END)
                    fields['cw3'].insert(0, student['course_marks'][2])
                    
                    fields['exam'].delete(0, tk.END)
                    fields['exam'].insert(0, student['exam_mark'])
        
        # trace watches the StringVar for changes
        selected_student.trace('w', load_student_data)
        
        def save_updates():
            if not selected_student.get():
                return messagebox.showwarning("Select", "Please select a student.")
            
            try:
                sid = selected_student.get().split(" - ")[0]
                student = next((s for s in self.students if s['id'] == sid), None)
                
                if student:
                    name = fields['name'].get().strip()
                    if not name:
                        return messagebox.showerror("Error", "Name cannot be empty!")
                    
                    cw1 = int(fields['cw1'].get())
                    cw2 = int(fields['cw2'].get())
                    cw3 = int(fields['cw3'].get())
                    exam = int(fields['exam'].get())
                    
                    if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                        return messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                    if not (0 <= exam <= 100):
                        return messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                    
                    # Update the dictionary directly
                    student['name'] = name
                    student['course_marks'] = [cw1, cw2, cw3]
                    student['exam_mark'] = exam
                    
                    if self.save_students():
                        messagebox.showinfo("Success", "Student updated successfully!")
                        self.update_combo()
                        update_window.destroy()
                        
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")
        
        tk.Button(update_window, text="Save Changes", font=("Segoe UI", 12, "bold"),
                  bg="#1976D2", fg="white", width=20, height=2,
                  command=save_updates).pack(pady=15)

# -------------------------------------------------------------
# PROGRAM ENTRY POINT
# This only runs if you execute this file directly.
# tk.Tk() creates the main window, mainloop() keeps it running.
# Source: https://realpython.com/python-gui-tkinter/
# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    StudentManager(root)
    root.mainloop()
