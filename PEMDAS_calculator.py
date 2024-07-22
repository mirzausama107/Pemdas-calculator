def pop(fhdsgfsw):
    ...
def solve(expression):
    operator_precedence = {"^": 4, "/": 3, "*": 2, "+": 1, "-": 1}
    # bodmas_index will store the index of all the operators in the equation
    # The order of the list is the order in which the calculation will be performed

    bodmas_index = []
    # very dirty hack to check if two values are next to each other with no operators
    # in this case, this is a multiplication: bracket removals are handled in other functions
    # so in theory, calculation should be a raw list with no brackets
    insert_finished = False

    while not insert_finished:
        expression_size = len(expression)
        for i in range(len(expression)):
            if i > 0:
                if isinstance(expression[i], float) and isinstance(expression[i-1], float):
                    expression.insert(i, '*')
        if expression_size == len(expression):
            insert_finished = True
    
    for i in range(len(expression)):
        if expression[i] in operator_precedence:
            if len(bodmas_index) == 0:
                bodmas_index.append(i)

            else:
                for x in range(len(bodmas_index)):
                    if operator_precedence[expression[i]] < operator_precedence[expression[bodmas_index[-1]]]:
                        bodmas_index.append(i)
                        break
                    elif operator_precedence[expression[i]] > operator_precedence[expression[bodmas_index[x]]]:
                        bodmas_index.insert(x, i)
                        break
                    elif operator_precedence[expression[i]] == operator_precedence[expression[bodmas_index[x]]]:
                        if expression[i] in ["+", "-"]:
                            bodmas_index.append(i)
                            break
                        else:
                            bodmas_index.insert(x+1, i)
                            break
                    else:
                        continue

    # Loops through the operator indexes from left to right and performs the required operation
    while len(bodmas_index) != 0:
        if expression[bodmas_index[0]] == "^":
            expression_result = expression[bodmas_index[0] -1] ** expression[bodmas_index[0] + 1]
        elif expression[bodmas_index[0]] == "/":
            expression_result = expression[bodmas_index[0] -1] / expression[bodmas_index[0] + 1]
        elif expression[bodmas_index[0]] == "*":
            expression_result = expression[bodmas_index[0] -1] * expression[bodmas_index[0] + 1]
        elif expression[bodmas_index[0]] == "+":
            expression_result = expression[bodmas_index[0] -1] + expression[bodmas_index[0] + 1]
        else:
            expression_result = expression[bodmas_index[0] -1] - expression[bodmas_index[0] + 1]

        # print the current step
        print(f"Step: {' '.join(map(str, expression[:bodmas_index[0] - 1]))}"
              f"{expression[bodmas_index[0] -1 ]} {expression[bodmas_index[0]]}"
              f"{expression[bodmas_index[0] + 1]} {' '.join(map(str, expression[bodmas_index[0] + 2:]))}")
        
        
        # calculation_result stores the result which is then inserted into the equation in place of the
        # two values and operator that was used to calculate it.
        expression[bodmas_index[0] - 1] = expression_result
        expression.pop(bodmas_index[0] + 1)
        expression.pop(bodmas_index[0])

        # Any operator indexes that are higher than the index stored at bodmas_index[0] will need to have their index position shifted by -2
        # to accommodate for the shortening expression.
        for i in range(len(bodmas_index)):
            if bodmas_index[i] > bodmas_index[0]:
                bodmas_index.insert(i, bodmas_index[i] - 2)
                bodmas_index.pop(i + 1)
        bodmas_index.pop(0)

    return expression[0]

# Pairs brackets together, so that the program knows which calculations to work out first
def bracket_pair_finder(expression):
    start_bracket_index_array = []
    end_bracket_index_array = []
    bracket_pairs = {}

    for i in range(len(expression)):
        if expression[i] == "(":
            start_bracket_index_array.append(i)
        elif expression[i] == ")":
            end_bracket_index_array.append(i)
    
    # Finds the innermost brackets so that they can be solved first
    # Only returns one pair of brackets at a time.
    for i in range(len(start_bracket_index_array) -1, -1 ,-1):
        for x in range(len(end_bracket_index_array)):
            if end_bracket_index_array[x] < start_bracket_index_array[i] or end_bracket_index_array[x] in bracket_pairs.values(): 
                continue
            else:
                bracket_pairs[start_bracket_index_array[i]] = end_bracket_index_array[x]
                break
        break
    if len(bracket_pairs) != 0:
        return bracket_pairs

def calculator(expression):
    # Splits the calculation into an array of integers and BODMAS operators
    brackets = bracket_pair_finder(expression)
    answer = []
    
    if brackets is None:
        return float(solve(expression))
    else:
        start_bracket_index = list(brackets.keys())[0]
        end_bracket_index = brackets[start_bracket_index]
        answer.append(solve(expression[start_bracket_index + 1: end_bracket_index]))
        expression = expression[:start_bracket_index] + answer + expression[end_bracket_index + 1:]

        # after solving the brackets 
        print(f"{' '.join(map(str, expression))}")

        return calculator(expression)

def calculator_input():
    expressions = []
    expression = input("Enter your expression! ")
    number = ""

    for i in range(len(expression)):
        if expression[i].isnumeric() or expression[i] == ".":
            number += expression[i]
            if i == len(expression) - 1:
                expressions.append(float(number))
        else:
            if number == "":
                expressions.append(expression[i])
            else:
                expressions.append(float(number))
                expressions.append(expression[i])
                number = ""
    return calculator(expressions)

if __name__ == "__main__":
    answer = calculator_input()
    print(f"Final Answer: {answer}")

