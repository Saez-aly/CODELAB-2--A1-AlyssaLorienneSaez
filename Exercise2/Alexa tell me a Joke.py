import tkinter as tk
from tkinter import messagebox
import random

# Load jokes from file
with open(r"C:\Users\saeza\OneDrive\Desktop\A1 Advanced Programming\Exercise 2\jokes.txt", "r") as file:
    jokes = [line.strip() for line in file if "?" in line]

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Machine")
        self.root.geometry("500x350")
        self.root.config(bg="#FFD700")
        self.current_joke = None
        self.showing_punchline = False
        
        # Title
        tk.Label(root, text="🎭 Alexa's Joke Machine 🎭", font=("Arial", 18, "bold"), 
                bg="#FFD700", fg="#000").pack(pady=15)
        
        # Joke Display
        self.joke_frame = tk.Frame(root, bg="#FFF8DC", bd=3, relief="ridge")
        self.joke_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        self.joke_label = tk.Label(self.joke_frame, 
                                   text="Click 'Tell me a Joke' to start!\nChoose at your own risk... 😏",
                                   font=("Arial", 13), bg="#FFF8DC", fg="#000", 
                                   wraplength=450, justify="center", pady=25)
        self.joke_label.pack(fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(root, bg="#FFD700")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Tell me a Joke", font=("Arial", 11, "bold"),
                 bg="#FFA500", fg="white", width=14, command=self.tell_joke).grid(row=0, column=0, padx=5)
        
        self.punchline_btn = tk.Button(btn_frame, text="Show Punchline", font=("Arial", 11, "bold"),
                                       bg="#FF8C00", fg="white", width=14, command=self.show_punchline)
        
        tk.Button(btn_frame, text="Quit", font=("Arial", 11, "bold"),
                 bg="#DAA520", fg="white", width=14, command=self.quit_app).grid(row=0, column=2, padx=5)
    
    def tell_joke(self):
        if not jokes:
            messagebox.showerror("Error", "No jokes found!")
            return
        self.current_joke = random.choice(jokes)
        setup, punchline = self.current_joke.split("?", 1)
        self.joke_label.config(text=setup + "?", font=("Arial", 15, "bold"))
        self.showing_punchline = False
        self.punchline_btn.grid(row=0, column=1, padx=5)
        
    def show_punchline(self):
        if self.current_joke and not self.showing_punchline:
            setup, punchline = self.current_joke.split("?", 1)
            self.joke_label.config(text=setup + "?\n\n" + punchline.strip(), font=("Arial", 13))
            self.showing_punchline = True
            self.punchline_btn.grid_forget()
    
    def quit_app(self):
        if messagebox.askyesno("Quit", "I guess you wanna have a bad day...\nQuit?"):
            self.root.destroy()

def main():
    if not jokes:
        print("I guess you wanna have a bad day..Exiting the program")
        return
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
