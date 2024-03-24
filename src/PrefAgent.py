import Penalty, collections, os

print("Welcome to PrefAgent!\n")

# change directory path
directory_path = "ExampleTestCase/"

# att_file_path = directory_path + input("Enter Attribute File Name: ")
# cons_file_path = directory_path + input("Enter Constraint File Name: ")
att_file_path = directory_path + "attributes.txt"

# Choose the preference logic to use:
# 1. Penalty Logic
# 2. Qualitative Choice Logic
# 3. Exit

print("Choose the preference logic to use: \n1. Penalty Logic \n2. Qualitative Choice Logic\n3. Exit")
user_input = int(input())
while user_input != 3:
    match(user_input):
        case 1:
            print("You have picked Penalty Logic")
            # pen_file_path = directory_path + input("Enter Preferences File Name: ")
            pen_file_path = directory_path + "penaltylogic.txt"
            Penalty.penalty_logic(att_file_path, pen_file_path)