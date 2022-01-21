from random import uniform, randint, shuffle

def readinput(lines, NULLCHAR='0'):
    grid = [[] for _ in range(9)]
    for j in range(9):
            lineval = []
            for value in lines[j].split(' '):
                lineval.append(int(value) if value != NULLCHAR else None)
            for i in range(len(lineval)):
                grid[int(i/3) + int(j/3)*3].append(lineval[i])
    return grid

def sameColumn(i, j, itself=True): #returns indices
    ret = []
    for a in range(i % 3, 9, 3):
        for b in range(j % 3, 9, 3):
            if (a, b) == (i, j) and not itself:
                continue
            ret.append((a, b))
    return ret

def sameSubgrid(i, j, itself=True): #returns indices
    ret = []
    for k in range(9):
        if k == j and not itself:
            continue
        ret.append((i, k))
    return ret

def sameRow(i, j, itself=True): #returns indices
    ret = []
    for a in range(int(i / 3) * 3, int(i / 3) * 3 + 3):
        for b in range(int(j / 3) * 3, int(j / 3) * 3 + 3):
            if (a, b) == (i, j) and not itself:
                continue
            ret.append((a, b))
    return ret

def getCells(grid, indexes): #returns elements' values
    return [grid[i][j] for i,j in indexes]

def generateGrid():
    return [[list(range(1,10)) for _ in range(9)] for __ in range(9)]

def copyGrid(grid):
    return [[grid[i][j] for j in range(9)] for i in range(9)]

def mark(i, j, grid, track):
    ssg = sameSubgrid(i, j, False)
    for a, b in ssg:
        try:
            track[a][b].remove(grid[i][j])
        except (ValueError, AttributeError):
            pass
    sr = sameRow(i, j, False)
    for a, b in sr:
        try:
            track[a][b].remove(grid[i][j])
        except (ValueError, AttributeError):
            pass
    sc = sameColumn(i, j, False)
    for a, b in sc:
        try:
            track[a][b].remove(grid[i][j])
        except (ValueError, AttributeError):
            pass
    return grid, track

def fillCells(grid):
    track = generateGrid()
    for i in range(9):
        for j in range(9):
            if grid[i][j] != None:
                grid, track = mark(i, j, grid, track)

    while True:
        flag = False
        for i in range(9):
            for j in range(9):
                if track[i][j] == None:
                    continue
                if len(track[i][j]) == 0:
                    raise Exception('Not solvable!')
                elif len(track[i][j]) == 1:
                    grid[i][j] = track[i][j][0]
                    grid, track = mark(i, j, grid, track)
                    track[i][j], flag = None, True
        if not flag:
            break

    return grid

def initialPopulation(grid, population_size): 
    candids = []
    for count in range(population_size):
        candid = [[None for _ in range(9)] for __ in range(9)]
        for i in range(9):
            shuffled = [n for n in range(1, 10)] #initialization
            shuffle(shuffled)
            for j in range(9):
                if grid[i][j] != None:
                    candid[i][j] = grid[i][j]
                    shuffled.remove(grid[i][j])
            for j in range(9):
                if candid[i][j] == None:
                    candid[i][j] = shuffled.pop()
        candids.append(candid)
    return candids

def fitness(grid):
    duplicated = 0
    for a, b in sameColumn(0, 0):
        row = getCells(grid, sameRow(a, b))
        duplicated += len(row)-len(set(row))
    for a, b in sameRow(0, 0):
        col = getCells(grid, sameColumn(a, b))
        duplicated += len(col)-len(set(col))
    return duplicated

def selection(candids, selectionrate):
    fits = []
    for i in range(len(candids)):
        fits.append(tuple([i, fitness(candids[i])]))
    fits.sort(key=lambda e: e[1])
    selected = fits[0: int(len(fits)*selectionrate)]
    indexes = [elem[0] for elem in selected]
    return [candids[i] for i in indexes]

def solve(grid, population_size, selectionrate, maxgencount, mutationrate):
    grid = copyGrid(grid)
    fillCells(grid)
    population = initialPopulation(grid, population_size)
    for i in range(maxgencount):
        population = selection(population, selectionrate)
        if i == maxgencount - 1 or fitness(population[0]) == 0:
            break
        shuffle(population)
        new_population = []
        while True:
            c1, c2 = None, None
            try:
                c1 = population.pop()
            except IndexError:
                break
            try:
                c2 = population.pop()
            except IndexError:
                new_population.append(c2)
                break
            crossover = randint(0, 7) #swapping two elements of same subgrid
            c1[crossover], c2[crossover+1] = c2[crossover+1], c1[crossover]
            new_population.extend([c1, c2])

        # mutation
        for candid in new_population:
            if uniform(0,1) <= mutationrate:
                randSubgrid = randint(0, 8)
                to_swap = []
                for gi in range(9):
                    if grid[randSubgrid][gi] == None:
                        to_swap.append(gi)
                if len(to_swap) > 1:
                    shuffle(to_swap)
                    i1 = to_swap.pop()
                    i2 = to_swap.pop()
                    candid[randSubgrid][i1], candid[randSubgrid][i2] = candid[randSubgrid][i2], candid[randSubgrid][i1]

        population.extend(new_population)

    return population[0]

def getOutput(solution):
    outstr = ""
    for a, b in sameColumn(0, 0):
        row = getCells(solution, sameRow(a, b))
        outstr += " ".join([str(elem) for elem in row]) + '\n'
    return outstr

def main():
    POPULATIONSIZE = 350000
    SELECTIONRATE = 0.7
    MAXGENCOUNT = 13000
    MUTATIONRATE = 0.08
    FILE = "Test2.txt"
    OUTFILE = "Test2-MySol.txt"
    NULLCHAR = '0'
    NEWLINE = '\n'
    with open(FILE, "r") as infile:
        lines = infile.read().split(NEWLINE)
        grid = readinput(lines, NULLCHAR)
        try:
            solution = solve(grid, POPULATIONSIZE, SELECTIONRATE, MAXGENCOUNT, MUTATIONRATE)
            outstr = getOutput(solution)
            with open(OUTFILE, "w") as outfile:
                outfile.write(outstr)
            print(outstr)
        except:
            exit('Not solvable!')

main()