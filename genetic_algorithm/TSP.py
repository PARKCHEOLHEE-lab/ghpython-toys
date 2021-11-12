import cv2
import math
import random
import numpy as np

class Genome:
    chromosome = []
    fitness = 0

    def __getitem__(self, index):
        return self.chromosome[index]

    def __len__(self):
        return len(self.chromosome)


    class Chromosome:
        def __init__(self, city_coordinates):
            self.city_coordinates = city_coordinates
            self.population = []

        def configurate_chromosome(self, chromosome_size, travel_size):
            for _ in range(chromosome_size):
                genome = Genome()
                genome.chromosome = random.sample(range(1, travel_size), travel_size-1)
                genome.chromosome.insert(0, 0)
                genome.chromosome.append(0)
                genome.fitness = self.evaluate_chromosome(genome.chromosome)
                self.population.append(genome)
            return self.population

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
    def __init__(self, city_coordinates, generation_limit):
        self.city_coordinates = city_coordinates
        self.generation_limit = generation_limit

    def travel_size(self):
        return len(self.city_coordinates)



if __name__ == "__main__":
    CITIES_COUNT = 15
    random.seed(777)

    city_coordinates = []
    # map = cv2.imread('america.jpg')
    for i in range(CITIES_COUNT):
        x = random.randint(100, 500)
        y = random.randint(200, 400)

        city_coordinates.append([x,y])
    
    genome_object = Genome()
    chromosome_object = genome_object.Chromosome(city_coordinates)
    genome = chromosome_object.configurate_chromosome(chromosome_size=10, travel_size=CITIES_COUNT)


    for chromosome in genome:
        evaluate_chromosome = chromosome_object.evaluate_chromosome(chromosome)
        print(evaluate_chromosome)