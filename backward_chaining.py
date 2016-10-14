import sys
import getopt

cmd_input = False
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:h', ['input=', 'help'])
except getopt.GetoptError:
    print "Please enter -i <input file name>"
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print "Please enter -i <input file name>"
        sys.exit(2)
    elif opt in ('-i', '--input'):
        in_file = arg.strip()
        if len(in_file) > 0:
            cmd_input = True
        else:
            cmd_input = False
    else:
        print "Please enter -i <input file name>"
        sys.exit(2)

if cmd_input == False:
    print "Please enter -i <input file name>"
    sys.exit(2)
    
#read input file and store the values
input_file = open(in_file, "r")

query = input_file.readline().strip()
no_of_clauses_KB = int(input_file.readline())
fact = []
implication = []
for i in range(0,no_of_clauses_KB):
    input_line = input_file.readline().strip()
    implication_loc = input_line.find("=>")
    if implication_loc > -1:
        premises = input_line[:implication_loc - 1]
        premise = premises.split(" && ")
        consequent = input_line[implication_loc + 3:]
        imply = {"Consequent": consequent, "Premise": premise}
        implication.append(imply)
    else:
        fact.append(input_line)

def get_argument(clause):
    var1 = clause.split("(")[1]
    var2 = var1.split(")")[0]
    return var2

def get_predicate(clause):
    var1 = clause.split("(")[0]
    return var1

def check_variable(arg):
    if (arg.islower() == True):
        return True
    else:
        return False

def parse_facts(subgoal):
    subgoal_arg = get_argument(subgoal)
    subgoal_array = subgoal_arg.split(", ")
    subs = {}
    choice_point = []
    if check_variable(subgoal_arg):
        for j in range(len(choice_points)-1, -1, -1):
            if subgoal in choice_points[j]: 
                current_fact = choice_points[j][subgoal].pop(0)
                if not choice_points[j][subgoal]:
                    choice_points.pop(j)
                if (get_argument(current_fact).find(",") == -1):
                    subs.update({subgoal_arg: get_argument(current_fact)})
                else:
                    fact_arg = get_argument(current_fact)
                    fact_array = fact_arg.split(", ")
                    for k in range(0, len(subgoal_array)):
                        subs.update({subgoal_array[k]: fact_array[k]})
                output_file.write("True: " + current_fact + "\n")
                return True,subs
        for i in range(0, len(fact)):
            if get_predicate(subgoal) == get_predicate(fact[i]):
                choice_point.append(fact[i])
        if choice_point: 
            current_fact = choice_point.pop(0)
            if choice_point:
                choice_points.append({subgoal: choice_point})
            if (get_argument(current_fact).find(",") == -1):
                subs.update({subgoal_arg: get_argument(current_fact)})
            else:
                fact_arg = get_argument(current_fact)
                fact_array = fact_arg.split(", ")
                for k in range(0, len(subgoal_array)):
                    subs.update({subgoal_array[k]: fact_array[k]})
            output_file.write("True: " + current_fact + "\n")
            return True,subs
    else:
        for i in range(0, len(fact)):
            if subgoal == fact[i]:
                output_file.write("True: " + subgoal + "\n")
                return True,subs
        var_flag = False
        for k in range(0, len(subgoal_array)):
            if check_variable(subgoal_array[k]):
                var_flag = True
                break
        if var_flag == True:
            for j in range(len(choice_points)-1, -1, -1):
                if subgoal in choice_points[j]:
                    current_fact = choice_points[j][subgoal].pop(0)
                    if not choice_points[j][subgoal]:
                        choice_points.pop(j)
                    current_fact_arg = get_argument(current_fact)
                    current_fact_array = current_fact_arg.split(", ")
                    for k in range(0, len(subgoal_array)):
                        if check_variable(subgoal_array[k]):
                            subs.update({subgoal_array[k]: current_fact_array[k]})
                    output_file.write("True: " + current_fact + "\n")
                    return True,subs
            for i in range(0, len(fact)):
                if get_predicate(subgoal) == get_predicate(fact[i]):
                    constant_flag = True
                    fact_arg = get_argument(fact[i])
                    fact_array = fact_arg.split(", ")
                    for k in range(0, len(subgoal_array)):
                        if check_variable(subgoal_array[k]) == False:
                            if subgoal_array[k] != fact_array[k]:
                                constant_flag = False
                                break
                    if constant_flag == True:
                        choice_point.append(fact[i])
            if choice_point:
                current_fact = choice_point.pop(0)
                if choice_point:
                    choice_points.append({subgoal: choice_point})
                current_fact_arg = get_argument(current_fact)
                current_fact_array = current_fact_arg.split(", ")
                for k in range(0, len(subgoal_array)):
                    if check_variable(subgoal_array[k]):
                        subs.update({subgoal_array[k]: current_fact_array[k]})
                output_file.write("True: " + current_fact + "\n")
                return True,subs
    return False,subs

