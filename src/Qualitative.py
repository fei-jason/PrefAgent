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
            case 4:
                table.clear()
                dict_quality_comparison = show_table(feasible_table, list_logic, dict_list_logic)
                exemplification(dict_quality_comparison)
                print()
            case 5:
                table.clear()
                dict_quality_comparison = show_table(feasible_table, list_logic, dict_list_logic)
                optimal = omnioptimization(dict_quality_comparison)
                print("All optimal objects: ", end="")
                for i in optimal:
                    print(f"o{i} ", end="")
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
    """
    feasible_table (dictionary): keys are index o1, o2, ettc. values are their corresponding integer model [-2,1,2]

    list_logic (list): a list of lists. each list contains the CNF logic. it will not work with more than
    5 words if the line were to be split [attribute, attribute, condition IF]

    list_logic_name (dictionary): keys are a tuple of the lists inside list_logic, values is the corresponding name. used to identify which 
    logic goes with who since the logic is translated to CNF.
    """
    ## this dictionary will keep track of each object's number o1, o2, etc. and their preference value across the row; ie, 1, 2, inf, 2, inf
    ## INFINITY WILL BE REPRESENTED AS A 0 
    dict_quality_comparison = {}
    value = None
    table_columns = []
    for item in list_logic:

        for i in feasible_table:

            if i not in dict_quality_comparison:
                dict_quality_comparison[i] = ""

            # there exist condition
            if item[2] != 0:

                if item[2] in feasible_table[i]:
                    if item[0] in feasible_table[i] and item[1] in feasible_table[i]:
                        value = float('inf')
                    elif item[0] in feasible_table[i]:
                        value = 1
                    elif item[1] in feasible_table[i]:
                        value = 2
                    else:
                        value = float('inf')
                else:
                    value = float('inf')
            # there exists no condition
            else:
                if item[0] in feasible_table[i] and item[1] in feasible_table[i]:
                    value - float('inf')
                elif item[0] in feasible_table[i]:
                    value = 1
                elif item[1] in feasible_table[i]:
                    value = 2
                else:
                    value = float('inf')

            table_columns.append(value)
            if value == float('inf'):
                dict_quality_comparison[i] += str(0)
            else:
                dict_quality_comparison[i] += str(value)
        table.add_column(list_logic_name[tuple(item)], table_columns)
        table_columns = []
    
    return dict_quality_comparison

def exemplification(dict_quality_comparison):
    """
    dict_quality_comparison (dictionary): will keep track of each object o1, o2, that is feasible and their respective preference rating across the row.
    For example, o2: 1212infinf
    """
    rand1, rand2 = random.sample(dict_quality_comparison.keys(), 2)
    str_comparison = ""

    str1 = dict_quality_comparison[rand1]
    str2 = dict_quality_comparison[rand2]

    if len(str1) == len(str2):
        for i in range(len(str1)):
            if str1[i] > str2[i]:
                str_comparison += str(1)
            elif str1[i] < str2[i]:
                str_comparison += str(2)
            elif str1[i] == str2[i]:
                str_comparison += str(0)
    else:
        print(f"Length of {str1} and {str2} are different. Something went really wrong.")

    print(f"Two randomly selected feasible objects are o{rand1} and o{rand2}.")

    if '1' in str_comparison and '2' in str_comparison:
        print(f"o{rand1} and o{rand2} are incomparable")
    elif '1' in str_comparison and '2' not in str_comparison:
        print(f"o{rand1} is strickly preferred over o{rand2}")
    elif '2' in str_comparison and '1' not in str_comparison:
        print(f"o{rand2} is strickly preferred over o{rand1}")
    else:
        print(f"o{rand1} and o{rand2} are equal")

def omnioptimization(dict_quality_comparison):
    optimal = []
    smallest = 0
    for i in dict_quality_comparison:
        sum = 0
        
        for digit in dict_quality_comparison[i]:
            sum += int(digit)
        
        if smallest == 0:
            smallest = sum
            optimal.append(i)
        elif sum < smallest:
            smallest = sum
            optimal = [i]
        elif sum == smallest:
            optimal.append(i)
    
    return optimal