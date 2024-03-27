import Penalty, Qualitative, collections, os

print("Welcome to PrefAgent!\n")

# change directory path
directory_path = "ExampleTestCase/"

att_file_path = directory_path + input("Enter Attribute File Name: ")
cons_file_path = directory_path + input("Enter Constraint File Name: ")

if os.path.exists(att_file_path) and os.path.exists(cons_file_path):
    while True:
        print("Choose the preference logic to use: \n1. Penalty Logic \n2. Qualitative Choice Logic\n3. Exit")
        try:
            user_input = int(input())
            match(user_input):
                case 1:
                    print("You have picked Penalty Logic")
                    pen_file_path = directory_path + input("Enter Preferences File Name: ")
                    if os.path.exists(pen_file_path):
                        Penalty.penalty_logic(att_file_path, cons_file_path, pen_file_path)
                    else:
                        print("Penalty file does not exist.")
                case 2:
                    print("You have picked Qualitative Choice Logic")
                    qual_file_path = directory_path + input("Enter Qualitative File Name: ")
                    if os.path.exists(qual_file_path):
                        Qualitative.qualitative_logic(att_file_path, cons_file_path, qual_file_path)
                    else:
                        print("Qualitative file does not exist.")
                case 3:
                    print("BYE")
                    break
        except ValueError:
            print("Invalid input, try again")

else:
    print("File path error, try again.")