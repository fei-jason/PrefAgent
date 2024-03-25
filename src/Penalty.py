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
    while True:
        penalty_menu()
        user_input = int(input("Choose the reasoning task to perform: "))
        match(user_input):
            case 1:
                product, int_prod = encoding(att_file_path)
                for i, items in enumerate(product):
                    print(f"o{i} - {', '.join(items)}")
                print("")
            case 2:
                product, int_prod = encoding(att_file_path)
                feasibility(int_prod)
                print("")
            case 6:
                break
          
def encoding(att_file_path):
    attributes = []
    int_attributes = []
    encoded_binary = []

    # while not os.path.exists(att_file_name):

    # counter is used to keep track of the encoding via numerical lines. it will be negative if the food item
    # is second. positive if first.
    with open(att_file_path, "r") as file:
        counter = 1
        for line in file:
            course, items = line.strip().split(":")
            items_list = [item.strip() for item in items.split(",")]
            attributes.append(items_list)
            int_attributes.append([counter, -counter])
            counter += 1
           
    # these two will be all unique combinations of the attributes.
    product = list(itertools.product(*attributes))
    int_product = list(itertools.product(*int_attributes))

    # So the cartesian product correctly makes the encoding, but you will need to reverse it when 
    # printing. There shouldn't be any issues because the binary representation is the final correct.
    # The product is only used for printing. I dont believe binary_encoding is used. i dont see why
    # I would use if given PySAT utility isn't in binary ( at least i dont know how to make it binary )
    for i, items in enumerate(product):
        binary_encoding = [attributes[j].index(item) for j, item in enumerate(items)]   
        encoded_binary.append(binary_encoding)

    product.reverse()
    int_product.reverse()

    return product, int_product 

def feasibility(product):
    cnf = CNF(from_clauses=[[-2, -3]])

    with Solver(bootstrap_with=cnf) as solver:
        print('Formula is', f'{"s" if solver.solve() else "uns"}atisfiable')
        model_list = list(solver.enum_models())
        print(f"There are {len(model_list)} feaisble objects")