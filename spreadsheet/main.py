import os
import csv
import re
import string

import helpers


class Spreadsheet:
    def __init__(self):
        self.formulae = []
        self._precedents = []
        self._dependents = []
        self.values = []

    def load_csv(self, csv_path, csv_input_file):
        csv_file = os.path.join(csv_path, csv_input_file)
        with open(csv_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                new_row = []
                for col in row:
                    cell = re.split('\s+', col.strip().lower())
                    new_row.append(cell)
                self.formulae.append(new_row)

                self.values.append([None for _ in new_row])
                self._precedents.append([[] for _ in new_row])
                self._dependents.append([[] for _ in new_row])

    def evaluate(self):
        self._set_precedents_and_dependents()
        self._compute()

    def _set_precedents_and_dependents(self):
        for y, row_formulae in enumerate(self.formulae):
            row = y + 1
            for x, cell_formula in enumerate(row_formulae):
                col = string.ascii_lowercase[x]
                for token in cell_formula:
                    if helpers.is_reference(token):
                        this_xy = (x, y)
                        other_xy = helpers.rc_to_xy(token)
                        other_x = other_xy[0]
                        other_y = other_xy[1]
                        self._precedents[y][x].append(other_xy)
                        self._dependents[other_y][other_x].append(this_xy)

    def _compute(self):
        precedents_satisfied = [[not cell for cell in row] for row in self._precedents]

        remaining_cells = []
        precedents_newly_satisfied = []

        for y, row_fomulae in enumerate(self.formulae):
            for x, cell_formula in enumerate(row_fomulae):
                location = (x, y)
                remaining_cells.append(location)
                if precedents_satisfied[y][x]:
                    precedents_newly_satisfied.append(location)

        while len(precedents_newly_satisfied) > 0:
            location = precedents_newly_satisfied.pop()
            x = location[0]
            y = location[1]

            dependents = self._dependents[y][x]
            for dependent in dependents:
                dependent_x = dependent[0]
                dependent_y = dependent[1]
                self._precedents[dependent_y][dependent_x].remove(location)
                if not self._precedents[dependent_y][dependent_x]:
                    precedents_newly_satisfied.append(dependent)

            formula = self.formulae[y][x]
            tokens = self._fill_in_references(formula)
            value = helpers.evaluate_postfix(tokens)
            self.values[y][x] = value
            remaining_cells.remove(location)

    def _fill_in_references(self, formula):
        dereferenced_formula = []
        for token in formula:
            if helpers.is_reference(token):
                x, y = helpers.rc_to_xy(token)
                value = self.values[y][x]
                dereferenced_formula.append(value)
            else:
                dereferenced_formula.append(token)
        return dereferenced_formula

    def output_result(self, csv_path, csv_output_file):
        csv_file = os.path.join(csv_path, csv_output_file)
        with open(csv_file, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in self.values:
                writer.writerow(row)


if __name__ == '__main__':
    csv_path = os.getcwd()
    csv_input_file = 'sample_input.csv'
    csv_output_file = 'sample_output.csv'

    spreadsheet = Spreadsheet()
    spreadsheet.load_csv(csv_path=csv_path, csv_input_file=csv_input_file)
    spreadsheet.evaluate()
    spreadsheet.output_result(csv_path=csv_path, csv_output_file=csv_output_file)
