import re
import string

supported_postfix_symbols = '+-*/'
ERROR_STR = '#ERR'


def is_reference(token):
    return bool(re.search('[a-z]+[0-9]+', token))


def xy_to_rc(x, y):
    row = y + 1
    col = string.ascii_lowercase[x]
    return '{}{}'.format(col, row)


def rc_to_xy(rc):
    x = string.ascii_lowercase.find(rc[0])
    y = int(rc[1:]) - 1
    return x, y


def evaluate_postfix(tokens):
    """
    Expect list of int or string of int or supported_postfix_symbols

    :param tokens:
    :return:
    """
    if not tokens:
        return 0
    if not tokens[0]:
        return 0

    stack = []
    try:
        for token in tokens:
            if str(token) in supported_postfix_symbols:
                try:
                    if token == '+':
                        stack.append(stack.pop() + stack.pop())
                    elif token == '-':
                        stack.append(stack.pop() - stack.pop())
                    elif token == '*':
                        stack.append(stack.pop() * stack.pop())
                    elif token == '/':
                        stack.append(stack.pop() / stack.pop())
                except:
                    raise Exception('Invalid postfix input, too many operators')
            else:
                try:
                    value = int(token)
                    stack.append(value)
                except:
                    raise Exception('Invalid postfix: invalid token')

        if len(stack) != 1:
            raise Exception('Invalid postfix: too few operators')

        return stack[0]
    except:
        return ERROR_STR
