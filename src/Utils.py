def show_menu():
    print("Choose the reasoning task to perform: "
      + "\n1. Encoding"
      + "\n2. Feasibility Checking"
      + "\n3. Show the Table"
      + "\n4. Exemplification"
      + "\n5. Omni-optimization"
      + "\n6. Back to previous menu")

def to_cnf(line, attribute_table):
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