def backtrack(local_subs, no_return_subs):
    bc_subs = {}
    cp_flag = True
    while (cp_flag):
        back_goal = goal.pop()
        for key in back_goal:
            if key == "Cons":
                pass
            else:
                for j in range(len(choice_points)-1, -1, -1):
                    if back_goal[key] in choice_points[j]:
                        cp_flag = False
                        back_goal_arg = get_argument(back_goal[key])
                        back_goal_array = back_goal_arg.split(", ")
                        for k in range(0, len(back_goal_array)):
                            if check_variable(back_goal_array[k]):
                                back_goal_array[k] = "_"
                        print_goal = get_predicate(back_goal[key]) + "(" + ", ".join(back_goal_array) + ")"
                        output_file.write("Ask: " + print_goal + "\n")
                        goal.append(back_goal)
                        bc_flag,bc_subs = backward_chaining(back_goal[key])
                        local_subs.update(bc_subs)
                        if bc_flag == True:
                            cons_flag = True
                            if cp_stack:
                                next_item = cp_stack[len(cp_stack)-1]
                                if next_item["Cons"] == back_goal["Cons"]:
                                    cons_flag = False
                            if cons_flag:
                                subgoal_predicate = get_predicate(back_goal["Cons"])
                                subgoal_argument = get_argument(back_goal["Cons"])
                                subgoal_array = subgoal_argument.split(", ")
                                for i in range(0, len(implication)):
                                    if subgoal_predicate == get_predicate(implication[i]["Consequent"]):
                                        consequent_arg = get_argument(implication[i]["Consequent"])
                                        consequent_array = consequent_arg.split(", ")
                                        for k in range(0, len(subgoal_array)):
                                            if check_variable(subgoal_array[k]) and check_variable(consequent_array[k]):
                                                if consequent_array[k] in local_subs:
                                                    temp_var = local_subs[consequent_array[k]]
                                                    del local_subs[consequent_array[k]]
                                                    local_subs.update({subgoal_array[k]: temp_var})
                                                    subgoal_array[k] = temp_var
                                            elif check_variable(subgoal_array[k]):
                                                if subgoal_array[k] in local_subs:
                                                    subgoal_array[k] = local_subs[subgoal_array[k]]
                                        subgoal = subgoal_predicate + "(" + (", ".join(subgoal_array)) + ")"
                                        output_file.write("True: " + subgoal + "\n")
                        else:
                            return False, bc_subs
                    else:
                        cp_stack.append(back_goal)
                    break
    while (cp_stack):
        back_goal = cp_stack.pop()
        for key in back_goal:
            if key == "Cons":
                pass
            else:
                key_arg = get_argument(key)
                key_array = key_arg.split(", ")
                for k in range(0, len(key_array)):
                    if check_variable(key_array[k]):
                        if key_array[k] in no_return_subs:
                            key_array[k] = no_return_subs[key_array[k]]
                        if key_array[k] in local_subs:
                            key_array[k] = local_subs[key_array[k]]
                premise_arg = ", ".join(key_array)
                print_premise_array = key_array
                for k in range(0, len(print_premise_array)):
                    if check_variable(print_premise_array[k]):
                        print_premise_array[k] = "_"
                new_goal = get_predicate(key) + "(" + premise_arg + ")"
                print_goal = get_predicate(key) + "(" + ", ".join(print_premise_array) + ")"
                goal.append({key: new_goal, "Cons": back_goal["Cons"]})
                output_file.write("Ask: " + print_goal + "\n")
                bc_flag,bc_subs = backward_chaining(new_goal)
                local_subs.update(bc_subs)
                if bc_flag == True:
                    cons_flag = True
                    if cp_stack:
                        next_item = cp_stack[len(cp_stack)-1]
                        if next_item["Cons"] == back_goal["Cons"]:
                            cons_flag = False
                    if cons_flag:
                        subgoal_predicate = get_predicate(back_goal["Cons"])
                        subgoal_argument = get_argument(back_goal["Cons"])
                        subgoal_array = subgoal_argument.split(", ")
                        for i in range(0, len(implication)):
                            if subgoal_predicate == get_predicate(implication[i]["Consequent"]):
                                consequent_arg = get_argument(implication[i]["Consequent"])
                                consequent_array = consequent_arg.split(", ")
                                for k in range(0, len(subgoal_array)):
                                    if check_variable(subgoal_array[k]) and check_variable(consequent_array[k]):
                                        if consequent_array[k] in local_subs:
                                            temp_var = local_subs[consequent_array[k]]
                                            del local_subs[consequent_array[k]]
                                            local_subs.update({subgoal_array[k]: temp_var})
                                            subgoal_array[k] = temp_var
                                    elif check_variable(subgoal_array[k]):
                                        if subgoal_array[k] in local_subs:
                                            subgoal_array[k] = local_subs[subgoal_array[k]]
                                subgoal = subgoal_predicate + "(" + (", ".join(subgoal_array)) + ")"
                                output_file.write("True: " + subgoal + "\n")
                else:
                    return False, bc_subs
    return True, local_subs
    
