import random

components = {"ALU" : (5, 5),
              "Cache" : (7, 4),
              "ControlUnit" : (4, 4),
              "RegisterFile" : (6, 6),
              "Decoder" : (5, 3),
              "FloatingUnit" : (5, 5)
              }

def generate_population():
    chromosome = []
    for i in components.values():
        width, height = i
        x = random.randint(0, 25 - width)
        y = random.randint(0, 25 - height)
        chromosome.append((x, y))
    return chromosome

population = []
for i in range(6):
    chromosome = generate_population()
    population.append(chromosome)

j = 1
for chromosome in population:
    print(f"P{j}-> {chromosome}")
    j += 1

def overlapping(p1, s1, p2, s2):
    A_left, A_bottom = p1
    A_right = A_left + s1[0]
    A_top = A_bottom + s1[1]
    B_left, B_bottom = p2
    B_right = B_left + s2[0]
    B_top = B_bottom + s2[1]

    overlap = not (
        A_right <= B_left or
        A_left >= B_right or
        A_bottom >= B_top or
        A_top <= B_bottom
    )

    return overlap

interconnection = [
    ("RegisterFile", "ALU"),
    ("ControlUnit", "ALU"),
    ("ALU", "Cache"),
    ("RegisterFile", "FloatingUnit"),
    ("Cache", "Decoder"),
    ("Decoder", "FloatingUnit")
]

def center_to_center(p, s):
    x, y = p
    w, h = s

    center = x + w / 2 , y + h / 2
    return center

def euclidean_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance

def bounding_box_area(chromosome):
    components_names = list(components.keys())
    x_min_list = []
    x_max_list = []
    y_min_list = []
    y_max_list = []

    for i in range(len(chromosome)):
        x, y = chromosome[i]
        w, h = components[components_names[i]]
        x_min_list.append(x)
        x_max_list.append(x + w)
        y_min_list.append(y)
        y_max_list.append(y + h)

    min_x = min(x_min_list)
    max_x = max(x_max_list)
    min_y = min(y_min_list)
    max_y = max(y_max_list)

    area = (max_x - min_x) * (max_y - min_y)

    return area

def fitness_check(chromosome):
    components_names = list(components.keys())
    overlap_count = 0

    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            p1, s1 = chromosome[i], components[components_names[i]]
            p2, s2 = chromosome[j], components[components_names[j]]
            if overlapping(p1, s1, p2, s2):
                overlap_count += 1

    total_wiring = 0
    index = {}
    for i in range(len(components_names)):
        name = components_names[i]
        index[name] = i

    for a, b in interconnection:
        i = index[a]
        j = index[b]

        c1 = center_to_center(chromosome[i], components[a])
        c2 = center_to_center(chromosome[j], components[b])
        distance = euclidean_distance(c1[0], c1[1], c2[0], c2[1])
        total_wiring += distance

    area = bounding_box_area(chromosome)

    alpha = 1000
    beta = 2
    gamma = 1
    fitness_score = - (alpha * overlap_count + beta * total_wiring + gamma * area)

    return fitness_score, overlap_count, total_wiring, area

def parent_selection(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)

    while parent2 == parent1:
        parent2 = random.choice(population)

    return parent1, parent2


def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[ : point] + parent2[point : ]
    child2 = parent2[ : point] + parent1[point : ]

    return child1, child2

def mutation(chromosome, mutation_rate = 0.1):
    if random.random() < mutation_rate:
        index = random.randint(0, len(chromosome) - 1)
        component_sizes = list(components.values())
        w, h = component_sizes[index]
        x = random.randint(0, 25 - w)
        y = random.randint(0, 25 - h)
        chromosome[index] = (x, y)
    return chromosome

def create_new_generation(population):
    fitness_res = []
    for i in population:
        score = fitness_check(i)[0]
        fitness_res.append((score, i))

    fitness_res.sort(reverse = True)

    new_population = []

    best_chromosome = fitness_res[0][1]
    new_population.append(best_chromosome)

    while len(new_population) < len(population):
        p1, p2 = parent_selection(population)
        c1, c2 = single_point_crossover(p1, p2)
        c1 = mutation(c1)
        if len(new_population) < len(population):
            new_population.append(c1)
        c2 = mutation(c2)
        if len(new_population) < len(population):
            new_population.append(c2)

    return new_population

def ga(pop_size = 6, max_generations = 15, plateau = 3):
    population = []

    count = 0
    while count < pop_size:
        chromosome = generate_population()
        population.append(chromosome)
        count += 1

    best_fitness = float('-inf')
    best_chromosome = None
    plateau_count = 0

    for generation in range(max_generations):
        print(f"\nGeneration {generation + 1}")
        flag = False
        i = 0
        for chrom in population:
            fitness, overlaps, wiring, area = fitness_check(chrom)
            print(f"P{i + 1} -> Fitness: {fitness:.2f}, Overlaps: {overlaps}, Wiring: {wiring:.2f}, Area: {area}")
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chrom
                best_generation = generation + 1
                best_p_number = i + 1

                flag = True
            i += 1

        if not flag :
          plateau_count += 1
        else:
          plateau_count = 0
        if plateau_count >= plateau:
          break
        population = create_new_generation(population)

    print("\nBest Chromosome Found:")
    print(best_chromosome)
    fitness, overlaps, wiring, area = fitness_check(best_chromosome)
    print(f"Pairwise block overlap count = {overlaps}")
    print(f"Total wiring distance (center-to-center) of the specified connected pairs = {wiring:.2f}")
    print(f"Total bounding box area = {area}")
    print(f"Fitness for generation {best_generation} chromosome {best_p_number} = {fitness:.2f}")

    return best_chromosome

best_chromosome = ga()