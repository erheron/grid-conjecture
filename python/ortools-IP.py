from ortools.linear_solver import pywraplp
import argparse

# Integer programming
def add_grid_constraints(solver, x):
    for i in range(5):
        if i == 0 or i == 4:
            solver.Add(7*sum(x[i,j] for j in range(5)) == 2*x['n'])
        else:
            solver.Add(7*sum(x[i,j] for j in range(5)) == x['n'])
    for j in range(5):
        if j == 0 or j == 4:
            solver.Add(7*sum(x[i,j] for i in range(5)) == 2*x['n'])
        else:
            solver.Add(7*sum(x[i,j] for i in range(5)) == x['n'])


def create_variables_with_basic_constraints(solver, x):
    # create variables
    for i in range(5):
        for j in range(5):
            x[(i,j)] = solver.IntVar(0, solver.infinity(), 'x_{}_{}'.format(i,j))
    x['delta'] = solver.IntVar(1, solver.infinity(), 'delta')
    x['n'] = solver.IntVar(7, solver.infinity(), 'n')

    # Add natural constraints
    solver.Add(x['delta'] <= x['n'])

    # sum of x[i,j] == n
    all_ij =[(i, j) for i in range(5) for j in range(5)]
    solver.Add(sum(x[i,j] for i,j in all_ij) == x['n'])


def add_subset_constraints(solver, subset, x):
    # subset is a list of 4-tuples (x_ul, y_ur, x_br, y_br)
    for l in range(len(subset)//4):
        l2 = 4*l
        rect_coords = [(i,j) for i in range(subset[l2], subset[l2 + 2])
                             for j in range(subset[l2 + 1], subset[l2 + 3])]
        solver.Add(7*sum(x[i,j] for i,j in rect_coords) >= 2*x['n'] + 7*x['delta'])
        # 7 * x[i,j] >= 2*n+ 7*delta

def main():
    cnt=0
    parser = argparse.ArgumentParser(description='Provide filename for input data')
    parser.add_argument('ifile', metavar ='ifile', type=str, help='Filename for input data')
    args = parser.parse_args()
    with open(args.ifile) as ifile:
        for line in ifile:
            subset = [int(x) for x in line.split()]

            solver = pywraplp.Solver('grid-conjceture', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
            solver.SetNumThreads(4)

            x={}
            create_variables_with_basic_constraints(solver, x)
            add_grid_constraints(solver, x)
            add_subset_constraints(solver, subset, x)

            # objective is to minimize delta, but remember that delta is >= 1 and integer
            solver.Minimize(x['delta'])

            status = solver.Solve()
            status_dict = {pywraplp.Solver.INFEASIBLE : ' proven infeasible',
                           pywraplp.Solver.UNBOUNDED  : ' proven unbounded'
                           }
                            
            if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
                print(f'Subset nr. {cnt} is OK')
                for i in range(5):
                    for j in range(5):
                        if j < 5:
                            print(f'{x[i,j].solution_value()} ', end=' ')
                        else:
                            print(f'{x[i,j].solution_value()} ')
                print('Delta: {}'.format(x['delta'].solution_value()))
            else:
                print(f'{status_dict[status]}')
            cnt += 1

if __name__ == '__main__':
    main()
