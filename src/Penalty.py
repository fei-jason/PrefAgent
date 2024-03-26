import itertools
from pysat.formula import CNF
from pysat.solvers import Solver
from prettytable import PrettyTable

attribute_table = {}
encoding_table = {}
table = PrettyTable()

def penalty_menu():
    print("Choose the reasoning task to perform: "
      + "\n1. Encoding"
      + "\n2. Feasibility Checking"
      + "\n3. Show the Table"
      + "\n4. Exemplification"
      + "\n5. Omni-optimization"
      + "\n6. Back to previous menu")
    
## MAIN FUNCTION
def penalty_logic(att_file_path, cons_file_path, pen_file_path):
    while True:
        penalty_menu()
        user_input = int(input("Choose the reasoning task to perform: "))

        # runs encoding
        product, int_prod = encoding(att_file_path)
        model_list = feasibility(cons_file_path)
        match(user_input):
            case 1: # encoding
                for i, items in enumerate(product):
                    print(f"o{i} - {', '.join(items)}")
                # for i, items in enumerate(int_prod):
                #     print(f"o{i} - {items}")
                print("")
            case 2: # feasibility
                print(f"There are {len(model_list)} feaisble objects") 
                print("")
            case 3: # show table
                name = []
                for i, items in enumerate(int_prod):
                    for model in model_list:
                        if list(items) == model:
                            name.append(f"o{i}")
                table.add_column("encoding", name)
                show_table(model_list, pen_file_path)
                print(table)
            case 4:
                print("")
            case 6: # exit
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
            # courses are not necessary
            course, items = line.strip().split(":")
            items_list = [item.strip() for item in items.split(",")]

            # this hash table is used to keep track of all available items
            # the purpose is to hopefully be able to convert to CNF easier because we can idenitfy key words
            if len(items_list) == 2:
                attribute_table[items_list[0]] = counter
                attribute_table[items_list[1]] = -counter
            else:
                print("Could not read all the items because there are more than 2 in each course")
                exit()

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

def feasibility(cons_file_path):
    cnf_list = []
    with open(cons_file_path, "r") as file:
        for line in file:
            cnf, condition = to_cnf(line)
            cnf_list.append(cnf)
    
    for attr in attribute_table.values():
        for clause in cnf_list:
            if attr in clause or -attr in clause:
                break
            else:
                cnf_list.append([-attr, attr])
                
    cnf = CNF(from_clauses=cnf_list)
    #cnf = CNF(from_clauses=[[-2,1],[-3,3]])

    with Solver(bootstrap_with=cnf) as solver:
        #print('Formula is', f'{"s" if solver.solve() else "uns"}atisfiable')
        # for item in solver.enum_models():
        #     print(item)
        model_list = list(solver.enum_models())
    
    return model_list

def show_table(int_prod, pen_file_path):
    penalty_list = []
    total_penalty = []
    table_columns = []

    with open(pen_file_path, "r") as file:
        for line in file:
            penalty_list.append(line.strip())

    for line in penalty_list:
        logic, penalty_str = map(str.strip, line.split(','))
        penalty = int(penalty_str)
        cnf, condition = to_cnf(logic)

        for object in int_prod:
            if condition == "AND":
                if cnf[0] not in object or cnf[1] not in object:
                    table_columns.append(penalty)
                else:
                    table_columns.append(0)
            else:
                if cnf[0] not in object and cnf[1] not in object:
                    table_columns.append(penalty)
                else:
                    table_columns.append(0)
            
        table.add_column(logic, table_columns)
        table_columns = []


def to_cnf(line):
    items = line.split()
    condition = "OR"
    result = []
    
    i = 0
    while i < len(items):
        if items[i] == "NOT":
            result.append(-1 * attribute_table[items[i+1]]) #i+1 for the item after NOT
            i += 2 #skip NOT and corresponding item
        elif items[i] == "AND":
            condition = "AND"
            i += 1
        elif items[i] == "OR":
            i += 1
        else:
            result.append(attribute_table[items[i]])
            i += 1

    return result, condition