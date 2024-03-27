import itertools, random
import Utils as utils
from pysat.formula import CNF
from pysat.solvers import Solver
from prettytable import PrettyTable

##attribute table is a dictionary of all the attributes and their values startin from 1 and -1
## feasible_table is a dictionary of all feasible attributes using index as key and int combination list as value
attribute_table = {}
feasible_table = {}
table = PrettyTable()

def qualitative_logic(att_file_path, cons_file_path, qual_file_path):
    while True:
        utils.show_menu()
        user_input = int(input("Choose the reasoning task to perform: "))
        
        # str_list_attribute is str version of all combinations
        # int_list_attributes is int version of all combinations
        # list_feasible_model is int list of all feasible combinations
        str_list_attribute, int_list_attribute = encoding(att_file_path)
        list_feasible_model = feasibility(cons_file_path)

        #required to set the feasible_table
        for i, items in enumerate(int_list_attribute):
            for model in list_feasible_model:
                if list(items) == model:
                    feasible_table[i] = model
        
        list_logic, dict_list_logic = comprehend_qualitative_choice(qual_file_path)

        match(user_input):
            case 1: #encoding
                for i, items in enumerate(str_list_attribute):
                    print(f"o{i} - {', '.join(items)}")
                print()
            case 2: #feasibility
                print(f"There are {len(feasible_table)} feasible objects.")
            case 3: #show_table
                table.clear()
                name = []
                for i in feasible_table:
                    name.append(f"o{i}")
                table.add_column("encoding", name)
                show_table(feasible_table, list_logic, dict_list_logic)
                print(table)
                print()
            case 6:
                break


def encoding(att_file_path):
    list_attributes = []
    int_list_attributes = []
    counter = 1

    with open(att_file_path, "r") as file:
        for line in file:
            # courses are not necessary
            course, items = line.strip().split(":")
            # gets the two items as a list
            items_list = [item.strip() for item in items.split(",")]

            if len(items_list) == 2:
                attribute_table[items_list[0]] = counter
                attribute_table[items_list[1]] = -counter
            else:
                print("Could not read all the items because there are more than 2 in each course")
                exit()

            ##append both string and int versions
            list_attributes.append(items_list)
            int_list_attributes.append([counter, -counter])
            counter += 1

    str_list_attribute = list(itertools.product(*list_attributes))
    int_int_list_attribute = list(itertools.product(*int_list_attributes))
    
    str_list_attribute.reverse()
    int_int_list_attribute.reverse()
    
    return str_list_attribute, int_int_list_attribute

def feasibility(cons_file_path):
    cnf_list = []
    with open(cons_file_path, "r") as file:
        for line in file:
            cnf, condition = utils.to_cnf(line, attribute_table)
            cnf_list.append(cnf)
        
    for attr in attribute_table.values():
        for clause in cnf_list:
            if attr in clause or -attr in clause:
                break
            else:
                cnf_list.append([-attr, attr])
    
    cnf = CNF(from_clauses=cnf_list)

    with Solver(bootstrap_with=cnf) as solver:
        model_list = list(solver.enum_models())
    
    return model_list

def comprehend_qualitative_choice(qual_file_path):
    """
    This method will have to be changed if there are many more clauses to the qualitative choice logic.
    This is because currently, i have hard coded the length to 4 and 5 which means either 2 items or 3 items ONLY
    """

    #list_logic will be the logic in int as list
    #dict_logic_name will have the int logic as a key and name as the value
    list_logic = []
    dict_logic_name = {}
    with open(qual_file_path, "r") as file:
        for line in file:
            items = line.strip().split()

            # the len will always be 4 because of this hardcoding
            attribute1 = attribute_table[items[0]]
            attribute2 = attribute_table[items[2]]
            condition = 0
            
            # if len is 5, then there is a condition met
            if len(items) == 5:
                condition = attribute_table[items[4]]
            
            logic = [attribute1, attribute2, condition]
            list_logic.append(logic)

            dict_logic_name[tuple(logic)] = line.strip()

    
    return list_logic, dict_logic_name

def show_table(feasible_table, list_logic, list_logic_name):

    table_columns = []
    for item in list_logic:

        for i in feasible_table:
            # there exist condition
            if item[2] != 0:

                if item[2] in feasible_table[i]:
                    if item[0] in feasible_table[i] and item[1] in feasible_table[i]:
                        table_columns.append("inf")
                    elif item[0] in feasible_table[i]:
                        table_columns.append(1)
                    elif item[1] in feasible_table[i]:
                        table_columns.append(2)
                    else:
                        table_columns.append("inf")
                else:
                    table_columns.append("inf")
            # there exists no condition
            else:
                if item[0] in feasible_table[i] and item[1] in feasible_table[i]:
                    table_columns.append("inf")
                elif item[0] in feasible_table[i]:
                    table_columns.append(1)
                elif item[1] in feasible_table[i]:
                    table_columns.append(2)
                else:
                    table_columns.append("inf")

        table.add_column(list_logic_name[tuple(item)], table_columns)
        table_columns = []