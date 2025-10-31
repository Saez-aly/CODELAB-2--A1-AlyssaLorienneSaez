# -------------------------------------------------------------
# STUDENT MANAGER PROGRAM
# Description:
#   A simple student record manager using Tkinter GUI.
# -------------------------------------------------------------
# Sources/References:
# - Tkinter documentation: https://docs.python.org/3/library/tkinter.html
# - ComboBox style examples: https://tkdocs.com/tutorial/widgets.html
# -------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox


class StudentManager:
    def __init__(self, root):
        """Initialize window, data list, and setup the UI."""
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("900x700")
        self.root.configure(bg="#1D252D")  # dark mode theme
        self.students = []  # list to store all student data
        self.load_students()  # load data from text file
        self.setup_ui()       # create GUI layout

    # -------------------------------------------------------------
    # Function: load_students
    # Purpose: Read student details from the file and store in a list
    # -------------------------------------------------------------
    def load_students(self):
        try:
            path = r"C:\Users\saeza\OneDrive\Desktop\A1 Advanced Programming\Exercise 3\database.txt"
            with open(path, "r") as f:
                lines = f.readlines()
            # Skip header line if it contains a number (e.g., total count)
            if lines and lines[0].strip().isdigit():
                lines = lines[1:]
            for line in lines:
                data = line.strip().split(',')
                if len(data) >= 6:
                    self.students.append({
                        'id': data[0],
                        'name': data[1],
                        'course_marks': list(map(int, data[2:5])),
                        'exam_mark': int(data[5])
                    })
        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

    # -------------------------------------------------------------
    # Function: calculate_results
    # Purpose: Compute total, percentage, and grade for a student
    # -------------------------------------------------------------
    def calculate_results(self, s):
        total_coursework = sum(s['course_marks'])
        total = total_coursework + s['exam_mark']
        percent = (total / 160) * 100  # total out of 160
        # Assign grade based on percentage
        for limit, grade in [(70, 'A'), (60, 'B'), (50, 'C'), (40, 'D')]:
            if percent >= limit:
                break
        else:
            grade = 'F'
        return total_coursework, total, percent, grade

    # -------------------------------------------------------------
    # Function: create_button
    # Purpose: Create styled button with hover effect
    # -------------------------------------------------------------
    def create_button(self, parent, text, cmd, bg):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                        bg=bg, fg="white", width=22, height=2,
                        relief="flat", cursor="hand2", command=cmd)
        hover = "#1F8A4A" if bg == "#26AD5E" else "#3A4A5C"
        # Change button color on hover (visual feedback)
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
                 fg="white", bg="#2B3643").pack(fill="x", pady=25)
        tk.Label(self.root, text=f"Total Students: {len(self.students)}",
                 font=("Segoe UI", 11), fg="#26AD5E", bg="#2B3643").pack()

        # Content frame
        content = tk.Frame(self.root, bg="#1D252D")
        content.pack(fill="both", expand=True, padx=25, pady=20)

        # --- BUTTONS ROW ---
        btns = tk.Frame(content, bg="#1D252D")
        btns.pack(fill="x", pady=10)
        self.create_button(btns, "View All Student Records", self.view_all, "#26AD5E").pack(side="left", padx=5)
        self.create_button(btns, "Show Highest Score", self.show_highest, "#2B3643").pack(side="left", padx=5)
        self.create_button(btns, "Show Lowest Score", self.show_lowest, "#2B3643").pack(side="left", padx=5)

        # --- DROPDOWN ROW ---
        select = tk.Frame(content, bg="#2B3643")
        select.pack(fill="x", pady=10, ipady=10)
        tk.Label(select, text="View Individual Student Record:",
                 font=("Segoe UI", 11, "bold"), fg="white", bg="#2B3643").pack(side="left", padx=10)

        # Populate combo box with IDs and names
        student_names = [f"{s['id']} - {s['name']}" for s in self.students]
        self.selected = tk.StringVar()
        ttk.Combobox(select, textvariable=self.selected, values=student_names,
                     state="readonly", width=35).pack(side="left", padx=10)
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

        # Enable mousewheel scroll (Windows OS specific)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    # -------------------------------------------------------------
    # Helper Function: get grade color for badge display
    # -------------------------------------------------------------
    def color(self, grade):
        return {'A': '#26AD5E', 'B': '#4CAF50', 'C': '#FF9800',
                'D': '#FF5722', 'F': '#D32F2F'}.get(grade, '#757575')

    # -------------------------------------------------------------
    # Helper Function: clear display area before new content
    # -------------------------------------------------------------
    def clear_display(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

    # -------------------------------------------------------------
    # Function: show_card
    # Purpose: Display a student's details (used for all views)
    # -------------------------------------------------------------
    def show_card(self, s, title):
        self.clear_display()
        c_total, total, percent, grade = self.calculate_results(s)
        tk.Label(self.scroll_frame, text=title, font=("Segoe UI", 16, "bold"),
                 bg="#FFF").pack(pady=(20, 10), anchor="w", padx=30)
        card = tk.Frame(self.scroll_frame, bg="#F8F9FA")
        card.pack(fill="x", padx=30, pady=10)

        # Show student info neatly
        details = [
            ("Name", s['name']),
            ("Number", s['id']),
            ("Coursework Total", f"{c_total}/60"),
            ("Exam Mark", f"{s['exam_mark']}/100"),
            ("Overall %", f"{percent:.2f}%")
        ]
        for k, v in details:
            tk.Label(card, text=f"{k}: {v}", font=("Segoe UI", 11),
                     bg="#F8F9FA", anchor="w").pack(anchor="w", pady=2)

        # Grade badge
        tk.Label(card, text=f"Grade: {grade}", font=("Segoe UI", 13, "bold"),
                 bg=self.color(grade), fg="white", width=10).pack(pady=10)

    # -------------------------------------------------------------
    # View Functions (reuse show_card for all)
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
# PROGRAM ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    StudentManager(root)
    root.mainloop()
