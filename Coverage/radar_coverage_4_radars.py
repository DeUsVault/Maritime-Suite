import pygad
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bresenham import bresenham
import csv


def draw_midpoint_circle(center_x, center_y, radius, grid_size):
    # Create the grid with zeros
    grid = np.zeros((grid_size, grid_size))
    grid_size = grid_size - 1
    # Set the midpoint of the grid to the center of the circle
    mid_x, mid_y = center_x, center_y

    # Initialize variables
    x = radius - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (radius << 1)

    # Loop until the circle is complete
    while x >= y:
        # Plot the 8 points of the circle
        if mid_x + x < grid_size and mid_y + y < grid_size:
            grid[mid_x + x, mid_y + y] = 1
        elif mid_x + x >= grid_size and mid_y + y < grid_size:
            grid[grid_size, mid_y + y] = 1
        elif mid_x + x < grid_size and mid_y + y >= grid_size:
            grid[mid_x + x, grid_size] = 1
        else:
            grid[grid_size, grid_size] = 1

        if mid_x + y < grid_size and mid_y + x < grid_size:
            grid[mid_x + y, mid_y + x] = 1
        elif mid_x + y >= grid_size and mid_y + x < grid_size:
            grid[grid_size, mid_y + x] = 1
        elif mid_x + y < grid_size and mid_y + x >= grid_size:
            grid[mid_x + y, grid_size] = 1
        else:
            grid[grid_size, grid_size] = 1

        if mid_x - y >= 0 and mid_y + x < grid_size:
            grid[mid_x - y, mid_y + x] = 1
        elif mid_x - y < 0 and mid_y + x < grid_size:
            grid[0, mid_y + x] = 1
        elif mid_x - y >= 0 and mid_y + x >= grid_size:
            grid[mid_x - y, grid_size] = 1
        else:
            grid[0, grid_size] = 1

        if mid_x - x >= 0 and mid_y + y < grid_size:
            grid[mid_x - x, mid_y + y] = 1
        elif mid_x - x < 0 and mid_y + y < grid_size:
            grid[0, mid_y + y] = 1
        elif mid_x - x >= 0 and mid_y + y >= grid_size:
            grid[mid_x - x, grid_size] = 1
        else:
            grid[0, grid_size] = 1

        if mid_x - x >= 0 and mid_y - y >= 0:
            grid[mid_x - x, mid_y - y] = 1
        elif mid_x - x < 0 and mid_y - y >= 0:
            grid[0, mid_y - y] = 1
        elif mid_x - x >= 0 and mid_y - y < 0:
            grid[mid_x - x, 0] = 1
        else:
            grid[0, 0] = 1

        if mid_x - y >= 0 and mid_y - x >= 0:
            grid[mid_x - y, mid_y - x] = 1
        elif mid_x - y < 0 and mid_y - x >= 0:
            grid[0, mid_y - x] = 1
        elif mid_x - y >= 0 and mid_y - x < 0:
            grid[mid_x - y, 0] = 1
        else:
            grid[0, 0] = 1

        if mid_x + y < grid_size and mid_y - x >= 0:
            grid[mid_x + y, mid_y - x] = 1
        elif mid_x + y >= grid_size and mid_y - x >= 0:
            grid[grid_size, mid_y - x] = 1
        elif mid_x + y < grid_size and mid_y - x < 0:
            grid[mid_x + y, 0] = 1
        else:
            grid[grid_size, 0] = 1

        if mid_x + x < grid_size and mid_y - y >= 0:
            grid[mid_x + x, mid_y - y] = 1
        elif mid_x + x >= grid_size and mid_y - y >= 0:
            grid[grid_size, mid_y - y] = 1
        elif mid_x + x < grid_size and mid_y - y < 0:
            grid[mid_x + x, 0] = 1
        else:
            grid[grid_size, 0] = 1

        # Update variables
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (radius << 1)

    # Plot the grid
    # plt.imshow(grid, cmap='gray', origin='lower')
    # plt.show()
    return grid


def draw_circle(radius, x0, y0, covered_grid, grid):

    grid_size = len(grid.index)
    radar_height = grid.iloc[y0, x0]
    grid_matrix = grid.to_numpy()
    midpoint_grid = draw_midpoint_circle(y0, x0, radius, grid_size)

    # Find the positions where the value is equal to 1
    positions = np.where(midpoint_grid == 1)

    # Print the positions
    for row, col in zip(positions[0], positions[1]):
        # print(f"({row}, {col})")

        cells = list(bresenham(x0, y0, col, row))
        for element in cells:
            x = element[0]
            y = element[1]
            cell_height = grid_matrix[y][x]
            if cell_height > radar_height + 50:
                # break the loop since we do not want to add ones anymore across the line of sight
                # due to an obstacle in front of us
                break
            else:
                covered_grid[y][x] = 1
    return covered_grid


