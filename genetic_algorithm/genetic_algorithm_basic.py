import random
import copy
import numpy as np

def evaluation(chromos):
    evalution_value = [0 for _ in range(len(chromos))]
    
    dominant_factor = 1

    for i in range(len(chromos)):
        m_sum = 0
        for j in range(len(chromos[0])):
            if chromos[i][j] > dominant_factor:
                m_sum += chromos[i][j] - dominant_factor
            else:
                m_sum += dominant_factor - chromos[i][j]
        evalution_value[i] = m_sum
    
    return evalution_value



if __name__ == "__main__":
    random.seed(0)
    
    gene_count = 10
    chromos_count = 5
    
    mutation = 0.01
    generation = 0

    done = False
    
    # First Generation
    chromos = [[random.randrange(0,10) for _ in range(gene_count)] for _ in range(chromos_count)]
    new_chromos = copy.deepcopy(chromos)
    generation = generation+1

    while generation < 1000:
        
        evaluation_value = evaluation(chromos)

        best_parents_indices = []
        for i in range(2):
            best_parent_index = np.argsort(evaluation_value)[i]
            best_parents_indices.append(best_parent_index)

        for i in range(chromos_count):
            for j in range(gene_count):
                if random.random() < mutation:
                    new_chromos[i][j] = random.randrange(0, 10)
                else:
                    new_chromos[i][j] = chromos[best_parents_indices[random.randrange(0, 2)]][j]

        for i in range(chromos_count):
            if evaluation_value[i] == 0:
                done = True
                break

        if done == True:
            print("done!!!")
            break

        chromos = copy.deepcopy(new_chromos)    
        
        print("\n")
        print("generation:", generation)
        print("chromos:", chromos)
        print("evaluation value:", evaluation_value)
        print("selected parents:", best_parents_indices)

        generation += 1 