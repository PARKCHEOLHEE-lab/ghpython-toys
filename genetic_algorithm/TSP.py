import cv2
import math
import copy
import random
import numpy as np
from numpy.lib.function_base import diff


class Genome:
    chromosome = []
    fitness = 0

    def __getitem__(self, index):
        return self.chromosome[index]

    def __len__(self):
        return len(self.chromosome)

    def __repr__(self):
        return str(self.chromosome)

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
    
    def configurate_chromosome(self, genome_size, chromosome_size):
        for _ in range(genome_size):
            genome = Genome()
            chromosome = random.sample(range(1, chromosome_size), chromosome_size-1)
            chromosome.insert(0, 0)
            chromosome.append(0)
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
    def __init__(self, generation_limit):
        self.generation_limit = generation_limit

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
        count = 10
        parent_1 = self.tournament_selection(genome, count)
        parent_2 = self.tournament_selection(genome, count)

        while parent_1 == parent_2:
            parent_2 = self.tournament_selection(genome, count)

        parents = [parent_1, parent_2]
        return parents

    def crossover_genome(self, parents):
        return

    def mutation_genome(self):
        return



if __name__ == "__main__":
    
    random.seed(777)

    CITIES_COUNT = 15
    GENOME_SIZE = 5
    GENERATION_LIMIT = 1000

    city_coordinates = []
    for i in range(CITIES_COUNT):
        x = random.randint(100, 500)
        y = random.randint(200, 400)
        city_coordinates.append([x,y])
    
    genome_object = Genome()
    chromosome_object = Chromosome(city_coordinates)
    genome = chromosome_object.configurate_chromosome(genome_size=GENOME_SIZE, chromosome_size=CITIES_COUNT)
    
    ga = GeneticAlgorithm(generation_limit=GENERATION_LIMIT)

    # parent_1, parent_2 = ga.reproduction_genome(genome)
    # print(parent_1)
    # print(parent_2)
    
    parent_1 = [0, 7, 14, 8, 6, 10, 9, 11, 12, 5, 13, 1, 3, 4, 2, 0]
    parent_2 = [0, 5, 2, 11, 12, 4, 14, 3, 7, 10, 9, 1, 13, 6, 8, 0]
    offspring = [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]

    start = len(parent_1) // 3
    end = len(parent_1) - 4

    start = random.randrange(start, end)
    
    order_genes = parent_1[start:end]
    offspring[start:end] = order_genes
    
    difference_genes = copy.deepcopy(parent_2)
    for gene in order_genes:
        i = difference_genes.index(gene)
        difference_genes[i] = -1
    
    while -1 in difference_genes:
        difference_genes.remove(-1)

    print(difference_genes)

    # while -1 in offspring:
        
        # break