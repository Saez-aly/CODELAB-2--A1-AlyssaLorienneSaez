import random

# -----------------------------
# Load jokes from file
# -----------------------------
with open(r"C:\Users\saeza\OneDrive\Desktop\A1 Advanced Programming\Exercise 2\jokes.txt", "r") as file:
    jokes = [line.strip() for line in file if "?" in line]

# -----------------------------
# Function to tell a single joke
# -----------------------------
def tell_joke(jokes):
    joke = random.choice(jokes)
    setup, punchline = joke.split("?", 1)
    print("\n" + setup + "?")
    input("Press Enter...")
    print(punchline)

# -----------------------------
# Function to handle repeating jokes
# -----------------------------
def joke_loop(jokes):
    while True:
        tell_joke(jokes)
        while True:
            another = input("\nHaving fun? Wanna hear another one? (yes/no): ").strip().lower()
            if another == "yes":
                break  # tell next joke
            elif another == "no":
                print("\nOkay then kitty.. You can comeback to me anytime..")
                return  # exit the loop
            else:
                print("Please type 'yes' or 'no'.")

# -----------------------------
# Main function
# -----------------------------
def main():
    if not jokes:
        print("I guess you wanna have a bad day..Exiting the program")
        return
    
    print("Type 'Alexa tell me a Joke', or 'quit'. Choose at your own risk.")
    
    while True:
        user_input = input("\nYou: ").strip().lower()
        if user_input == "alexa tell me a joke":
            joke_loop(jokes)
            break
        elif user_input == "quit":
            print("I guess you wanna have a bad day..Bye!")
            break
        else:
            print("Say 'Alexa tell me a Joke' to hear a joke, or 'quit' to exit.")

# -----------------------------
# Run the program
# -----------------------------
if __name__ == "__main__":
    main()