def check_radar_availability(solution, radar1_height, radar2_height, radar3_height, radar4_height):
    radar1_is_available, radar2_is_available, radar3_is_available, radar4_is_available = True, True, True, True

    if solution[0] == 0 and radar1_height > 0:
        # we cannot place a sea radar at land
        radar1_is_available = False
    elif solution[0] == 1 and radar1_height == 0:
        # we cannot place a land radar at sea
        radar1_is_available = False
    if solution[4] == 0 and radar2_height > 0:
        # we cannot place a sea radar at land
        radar2_is_available = False
    elif solution[4] == 1 and radar2_height == 0:
        # we cannot place a land radar at sea
        radar2_is_available = False

    if solution[8] == 0 and radar3_height > 0:
        # we cannot place a sea radar at land
        radar2_is_available = False
    elif solution[8] == 1 and radar3_height == 0:
        # we cannot place a land radar at sea
        radar2_is_available = False

    if solution[12] == 0 and radar4_height > 0:
        # we cannot place a sea radar at land
        radar2_is_available = False
    elif solution[12] == 1 and radar4_height == 0:
        # we cannot place a land radar at sea
        radar2_is_available = False

    return radar1_is_available, radar2_is_available, radar3_is_available, radar4_is_available


def extract_coordinates_from_chromosome(solution, grid):
    x1, y1 = solution[2], solution[3]
    x2, y2 = solution[6], solution[7]
    x3, y3 = solution[10], solution[11]
    x4, y4 = solution[14], solution[15]
    radar1_height = grid.iloc[y1, x1]
    radar2_height = grid.iloc[y2, x2]
    radar3_height = grid.iloc[y1, x1]
    radar4_height = grid.iloc[y2, x2]

    return x1, y1, x2, y2, x3, y3, x4, y4, radar1_height, radar2_height, radar3_height, radar4_height


def fitness_function(solution, solution_idx):
    # sea -> 0
    # land -> 1
    # solution = np.array([1, 1, 10, 12, 0, 1, 30, 35])
    grid = pd.read_csv('./data/grids/Grid.csv', header=None)
    radars = pd.read_csv('./data/radars.csv')

    x1, y1, x2, y2, x3, y3, x4, y4, radar1_height, radar2_height, radar3_height, radar4_height = extract_coordinates_from_chromosome(solution, grid)

    radar1_is_available, radar2_is_available, radar3_is_available, radar4_is_available = check_radar_availability(solution, radar1_height, radar2_height, radar3_height, radar4_height)

    covered_grid = np.zeros((grid_size, grid_size))
    # Place a 1 in the gird in a circle around the point the radar has been placed
    if radar1_is_available:
        covered_grid[y1][x1] = 1
        radar1_radius = radars['radius'][0]
        covered_grid = draw_circle(radius=radar1_radius, x0=x1, y0=y1, covered_grid=covered_grid, grid=grid)

    if radar2_is_available:
        covered_grid[y2][x2] = 1
        radar2_radius = radars['radius'][1]
        covered_grid = draw_circle(radius=radar2_radius, x0=x2, y0=y2, covered_grid=covered_grid, grid=grid)

    if radar3_is_available:
        covered_grid[y3][x3] = 1
        radar3_radius = radars['radius'][2]
        covered_grid = draw_circle(radius=radar3_radius, x0=x3, y0=y3, covered_grid=covered_grid, grid=grid)

    if radar4_is_available:
        covered_grid[y4][x4] = 1
        radar4_radius = radars['radius'][3]
        covered_grid = draw_circle(radius=radar4_radius, x0=x4, y0=y4, covered_grid=covered_grid, grid=grid)

    # Calculate the percentage of ones
    area_coverage = covered_grid.sum().sum() / covered_grid.size * 100

    return area_coverage


def mutation_func(offspring, ga_instance):
    mutated_offspring = offspring.copy()

    for chromosome_idx in range(offspring.shape[0]):
        grid = pd.read_csv('./data/grids/Grid.csv', header=None)
        GRID_SIZE=len(grid.index)
        # We don't want to mutate the first two bits of each radar sequence, i.e. the type (sea, land) and status
        # (active, inactive)
        # We need to find a more intelligent way to select these indexes
        exclude_indexes = [0, 1, 4, 5, 8, 9, 12, 13]

        random_gene_idx = np.random.choice(offspring.shape[1])
        while random_gene_idx in exclude_indexes:
            random_gene_idx = np.random.choice(offspring.shape[1])

        # Mutate either x or y location of one of the radars by a small margin
        # specify integer range of mutation of a radars location
        low = -1
        high = 2
        random_num = np.random.randint(low, high)
        while random_num == 0:
            random_num = np.random.randint(low, high)

        mutated_offspring[chromosome_idx, random_gene_idx] = offspring[chromosome_idx, random_gene_idx] + random_num

        # If after the mutation a gene has taken a value out of range, we discard it and keep the original gene
        if 0 <= mutated_offspring[chromosome_idx, random_gene_idx] < GRID_SIZE:
            # print("Successful mutation!")
            pass
        else:
            print("Unsuccessful mutation! Keeping the original gene.")
            mutated_offspring[chromosome_idx] = offspring[chromosome_idx]

    return mutated_offspring

