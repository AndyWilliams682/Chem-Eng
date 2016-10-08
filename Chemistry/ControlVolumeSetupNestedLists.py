# This function takes no inputs and allows for the creation of a control volume's properties to be organized into
# a nested array. The lowest arrays are formatted in direction (+1 for in, -1 for out), amount (total moles, mass or
# rates of each, 0 indicates an unknown amount of stuff), and fractions of said amounts for each compound in the mixture
# (negative values indicate an unknown and values > 1 depend on an unknown)


def control_volume_setup():
    paths = int(input('Input the number of paths crossing the control volume boundary: '))
    paths_in = int(input('Input the number of paths entering the control volume: '))

    balances = int(input('Input the number of materials in the control volume: '))
    control_volume_matrix = []

    for path in range(paths):
        control_volume_matrix.insert(path, [])

    path_counter = 1

    for path in control_volume_matrix:
        path.insert(0, 1)

        for value in range(balances + 2):
            if value == 0:
                if path_counter > paths_in:
                    path[value] = -1

            elif value == 1:
                path.insert(value, input('Input the total material going through path {}: '.format(path_counter)))

                if path[1] == '?':
                    path[value] = 0

                else:
                    path[value] = float(path[value])

            else:
                path.insert(value, list(input('Input the percentage of material [{}] going through path {}: '
                                        .format(chr(value - 2 + ord('A')), path_counter))))

                if '?' in path[value]:
                    position = path[value].index('?')
                    path[value][position] = '-1'
                    path[value] = ''.join(path[value])
                    path[value] = eval(path[value])

                else:
                    path[value] = float(''.join(path[value]))

        path_counter += 1

    return control_volume_matrix
