import itertools
from pysat.formula import CNF
from pysat.solvers import Solver

def penalty_menu():
    print("Choose the reasoning task to perform: "
      + "\n1. Encoding"
      + "\n2. Feasibility Checking"
      + "\n3. Show the Table"
      + "\n4. Exemplification"
      + "\n5. Omni-optimization"
      + "\n6. Back to previous menu")
    
## MAIN FUNCTION
def penalty_logic(att_file_path, pen_file_path):
    while(True):
        penalty_menu()
        user_input = int(input("Choose the reasoning task to perform: "))
        match(user_input):
            case 1:
                encoding(att_file_path)

def encoding(att_file_path):
    attributes = []
    encoded_binary = []

    # while not os.path.exists(att_file_name):

    with open(att_file_path, "r") as file:
        for line in file:
            course, items = line.strip().split(":")
            items_list = [item.strip() for item in items.split(",")]
            attributes.append(items_list)
           
    product = list(itertools.product(*attributes))

    # So the cartesian product correctly makes the encoding, but you will need to reverse it when 
    # printing. There shouldn't be any issues because the binary representation is the final correct.
    # The product is only used for printing. This is a scuffed way to fix, idk really. 
    for i, items in enumerate(product):
        binary_encoding = [attributes[j].index(item) for j, item in enumerate(items)]   
        encoded_binary.append(binary_encoding)

    product.reverse()

    for i, items in enumerate(product):
        print(f"o{i} - {', '.join(items)}")

    return binary_encoding