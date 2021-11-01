import random
import copy
import numpy as np

def evaluation(chromos):
    evalution_value = [0 for _ in range(len(chromos))]
    
    dominant_factor = 1

    for i in range(len(chromos)):
        score = 0

        for j in range(len(chromos[0])):
            if chromos[i][j] > dominant_factor:
                score += chromos[i][j] - dominant_factor
            else:
                score += dominant_factor - chromos[i][j]

        evalution_value[i] = score
    
    return evalution_value


if __name__ == "__main__":
    random.seed(777)
    
    GENE_COUNT = 10
    GENOME_COUNT = 5
    MUTATION_RATE = 0.01
    
    chromosome = [[random.randint(0, 9) for _ in range(GENE_COUNT)] for _ in range(GENOME_COUNT)]
    copied_chromosome = copy.deepcopy(chromosome)
    generation = 1
    done = False

    while generation < 1000:
        
        evaluation_value = evaluation(chromosome)

        best_parents_indices = []
        for i in range(2):
            best_parent_index = np.argsort(evaluation_value)[i]
            best_parents_indices.append(best_parent_index)

        for i in range(GENOME_COUNT):
            for j in range(GENE_COUNT):
                if random.random() < MUTATION_RATE:
                    mutation = random.randint(0, 9)
                    copied_chromosome[i][j] = mutation
                else:
                    selected_parent = best_parents_indices[random.randint(0, 1)]
                    crossover = chromosome[selected_parent][j]
                    copied_chromosome[i][j] = crossover

        chromosome = copy.deepcopy(copied_chromosome)

        for i in range(GENOME_COUNT):
            if evaluation_value[i] == 0:
                done = True
                break

        if done == True:
            print("done!!!")
            break

        
        print("\n")
        print("generation:", generation)
        print("chromos:", chromosome)
        print("evaluation value:", evaluation_value)
        print("selected parents:", best_parents_indices)

        generation += 1 