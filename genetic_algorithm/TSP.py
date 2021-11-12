import cv2
import math
import random
import numpy as np
from numpy.lib.function_base import select


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
    def __init__(self, genome, generation_limit):
        self.genome = genome
        self.generation_limit = generation_limit

    def get_genome(self):
        return self.genome

    def evaluate_fittest(self):
        fitnesses = []
        for chromosome in self.get_genome():
            fitness = chromosome.get_fitness()
            fitnesses.append(fitness)

        i = fitnesses.index(min(fitnesses))
        fittest = self.genome[i]
        return fittest

    def tournament_selection(self):
        return


if __name__ == "__main__":
    
    random.seed(777)

    CITIES_COUNT = 15
    GENOME_SIZE = 2
    GENERATION_LIMIT = 1000

    city_coordinates = []
    for i in range(CITIES_COUNT):
        x = random.randint(100, 500)
        y = random.randint(200, 400)
        city_coordinates.append([x,y])
    
    genome_object = Genome()
    chromosome_object = Chromosome(city_coordinates)
    genome = chromosome_object.configurate_chromosome(genome_size=GENOME_SIZE, chromosome_size=CITIES_COUNT)

    ga = GeneticAlgorithm(genome=genome, generation_limit=GENERATION_LIMIT)