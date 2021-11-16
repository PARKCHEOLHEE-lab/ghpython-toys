import cv2
import math
import copy
import random
import numpy as np


class Genome:
    chromosome = []
    fitness = 0

    def __getitem__(self, index):
        return self.chromosome[index]

    def __len__(self):
        return len(self.chromosome)

    def __repr__(self):
        return str(self.chromosome)

    def get_chromosome(self):
        return self.chromosome

    def set_chromosome(self, other_chromosome):
        self.chromosome = other_chromosome

    def get_fitness(self):
        return self.fitness    

    def set_fitness(self, fitness_value):
        self.fitness = fitness_value


class Chromosome:
    def __init__(self, city_coordinates):
        self.city_coordinates = city_coordinates
        self.genes = []

    def __getitem__(self, index):
        return self.genes[index]
    
    def configurate_chromosome(self, population_size, chromosome_size):
        origin = 0
        for _ in range(population_size):
            genome = Genome()
            chromosome = random.sample(range(1, chromosome_size), chromosome_size-1)
            chromosome.insert(0, origin)
            chromosome.append(origin)
            genome.set_chromosome(chromosome)
            genome.set_fitness(self.evaluate_chromosome(genome.chromosome))
            self.genes.append(genome)
        return self.genes

    def evaluate_chromosome(self, chromosome):
        evaluated_fitness = 0
        for i in range(len(chromosome)-1):
            curr_city = self.city_coordinates[chromosome[i]]
            next_city = self.city_coordinates[chromosome[i+1]]
            evaluated_fitness += self.evaluate_distance(curr_city, next_city)
        evaluated_fitness = round(evaluated_fitness, 2)
        return evaluated_fitness

    def evaluate_distance(self, city_1, city_2):
        x1, y1 = city_1
        x2, y2 = city_2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance


class GeneticAlgorithm:
    def __init__(self, city_coordinates, population_size, generation_limit, mutation_rate, map_path, cities_count, weakness_threshold, chromosome_size):
        self.weakness_threshold = weakness_threshold
        self.city_coordinates = city_coordinates
        self.generation_limit = generation_limit
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.cities_count = cities_count
        self.map_path = map_path

    def evaluate_fittest(self, genome):
        fitnesses = []
        for chromosome in genome:
            fitness = chromosome.get_fitness()
            fitnesses.append(fitness)

        i = fitnesses.index(min(fitnesses))
        fittest = genome[i]
        return fittest

    def tournament_selection(self, genome, count):
        selected_genome = []
        for _ in range(count):
            i = random.randrange(len(genome))
            selected_genome.append(genome[i])
            
        fittest = self.evaluate_fittest(selected_genome)
        return fittest

    def reproduction_genome(self, genome):
        parent_1 = self.tournament_selection(genome, 20)
        parent_2 = self.tournament_selection(genome, 20)

        while parent_1 == parent_2:
            parent_2 = self.tournament_selection(genome, 20)

        parents = [parent_1, parent_2]
        offspring = self.crossover_genome(parents)
        return offspring

    def crossover_genome(self, parents):
        origin = 0
        blank = -1
        parent_1, parent_2 = parents
        offspring = [blank] * (len(parent_1) - parent_1.get_chromosome().count(origin))
        offspring.insert(0, origin)
        offspring.append(origin)

        start = len(parent_1) // 3
        end = len(parent_1) - 4

        start = random.randrange(start, end)
    
        order_genes = parent_1[start:end]
        offspring[start:end] = order_genes
        difference_genes = copy.deepcopy(parent_2)
        for gene in order_genes:
            i = difference_genes.get_chromosome().index(gene)
            difference_genes.get_chromosome()[i] = origin
    
        while origin in difference_genes:
            difference_genes.get_chromosome().remove(origin)

        for gene in difference_genes:
            i = offspring.index(blank)
            offspring[i] = gene

        if random.randrange(0, 100) < self.mutation_rate:
            offspring = self.mutation_genome(offspring)

        offspring_genom = Genome()
        chromosome_object = Chromosome(self.city_coordinates)
        offspring_genom.set_chromosome(offspring)
        offspring_genom.set_fitness(chromosome_object.evaluate_chromosome(offspring_genom))
        # print('order_genes :', order_genes)
        # print('parent_1 :', parent_1)
        # print('parent_2 :', parent_2)
        # print('offspring_genom :', offspring_genom)
        # print()

        return offspring_genom

    def mutation_genome(self, offspring):
        mutation_repeat_count = 2
        for _ in range(mutation_repeat_count):
            p1, p2 = [random.randrange(1, len(offspring)-1) for _ in range(2)]

            while p1 == p2:
                p2 = random.randrange(1, len(offspring)-1)

            offspring[p1], offspring[p2] = offspring[p2], offspring[p1]
        return offspring

    def main(self):

        RED = (0,0,255)
        BLUE = (255,0,0)
        title = 'TSP'
        # text = 'Press any button to get started'

        travel_map = cv2.imread(self.map_path)
        for coord in self.city_coordinates:
            x, y = coord
            cv2.circle(travel_map, center=(x, y), radius=3, color=RED, thickness=-1, lineType=cv2.LINE_AA)

        # cv2.putText(travel_map, org=(10, 35), text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=BLUE, thickness=1, lineType=cv2.LINE_AA)
        cv2.imshow(title, travel_map)
        cv2.waitKey(0)
        chromosome_object = Chromosome(self.city_coordinates)
        population = chromosome_object.configurate_chromosome(population_size=self.population_size, chromosome_size=self.cities_count)


        generation = 1
        while generation < self.generation_limit:

            for _ in range(self.population_size // 2):
                population.append(self.reproduction_genome(population))

            for genome in population:
                fitness = genome.get_fitness()

                if fitness > self.weakness_threshold:
                    population.remove(genome)

            best_genome = self.evaluate_fittest(population)
            distance = best_genome.get_fitness()

            print("\n")
            print(f"Generation: {generation}\nDistance: {distance}\nBest Genome: {best_genome}")                  

            for i in best_genome:
                x, y = self.city_coordinates[i]
                cv2.circle(travel_map, center=(x, y), radius=3, color=RED, thickness=-1, lineType=cv2.LINE_AA)

                if i == 0:
                    cv2.putText(travel_map, org=(x, y), text='origin', color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, lineType=cv2.LINE_AA)

                else:
                    cv2.putText(travel_map, org=(x, y), text=f'{i}', color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3, lineType=cv2.LINE_AA)

            fancy_coordinates = np.array(self.city_coordinates)[best_genome]
            for i in range(len(fancy_coordinates)-1):
                curr_point = fancy_coordinates[i]
                next_point = fancy_coordinates[i+1]
                cv2.line(travel_map, curr_point, next_point, BLUE, 1, cv2.LINE_AA)

            cv2.putText(travel_map, org=(10, 25), text=f'generation: {generation}', fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=0, thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(travel_map, org=(10, 45), text=f'distance: {distance}', fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=BLUE, thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(travel_map, org=(10, 65), text=f'best route: {best_genome}', fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=0, thickness=1, lineType=cv2.LINE_AA)

            cv2.imshow(title, travel_map)
            if cv2.waitKey(1) == ord('q'):
                break
            
            travel_map = cv2.imread(self.map_path)

            generation += 1
        
        cv2.waitKey(0)



if __name__ == "__main__":
    
    random.seed(777)

    CITIES_COUNT = 20
    POPULATION_SIZE = 100
    GENERATION_LIMIT = 2000
    MUTATION_RATE = 65
    WEAKNESS_THRESHOLD = 1400
    
    # CITIES_COUNT = 20
    # POPULATION_SIZE = 100
    # GENERATION_LIMIT = 2000
    # MUTATION_RATE = 65
    # WEAKNESS_THRESHOLD = 1500

    map_path = 'america.jpg'


    city_coordinates = []
    for i in range(CITIES_COUNT):
        x = random.randint(100, 500)
        y = random.randint(200, 400)
        city_coordinates.append([x, y])

    ga = GeneticAlgorithm(weakness_threshold=WEAKNESS_THRESHOLD,
                          generation_limit=GENERATION_LIMIT,
                          population_size=POPULATION_SIZE,
                          chromosome_size=CITIES_COUNT,
                          mutation_rate=MUTATION_RATE,
                          cities_count=CITIES_COUNT,
                          city_coordinates=city_coordinates,
                          map_path=map_path)

    ga.main()