def backward_chaining(subgoal):
    subgoal_arg = get_argument(subgoal)
    subgoal_array = subgoal_arg.split(", ")
    print_subgoal_array = subgoal_arg.split(", ")
    for j in range(0, len(print_subgoal_array)):
        if check_variable(print_subgoal_array[j]):
            print_subgoal_array[j] = "_"
    subs = {}
    fact_flag,subs = parse_facts(subgoal)
    if fact_flag == True:
        return True,subs
                            
    flag = False
    or_flag = False
    for i in range(0, len(implication)):
        if get_predicate(subgoal) == get_predicate(implication[i]["Consequent"]):
            if or_flag == True:
                output_file.write("Ask: " + get_predicate(subgoal)+ "(" +", ".join(print_subgoal_array) + ")" + "\n")
            flag = True
            local_subs = {}
            no_return_subs = {}
            consequent_arg = get_argument(implication[i]["Consequent"])
            consequent_array = consequent_arg.split(", ")
            if (check_variable(subgoal_arg) == False):
                if subgoal_arg.find(",") == -1 and consequent_arg not in no_return_subs:
                    no_return_subs.update({consequent_arg: subgoal_arg})
                else:
                    for k in range(0, len(consequent_array)):
                        if check_variable(consequent_array[k]) and check_variable(subgoal_array[k])==False:
                            no_return_subs.update({consequent_array[k]: subgoal_array[k]})
                        if check_variable(subgoal_array[k]) and check_variable(consequent_array[k])==False:
                            local_subs.update({subgoal_array[k]: consequent_array[k]})

            and_flag = True
            for j in range(0, len(implication[i]["Premise"])):
                premise_arg = get_argument(implication[i]["Premise"][j])
                premise_array = premise_arg.split(", ")
                for k in range(0, len(premise_array)):
                    if check_variable(premise_array[k]):
                        if premise_array[k] in no_return_subs:
                            premise_array[k] = no_return_subs[premise_array[k]]
                        if premise_array[k] in local_subs:
                            premise_array[k] = local_subs[premise_array[k]]
                premise_arg = ", ".join(premise_array)
                print_premise_array = premise_array
                for k in range(0, len(print_premise_array)):
                    if check_variable(print_premise_array[k]):
                        print_premise_array[k] = "_"
                new_goal = get_predicate(implication[i]["Premise"][j]) + "(" + premise_arg + ")"
                print_goal = get_predicate(implication[i]["Premise"][j]) + "(" + ", ".join(print_premise_array) + ")"
                goal.append({implication[i]["Premise"][j]: new_goal, "Cons": subgoal})
                if new_goal == subgoal:
                    return False, subs
                output_file.write("Ask: " + print_goal + "\n")
                bc_flag,bc_subs = backward_chaining(new_goal)
                local_subs.update(bc_subs)
                if (bc_flag == False):
                    while choice_points:
                        bc_flag,bc_subs = backtrack(local_subs, no_return_subs)
                        local_subs.clear()
                        local_subs.update(bc_subs)
                        if bc_flag == True:
                            break
                    if bc_flag == True:
                        return True,local_subs
                    else:
                        and_flag = False
                    break
            if and_flag == True:
                for k in range(0, len(subgoal_array)):
                    if check_variable(subgoal_array[k]) and check_variable(consequent_array[k]):
                        if consequent_array[k] in local_subs:
                            temp_var = local_subs[consequent_array[k]]
                            del local_subs[consequent_array[k]]
                            local_subs.update({subgoal_array[k]: temp_var})
                            subgoal_array[k] = temp_var
                    elif check_variable(subgoal_array[k]):
                        if subgoal_array[k] in local_subs:
                            subgoal_array[k] = local_subs[subgoal_array[k]]
                subgoal = get_predicate(subgoal) + "(" + (", ".join(subgoal_array)) + ")"
                output_file.write("True: " + subgoal + "\n")
                return True,local_subs
            or_flag = True
    else:
        output_file.write("False: " + get_predicate(subgoal)+ "(" +", ".join(print_subgoal_array) + ")" + "\n")
        return False,subs
    output_file.write(str(flag) + ": " + subgoal + "\n")
    return flag,subs

#create output file to print the inference
output_file = open("output.txt", "w")

goal = []
substitution = {}
choice_points = []
cp_stack = []
query_array = query.split(" && ")
query_flag = True
for i in range(0, len(query_array)):
    query_arg = get_argument(query_array[i])
    query_arg_array = query_arg.split(", ")
    for j in range(0, len(query_arg_array)):
        if check_variable(query_arg_array[j]):
            query_arg_array[j] = "_"

    goal.append({query_array[i]: query_array[i]}) 
    output_file.write("Ask: " + get_predicate(query_array[i]) + "(" + ", ".join(query_arg_array) + ")" + "\n")
    bc_result,substitution = backward_chaining(query_array[i])
    if bc_result == False:
        query_flag = False
        break
output_file.write(str(query_flag))

#close output file
output_file.close()
