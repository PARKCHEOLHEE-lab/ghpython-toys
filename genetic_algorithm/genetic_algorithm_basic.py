import random
import copy
import numpy as np

def evaluation(chromosome):
    evalution_value = [0 for _ in range(len(chromosome))]
    
    dominant_factor = 1

    for i in range(len(chromosome)):
        score = 0

        for j in range(len(chromosome[0])):
            if chromosome[i][j] > dominant_factor:
                score += chromosome[i][j] - dominant_factor
            else:
                score += dominant_factor - chromosome[i][j]

        evalution_value[i] = score
    
    return evalution_value


if __name__ == "__main__":
    random.seed(777)
    
    GENE_COUNT = 10
    GENOME_COUNT = 5
    MUTATION_RATE = 0.01
    GENERATION_LIMIT = 1000
    
    generation = 1
    done = False

    while generation < GENERATION_LIMIT:
        if generation == 1:
            parent_chromosome = [[random.randint(0, 9) for _ in range(GENE_COUNT)] for _ in range(GENOME_COUNT)]
            child_chromosome = copy.deepcopy(parent_chromosome)
        
        evaluation_value = evaluation(parent_chromosome)

        best_parents_indices = []
        for i in range(2):
            best_parent_index = np.argsort(evaluation_value)[i]
            best_parents_indices.append(best_parent_index)

        for i in range(GENOME_COUNT):
            for j in range(GENE_COUNT):
                if random.random() < MUTATION_RATE:
                    mutation = random.randint(0, 9)
                    child_chromosome[i][j] = mutation
                else:
                    selected_parent = best_parents_indices[random.randint(0, 1)]
                    crossover = parent_chromosome[selected_parent][j]
                    child_chromosome[i][j] = crossover

        parent_chromosome = copy.deepcopy(child_chromosome)

        for i in range(GENOME_COUNT):
            if evaluation_value[i] == 0:
                done = True
                break

        if done == True:
            print()
            print("###### done ######")
            print("dominant genome:")
            break

        
        print("\n")
        print("generation:", generation)
        print("chromosome:", parent_chromosome)
        print("evaluation value:", evaluation_value)
        print("selected parents:", best_parents_indices)

        generation += 1 