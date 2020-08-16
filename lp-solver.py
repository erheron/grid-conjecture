from ortools.linear_solver import pywraplp
import argparse

# Linear programming 
def add_grid_constraints(solver, x, k):
    """
    solver:
        linear solver from ortools.linear_solver
    x:
        matrix of solver's variables of size (k+1) x (k+1)
    k:
        size of a net == number of horizontal (vertical) lines
        of a grid
    """
    n = k+1
    for i in range(n):
        if i == 0 or i == k:
            solver.Add((k+3)*sum(x[i,j] for j in range(n)) == 2)
        else:
            solver.Add((k+3)*sum(x[i,j] for j in range(n)) == 1)
    for j in range(n):
        if j == 0 or j == k:
            solver.Add((k+3)*sum(x[i,j] for i in range(n)) == 2)
        else:
            solver.Add((k+3)*sum(x[i,j] for i in range(n)) == 1)


def create_variables_with_basic_constraints(solver, x, k):
    """
    solver:
        linear solver from ortools.linear_solver
    x:
        matrix of solver's variables of size (k+1) x (k+1)
    k:
        size of a net == number of horizontal (vertical) lines
        of a grid
    """
    # create variables
    n = k+1
    for i in range(n):
        for j in range(n):
            x[(i,j)] = solver.NumVar(0, 1, 'x_{}_{}'.format(i,j))
    x['delta'] = solver.NumVar(0, 1, 'delta')

    # sum of x[i,j] == 1
    all_ij =[(i, j) for i in range(n) for j in range(n)]
    solver.Add(sum(x[i,j] for i,j in all_ij) == 1)


def add_subset_constraints(solver, subset, x, k):
    """
    solver:
        linear solver from ortools.linear_solver
    subset:
        list of rectangles in form "x1 y1 x2 y2"
        where x1 and y1 denote the upper left corner
        and x2, y2 denote the bottom right corner
    x:
        matrix of solver's variables of size (k+1) x (k+1)
    k:
        size of a net == number of horizontal (vertical) lines
        of a grid
    """
    for l in range(len(subset)//4):
        l2 = 4*l
        rect_coords = [(i,j) for i in range(subset[l2], subset[l2 + 2]+1)
                             for j in range(subset[l2 + 1], subset[l2 + 3]+1)]
        solver.Add((k+3)*sum(x[i,j] for i,j in rect_coords) >= 2 + (k+3)*x['delta'])
        # (k+3) * x[i,j] >= 2*n+ (k+3)*delta

def main():
    cnt=0
    parser = argparse.ArgumentParser(description='Provide filename for input data')
    parser.add_argument('ifile', metavar ='ifile', type=str, help='Filename for input data')
    parser.add_argument('k', metavar='k', type=int, help='Size of a net')
    parser.add_argument('--terminate', action='store_true', help='Terminate after first solution is found')
    args = parser.parse_args()
    with open(args.ifile) as ifile:
        for line in ifile:
            subset = [int(x) for x in line.split()]

            solver = pywraplp.Solver('grid-conjceture', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
            solver.SetNumThreads(4)

            x={}
            create_variables_with_basic_constraints(solver, x,args.k)
            add_grid_constraints(solver, x, args.k)
            add_subset_constraints(solver, subset, x, args.k)

            # objective is to maximize delta, we're operating on densities
            solver.Maximize(x['delta'])

            status = solver.Solve()
                            
            if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
                if x['delta'].solution_value() > 0.0:
                    n = args.k + 1
                    print(f'Subset nr. {cnt} encodes a counterexample')
                    for i in range(n):
                        for j in range(n):
                                print(f'X[{i}][{j}] = {x[i,j].solution_value()} ')
                    if parser.terminate:
                        return
            cnt += 1

if __name__ == '__main__':
    main()
