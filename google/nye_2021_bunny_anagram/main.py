from collections import defaultdict, OrderedDict
from copy import deepcopy

OUTPUT = "endrtednedd:/os....cp.rnnn.rhhps/.tt$sfeaiaaofd.ow.otooapa.asu./thhse"
TERMINATOR = "$"


def print_rows(rows):
    print("\n".join(["".join(row) for row in rows]))


def print_sort_table(cols):
    sort_table = map(list, zip(*cols))
    print_rows(rows=sort_table)


def get_descendants(left_col, right_col):
    """
    e.g.:
        get_descendants(first=[1,1,1,2,2,3], second=[4,4,5,5,6,7])
    returns:
        {1: {4: 2, 5: 1}, 2: {5: 1, 6: 1}, 3: {7: 1}}
    """
    descendants = defaultdict(lambda: defaultdict(int))
    for i, char in enumerate(left_col):
        next_char = right_col[i]
        descendants[char][next_char] += 1

    return descendants


def get_precedents(left_col, right_col):
    """
    e.g.:
        get_precedents(first=[1,1,1,2,2,3], second=[4,4,5,6,6,7])
    returns:
        {4: {1: 2}, 5: {1: 1, 2: 1}, 6: {2: 1}, 7: {3: 1}}
    """
    precedents = defaultdict(lambda: defaultdict(int))
    for i, char in enumerate(right_col):
        prev_char = left_col[i]
        precedents[char][prev_char] += 1

    return precedents


def rotate(base, n):
    """rotate list l to the left by n places"""
    return base[n:] + base[:n]


def get_second_col(first_col, descendants):
    """
    go thru each left letter by row
    find list of possible right letters
    try first one
    move down
    if run out of available letters,
        go back up
        put that letter back in available
        try next letter in above line
    """

    # List of descendant right letters for key left letter
    # if multiple right letter choices, try the most common one first
    letter_descendants = []
    for left_letter, right_letter_frequencies in descendants.items():
        right_letters = list(right_letter_frequencies.keys())
        right_letters.sort(key=lambda x: right_letter_frequencies[x], reverse=True)
        letter_descendants[left_letter] = right_letters

    remaining_letters = {
        left_letter: sum(right_letter_frequencies.values())
        for left_letter, right_letter_frequencies in descendants.items()
    }

    # keep track of which right letter index we're testing in letter_descendants list
    all_which_right_letter = {row: 0 for row in range(len(first_col))}

    # what order of the left_col rows should we attempt to match right_letter options
    row_order = list(all_which_right_letter.keys())
    row_order.sort(key=lambda x: (
        len(descendants[first_col[x]]),  # try letters with fewer unique descendants first
    ))

    second_col = [None] * len(first_col)
    row_order_index = 0  # start with highest priority row
    attempts = 0

    while any([i is None for i in second_col]):
        row = row_order[row_order_index]
        attempts += 1  # track how many permutations we've attempted
        row_order_index += 1
        left_letter = first_col[row]

        possible_right_letters = letter_descendants[left_letter]
        which_right_letter = all_which_right_letter[row]

        if which_right_letter >= len(possible_right_letters):
            returned_letter = second_col.pop()
            remaining_letters[returned_letter] += 1
            all_which_right_letter[row] = 0
            row_order_index -= 1
            row = row_order[row_order_index]
            all_which_right_letter[row] += 1
            continue

        right_letter = possible_right_letters[which_right_letter]

        if remaining_letters[right_letter] == 0:
            all_which_right_letter[row] += 1
            continue

        remaining_letters[right_letter] -= 1
        second_col.append(right_letter)
        row += 1

    return second_col


def get_input(output, term_char):
    # output is right-most column of array
    last_col = list(output)

    # first_col aka first col is sorted by definition, though there are duplicates
    first_col = list(output)
    first_col.sort(key=lambda x: x if x[0] != term_char else 'zz')

    descendants = get_descendants(left_col=last_col, right_col=first_col)
    precedents = get_precedents(left_col=last_col, right_col=first_col)

    cols = [first_col]
    second_col = get_second_col(first_col=first_col, descendants=descendants)
    cols.append(second_col)

    # now we have 2 examples of [left_letter, right_letter], also [letter_pair_1_2, third_letter]
    # so finding the third column should be easier

    print_sort_table(cols=cols)
    assert cols[-1] == last_col

    # first element of each column will be a rotated version of the input string
    input_rotated = [col[0] for col in cols]
    input_str = rotate(base=input_rotated, n=input_rotated.index(term_char) + 1)

    return input_str


def scramble(input_str, term_char):
    first_row = list(input_str) + [term_char]
    rotation_table = [first_row]
    for i in range(len(input_str)):
        rotation_table.append(rotate(base=first_row, n=i + 1))

    print()
    print_rows(rows=rotation_table)

    sort_table = rotation_table
    sort_table.sort(key=lambda x: x if x[0] != term_char else ['zz'])

    print()
    print_rows(rows=sort_table)

    output = [row[-1] for row in sort_table]

    print()
    print(output)


def main():
    input_str = get_input(output=OUTPUT, term_char=TERMINATOR)
    print(input_str)

    # scramble(input_str="1234123121", term_char=TERMINATOR)


if __name__ == "__main__":
    main()

'''

def order_dict(unordered_dict):
    """Use for finding a letter with only one possible next letter"""
    tuples = list(unordered_dict.items())
    tuples.sort(key=lambda x: len(x[1]))
    return OrderedDict(tuples)


def recursive_next_col(left_col, right_col, descendants):
    if not any([i is None for i in right_col]):
        return right_col

    left_letter = next(iter(descendants))
    right_letter = next(iter(descendants[left_letter]))
    index_to_place = next(i for i, letter in enumerate(left_col) if letter == left_letter and right_col[i] is None)
    right_col[index_to_place] = right_letter
    descendants[left_letter][right_letter] -= 1
    if descendants[left_letter][right_letter] == 0:
        descendants[left_letter].pop(right_letter)
        if len(descendants[left_letter]) == 0:
            descendants.pop(left_letter)

    recursive_next_col(left_col=left_col, right_col=right_col, descendants=descendants)


'''
