def print_middle(column, grid_size):
    print(('|' + ' ' * grid_size) * column + '|')

def print_boundary(column, grid_size):
    print(('+' + '-' * grid_size) * column + '+')

def main():
    row = int(input('Number of rows: '))
    column = int(input('Number of column: '))
    grid_size = int(input('Grid size: '))

    print_boundary(column, grid_size)
    for i in range(row):
        for j in range(grid_size):
            print_middle(column, grid_size)
        print_boundary(column, grid_size)

if __name__ == '__main__':
    main()
