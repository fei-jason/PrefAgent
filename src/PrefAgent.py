
print("Welcome to PrefAgent!\n")

# change directory path
directory_path = "ExampleTestCase/"

att_file_name = directory_path + input("Enter Attribute File Name: ")
cons_file_name = directory_path + input("Enter Constraint File Name: ")

# change to the folder directory
with open(att_file_name, "r") as file:
    content = file.read()

print(content)