def single_point_crossover_func(parents, offspring_size, ga_instance):
    offspring = []
    split_point = 8
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        parent1[split_point:] = parent2[split_point:]

        offspring.append(parent1)
        idx += 1

    return np.array(offspring)


def make_visualization(best_solution):
    grid = pd.read_csv('./data/grids/Grid.csv', header=None)
    grid_size = len(grid.index)
    final_grid = pd.DataFrame(np.zeros((grid_size, grid_size)))
    radars = pd.read_csv('./data/radars.csv')

    x1, y1, x2, y2, x3, y3, x4, y4, radar1_height, radar2_height, radar3_height, radar4_height = extract_coordinates_from_chromosome(
        solution, grid)

    radar1_is_available, radar2_is_available, radar3_is_available, radar4_is_available = check_radar_availability(
        solution, radar1_height, radar2_height, radar3_height, radar4_height)

    if radar1_is_available:
        final_grid[y1][x1] = 1
        radar1_radius = radars['radius'][0]
        final_grid = draw_circle(radius=radar1_radius, x0=x1, y0=y1, covered_grid=final_grid, grid=grid)
        best_solution[1] = 1
    else:
        best_solution[1] = 0

    if radar2_is_available:
        final_grid[y2][x2] = 1
        radar2_radius = radars['radius'][1]
        final_grid = draw_circle(radius=radar2_radius, x0=x2, y0=y2, covered_grid=final_grid, grid=grid)
        best_solution[5] = 1
    else:
        best_solution[1] = 0

    if radar3_is_available:
        final_grid[y3][x3] = 1
        radar3_radius = radars['radius'][2]
        final_grid = draw_circle(radius=radar3_radius, x0=x3, y0=y3, covered_grid=final_grid, grid=grid)
        best_solution[9] = 1
    else:
        best_solution[9] = 0

    if radar4_is_available:
        final_grid[y4][x4] = 1
        radar4_radius = radars['radius'][3]
        final_grid = draw_circle(radius=radar4_radius, x0=x4, y0=y4, covered_grid=final_grid, grid=grid)
        best_solution[13] = 1
    else:
        best_solution[13] = 0

    # Calculate the percentage of ones
    area_coverage = final_grid.sum().sum() / final_grid.size * 100

    covered_grid_matrix = final_grid.to_numpy()
    # Plot the matrix with a cell grid
    #plt.imshow(covered_grid_matrix, cmap='gray', interpolation='nearest')

    # Add a cell grid to the plot
    #plt.grid(True, which='both', color='red', linewidth=1)

    # Display the plot
    #plt.show()
    return best_solution

# Consider 2 radars
# For each radar:
# first number says if it is a sea radar->1 or a land radar->0
# second number says if the radar is active or not
# the next two number show the x,y location of the radar on the grid
# Therefore, we need

if __name__ == "__main__":
    radars = pd.read_csv('./data/radars.csv')
    radars_radius = radars['radius']
    radar_type = radars['type']

    grid = pd.read_csv('./data/grids/Grid.csv', header=None)
    grid_size = len(grid.index)

    # Call the function to draw a circle with center (25, 25) and radius 20
    # In case we want to specify a specific initialization:
    # initial_population = complete this line ...

    ga_instance = pygad.GA(num_generations=10000,
                           stop_criteria=["reach_70"],
                           num_parents_mating=2,
                           parent_selection_type='rws',
                           sol_per_pop=8,
                           num_genes=16,
                           gene_type=int,
                           fitness_func=fitness_function,
                           crossover_type=single_point_crossover_func,
                           mutation_type=mutation_func,

                           gene_space=[0 if radar_type[0] == 'sea' else 1,
                                       range(0, 2),
                                       range(0, grid_size),
                                       range(0, grid_size),
                                       0 if radar_type[1] == 'sea' else 1,
                                       range(0, 2),
                                       range(0, grid_size),
                                       range(0, grid_size),
                                       0 if radar_type[2] == 'sea' else 1,
                                       range(0, 2),
                                       range(0, grid_size),
                                       range(0, grid_size),
                                       0 if radar_type[3] == 'sea' else 1,
                                       range(0, 2),
                                       range(0, grid_size),
                                       range(0, grid_size)
                                       ])

    ga_instance.run()
    #ga_instance.plot_fitness()
    print('Initial Population')
    print(ga_instance.initial_population)

    print('\n')

    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    print('Final Population')
    print(ga_instance.population)

    print('\n')
    best_solution = make_visualization(best_solution=solution)
    print("Best solution : {solution}".format(solution=solution))
    print('\n')
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

    with open('radars4_position.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["active", "x", "y"])
        writer.writerow([best_solution[1], best_solution[2], best_solution[3]])
        writer.writerow([best_solution[5], best_solution[6], best_solution[7]])
        writer.writerow([best_solution[9], best_solution[10], best_solution[11]])
        writer.writerow([best_solution[13], best_solution[14], best_solution[15]])