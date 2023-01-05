import re

# tokens plus their regex
BINARY_OP = '0'     # [+\-*/\^%]
UNARY_MINUS = '1'   # -
UNARY_FUNC = '2'    # sqrt|abs|sin|cos|tan
LP = '3'            # \(
RP = '4'            # \)
NUM = '5'           # ([0-9]+)|([0-9]+\.[0-9]+)|pi

# BNF grammar for arithmetic expressions
# <expr> ::= <unit> <expr_tail>
# <expr_tail> ::= BINARY_OP <unit> <expr_tail> | EOF
# <unit> ::= UNARY_MINUS <unit_tail> | <unit_tail>
# <unit_tail> ::= NUM | UNARY_FUNC <enclosed> | <enclosed>
# <enclosed> ::= LP <expr> RP


# converts the input into a stream of tokens
def scanner(input):
    # used to tokenize and differentiate the unary minus and subtraction operator
    def tokenize_unary_minus(input):
        i = 0
        input = list(input)
        if input[i] == '-':
            input[i] = UNARY_MINUS
        while i < len(input) - 1:
            if input[i + 1] == '-' and re.search("[+\-*/\^%\(]", input[i]) != None:
                input[i + 1] = UNARY_MINUS
            i += 1
        return ''.join(input)

    input = re.sub(r"\s+", "", input)
    input = re.sub("([0-9]+\.[0-9]+)|([0-9]+)|pi", NUM, input)
    input = tokenize_unary_minus(input)
    input = re.sub("\)", RP, input)
    input = re.sub("\(", LP, input)
    input = re.sub("sqrt|abs|sin|cos|tan", UNARY_FUNC, input)
    input = re.sub("[+\-*/\^%]", BINARY_OP, input)
    return input


# returns True if the input is a valid arithmetic expression
def parser(input):
    def expr(input):
        input = unit(input)
        input = expr_tail(input)
        return input

    def expr_tail(input):
        if len(input) == 0:
            return input
        if input[0] == BINARY_OP:
            input = unit(input[1:])
            input = expr_tail(input)
        return input

    def unit(input):
        if input[0] == UNARY_MINUS:
            input = unit_tail(input[1:])
        else:
            input = unit_tail(input)
        return input

    def unit_tail(input):
        if input[0] == NUM:
            input = input[1:]
        elif input[0] == UNARY_FUNC:
            input = enclosed(input[1:])
        else:
            input = enclosed(input)
        return input

    def enclosed(input):
        if input[0] == LP:
            input = expr(input[1:])
            if input[0] == RP:
                input = input[1:]
        return input

    input = scanner(input)
    input = expr(input)
    if len(input) == 0:
        return True
    else:
        return False


# example
expression = "-sqrt(5.342) * (3 % (9 ^ abs(-324.342) + (sin(cos(-pi)))))"
print("Is \"" + expression + "\" a valid arithmetic expression?")
print(parser(expression))
