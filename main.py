# Runs the program, takes user input and calls logic and finally prints the result
from logic import process_input, format_output

def ask_user():
    # Get user input
    feelings = input("How are you feeling today? > \n")
    return feelings



def main():
    feelings = ask_user()
    result = process_input(feelings)
    text = format_output(result)
    print(text)


if __name__ == "__main__":
    main()
