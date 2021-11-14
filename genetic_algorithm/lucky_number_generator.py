import random
import copy
import numpy as np

class GeneticAlgorithm:
    def __init__(self, gene_count, chromosome_count, mutation_rate, dominant_factor, generation_limit=1000):
        self.GENE_COUNT = gene_count
        self.GENOME_COUNT = chromosome_count
        self.MUTATION_RATE = mutation_rate
        self.GENERATION_LIMIT = generation_limit
        self.DOMINANT_FACTOR = dominant_factor

    def generate_genome(self):
        genome = []
        for _ in range(self.GENOME_COUNT):
            chromosome = []
            for _ in range(self.GENE_COUNT):
                gene = random.randint(0, 9)
                chromosome.append(gene)
            genome.append(chromosome)
        return genome    

    def manipulation_chromosome(self, parent_chromosome, child_chromosome, best_parents_indices):
        for i in range(self.GENOME_COUNT):
            for j in range(self.GENE_COUNT):
                if random.random() < self.MUTATION_RATE:
                    mutated_gene = random.randint(0, 9)
                    child_chromosome[i][j] = mutated_gene
                else:
                    idx = random.randint(0, 1)
                    selected_parent = best_parents_indices[idx]
                    crossoverd_gene = parent_chromosome[selected_parent][j]
                    child_chromosome[i][j] = crossoverd_gene

    def evaluate_chromosome(self, genome):
        evaluation_values = [0] * len(genome)
        for i, chromosome in enumerate(genome):
            score = 0
            for gene in chromosome:
                score += abs(gene - self.DOMINANT_FACTOR)
            evaluation_values[i] = score
        return evaluation_values

    def copy_chromosome(self, chromosome):
        return copy.deepcopy(chromosome)

    def evaluate_dominant(self, evaluation_values):
        if evaluation_values.count(0) == CHROMOSOME_COUNT:
            return True

        # for i in range(GENOME_COUNT):
        #     if evaluation_values[i] == 0:
        #         return True

    def best_parents(self, evaluation_values):
        PARENTS_COUNT = 2
        best_parents_indices = [0] * PARENTS_COUNT
        for i in range(PARENTS_COUNT):
            best_parent_index = np.argsort(evaluation_values)[i]
            best_parents_indices[i] = best_parent_index
        return best_parents_indices

    def main(self):
        generation = 1
        while generation < self.GENERATION_LIMIT:
            if generation == 1:
                parent_genome = self.generate_genome()
                child_genome = self.copy_chromosome(parent_genome)

            evaluation_values = self.evaluate_chromosome(parent_genome)
            best_parents_indices = self.best_parents(evaluation_values)

            self.manipulation_chromosome(parent_genome, child_genome, best_parents_indices)
            parent_genome = self.copy_chromosome(child_genome)

            if self.evaluate_dominant(evaluation_values):
                break

            print("\n")
            print("generation:", generation)
            print("chromosome:", parent_genome)
            print("evaluation value:", evaluation_values)
            print("selected parents:", best_parents_indices)

            generation += 1



if __name__ == "__main__":
    random.seed(777)

    GENE_COUNT = 7
    CHROMOSOME_COUNT = 7
    MUTATION_RATE = 0.07
    DOMINANT_FACTOR = 7
    GENERATION_LIMIT = 777

    ga = GeneticAlgorithm(gene_count=GENE_COUNT,
                          chromosome_count=CHROMOSOME_COUNT,
                          mutation_rate=MUTATION_RATE,
                          dominant_factor=DOMINANT_FACTOR,
                          generation_limit=GENERATION_LIMIT)

    ga.main()
