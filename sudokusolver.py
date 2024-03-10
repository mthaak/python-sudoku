def create_field_from_file(file_name):
    file = open(file_name)
    file_content = file.readlines()
    file.close()

    field = []
    for j in range(0, 9):
        file_content[j] = list(file_content[j].rstrip())
        row = []
        for i in range(0, 9):
            if file_content[j][i] == "_":
                row.append(None)
            else:
                row.append(int(file_content[j][i]))
        field.append(row)
    return (field)


def print_field(field):
    for j in range(0, 9):
        for i in range(0, 9):
            if field[j][i] == None:
                print(" ", end="")
            else:
                print(str(field[j][i]), end="")
            if i == 2 or i == 5:
                print("|", end="")
            else:
                print(" ", end="")
        print("")
        if j == 2 or j == 5:
            print("- - -+- - -+- - -")
    print("")


def add_number(field, possibilities, number, i, j):
    field[j][i] = number
    possibilities[j][i] = [False, False, False, False, False, False, False,
                           False, False]
    for k in range(0, 9):
        possibilities[j][k][number - 1] = False
        possibilities[k][i][number - 1] = False
    y = 3 * (j // 3)
    x = 3 * (i // 3)
    for l in range(y, y + 3):
        for k in range(x, x + 3):
            possibilities[l][k][number - 1] = False
    return (field, possibilities)


def generate_possibilities(field):
    #  Creates a 3d array where the third dimension indicates the possibilities
    #  for that cell which are all True by default
    possibilities = []
    for j in range(0, 9):
        row = []
        for i in range(0, 9):
            row.append([True, True, True, True, True, True, True,
                        True, True])
        possibilities.append(row)

    # For every known number, removes all the possibilities of that number in it's row, column and square
    for j in range(0, 9):
        for i in range(0, 9):
            if field[j][i] is not None:
                field, possibilities = add_number(field, possibilities,
                                                  field[j][i], i, j)
    return (possibilities, field)


def solve(field, possibilities):
    def single_candidate(field, possibilities):
        changes_made = False
        for j in range(0, 9):
            for i in range(0, 9):
                if field[j][i] is None and possibilities[j][i].count(True) == \
                        1:
                    found_number = possibilities[j][i].index(True) + 1
                    field, possibilities = add_number(field, possibilities,
                                                      found_number, i, j)
                    changes_made = True
        return (field, possibilities, changes_made)

    def solve_by_row(field, possibilities):
        changes_made = False
        for j in range(0, 9):
            possible = [[], [], [], [], [], [], [], [], [], []]
            for i in range(0, 9):
                for n in range(0, 9):
                    if possibilities[j][i][n]:
                        possible[n].append((i, j))

            for n in range(0, 9):
                if possible[n].__len__() == 1:
                    found_cell = possible[n].pop()
                    found_number = n + 1
                    field, possibilities = add_number(field, possibilities,
                                                      found_number,
                                                      found_cell[0],
                                                      found_cell[1])
                    changes_made = True

        return (field, possibilities, changes_made)

    def solve_by_column(field, possibilities):
        changes_made = False
        for i in range(0, 9):
            possible = [[], [], [], [], [], [], [], [], [], []]
            for j in range(0, 9):
                for n in range(0, 9):
                    if possibilities[j][i][n]:
                        possible[n].append((i, j))

            for n in range(0, 9):
                if possible[n].__len__() == 1:
                    found_cell = possible[n].pop()
                    found_number = n + 1
                    field, possibilities = add_number(field, possibilities,
                                                      found_number,
                                                      found_cell[0],
                                                      found_cell[1])
                    changes_made = True

        return (field, possibilities, changes_made)

    def solve_by_square(field, possibilities):
        changes_made = False
        for s in range(0, 3):
            for t in range(0, 3):
                possible = [[], [], [], [], [], [], [], [], [], []]
                for j in range(3 * t, 3 * t + 3):
                    for i in range(3 * s, 3 * s + 3):
                        for n in range(0, 9):
                            if possibilities[j][i][n]:
                                possible[n].append((i, j))

                for n in range(0, 9):
                    if possible[n].__len__() == 1:
                        found_cell = possible[n].pop()
                        found_number = n + 1
                        field, possibilities = add_number(field, possibilities,
                                                          found_number,
                                                          found_cell[0],
                                                          found_cell[1])
                        changes_made = True

        return (field, possibilities, changes_made)

    def single_location(field, possibilities):
        field, possibilities, changes_made = solve_by_row(field,
                                                          possibilities)
        field, possibilities, changes_made = solve_by_column(field,
                                                             possibilities)
        field, possibilities, changes_made = solve_by_square(field,
                                                             possibilities)
        return (field, possibilities, changes_made)

    changes_made = True
    while changes_made:
        while changes_made:
            field, possibilities, changes_made = single_candidate(field,
                                                                  possibilities)
        field, possibilities, changes_made = single_location(field,
                                                             possibilities)

    return (field)


file_name = "sudoku2.txt"
field = create_field_from_file(file_name)
print_field(field)
print("Becomes: \n")
possibilities, field = generate_possibilities(field)
field = solve(field, possibilities)
print_field(field)

# SudokuOfTheDay.com
