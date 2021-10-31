import math
import random
import Rhino.Geometry as rg
import Rhino.RhinoDoc as rc
import rhinoscriptsyntax as rs
import ghpythonlib.components as gh


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
        
    def distance_to(self, city):
        x_distance = abs(self.get_x() - city.get_x())
        y_distance = abs(self.get_y() - city.get_y())
        distance = math.sqrt(x_distance**2 + y_distance**2)
        return distance
        
    def __repr__(self):
        return str(self.get_x()) +", " + str(self.get_y())
        

class Manager:
    destination_cities = []
    
    def add_city(self, city):
        self.destination_cities.append(city)
        
    def get_city(self, index):
        return self.destination_cities[index]
        
    def len_destination(self):
        return len(self.destination_cities)
        
#    def __getitem__(self, index):
#        return self.destination_cities[index]


class Tour:
    def __init__(self, manager, tour=None):
        self.manager = manager
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for i in range(self.manager.len_destination()):
                self.tour.append(None)
                
    def __len__(self):
        return len(self.tour)
        
    def __getitem__(self, index):
        return self.tour[index]
        
    def __setitem__(self, index, value):
        self.tour[index] = value
        
    def __repr__(self):
        gene_string = 'Start -> '
        for i in range(0, self.tour_size()):
            gene_string += str(self.get_city(i)) + ' -> '
        gene_string += 'End'
        return gene_string
        
    def get_city(self, index):
        return self.tour[index]
        
    def set_city(self, index, city):
        self.tour[index] = city
        self.fitness = 0.0
        self.distance = 0
        
    def get_distance(self):
        if self.distance == 0:
            tour_distance = 0
            for i in range(self.tour_size()):
                from_city = self.get_city(i)

                if i+1 < self.tour_size():
                    destination_city = self.get_city(i+1)
                
                else:
                    destination_city = self.get_city(0)
                
                tour_distance += from_city.distance_to(destination_city)
            self.distance = tour_distance
        return self.distance
        
    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.get_distance())
        return self.fitness
        
    def tour_size(self):
        return len(self.tour)
        
    def contains_city(self, city):
        return city in self.tour
        
    def generate_individual(self):
        for i in range(0, self.manager.len_destination()):
            self.set_city(i, self.manager.get_city(i))
        random.shuffle(self.tour)


class Population:
    def __init__(self, manager, population_size, initialize):
        self.tours = [None] * population_size
        
        if initialize == True:
            for i in range(population_size):
                new_tour = Tour(manager)
                new_tour.generate_individual()
                self.save_tour(i, new_tour)
            
    def __setitem__(self, index, value):
        self.tours[index] = value
        
    def __getitem__(self, index):
        return self.tours[index]
        
    def save_tour(self, index, tour):
        self.tours[index] = tour
        
    def get_tour(self, index):
        return self.tours[index]
        
    def get_fittest(self):
        fittest = self.tours[0]
        for i in range(self.population_size()):
            if fittest.get_fitness() <= self.get_tour(i).get_fitness():
                fittest = self.get_tour(i)
        return fittest
        
    def population_size(self):
        return len(self.tours)


class GeneticAlgorithm:
    def __init__(self, manager, mutation_rate=0.05, tournament_size=5, elitism=True):
        self.manager = manager
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism
        
    def evolve_population(self, pop):
        new_population = Population(self.manager, pop.population_size(), False)
        elitism_offset = 0
        if self.elitism:
            new_population.save_tour(0, pop.get_fittest())
            elitism_offset = 1
            
        for i in range(elitism_offset, new_population.population_size()):
            parent_1 = self.tournament_selection(pop)
            parent_2 = self.tournament_selection(pop)
            child = self.crossover(parent_1, parent_2)
            new_population.save_tour(i, child)
            
        for i in range(elitism_offset, new_population.population_size()):
            self.mutate(new_population.get_tour(i))
            
        return new_population
        
    def crossover(self, parent_1, parent_2):
        child = Tour(self.manager)
        
        start_pos = int(random.random() * parent_1.tour_size())
        end_pos = int(random.random() * parent_1.tour_size())

        
        for i in range(0, child.tour_size()):
            if start_pos < end_pos and i > start_pos and i < end_pos:
                child.set_city(i, parent_1.get_city(i))
            elif start_pos > end_pos:
                if not (i < start_pos and i > end_pos):
                    child.set_city(i, parent_1.get_city(i))
        
        for i in range(0, parent_2.tour_size()):
            if not child.contains_city(parent_2.get_city(i)):
                for ii in range(0, child.tour_size()):
                    if child.get_city(ii) == None:
                        child.set_city(ii, parent_2.get_city(i))
                        break

        return child
   
    def mutate(self, tour):
        for tour_pos_1 in range(0, tour.tour_size()):
            if random.random() < self.mutation_rate:
                tour_pos_2 = int(tour.tour_size() * random.random())
                
                city1 = tour.get_city(tour_pos_1)
                city2 = tour.get_city(tour_pos_2)
                
                tour.set_city(tour_pos_2, city1)
                tour.set_city(tour_pos_1, city2)

    def tournament_selection(self, pop):
        tournament = Population(self.manager, self.tournament_size, False)
        for i in range(0, self.tournament_size):
            random_id = int(random.random() * pop.population_size())
            tournament.save_tour(i, pop.get_tour(random_id))
        fittest = tournament.get_fittest()
        return fittest



if __name__ == "__main__":
    population_size = 50
    generations = 100
    
    random.seed(100)
    
    cities_circles = []
    cities = []
    manager = Manager()
    for x,y,z in coordinates:
        cities_circles.append(rs.AddCircle([x,y,z], 2))
        city = City(x,y)
        
        cities.append(city)
        manager.add_city(city)
        
#    for i in range(n_cities):
#        x = random.randint(200, 800)
#        y = random.randint(200, 800)
#        cities_circles.append(rs.AddCircle([x,y,0], 2))
#        
#        city = City(x,y)
#        manager.add_city(city)
        
    pop = Population(manager, population_size, True)
    print("Initial Distance:" + str(pop.get_fittest().get_distance()))
    
    cities_connections = []
    ga = GeneticAlgorithm(manager)
    
    for i in range(generations):
        pop = ga.evolve_population(pop)
        fittest = pop.get_fittest()
        pts = []

        for j in range(len(cities)):
            pts.append(rs.AddPoint(fittest[j].get_x(), fittest[j].get_y(), 0))
            
        connection = rs.AddPolyline(pts)
        print(rs.CurveLength(connection))
        cities_connections.append(connection)
    
    cities_connections_length = [rs.CurveLength(connection) for connection in cities_connections]
    min_index = cities_connections_length.index(min(cities_connections_length))
#    cities_connections = cities_connections[min_index]
    cities_connections = cities_connections[-1]
    print(min(cities_connections_length))