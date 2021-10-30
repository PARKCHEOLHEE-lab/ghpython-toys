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


class Tour:
    def __init__(self, manager, tour=None):
        self.manager = manager
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for i in range(0, self.manager.len_destination()):
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
            for i in range(0, self.tour_size()):
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
    


if __name__ == "__main__":
    random.seed(999)
    
    cities_circles = []
    cities = []
    for x,y,z in coordinates:
        cities_circles.append(rs.AddCircle([x,y,z], 2))
        cities.append(City(x,y))
    
    manager = Manager()
    tour = Tour(manager, cities)
    
    test_1 = tour.get_distance()
    test_2 = 0
    for i in range(len(tour)):
        if i == len(tour)-1:
            test_2 += tour[i].distance_to(tour[0])
        else:
            test_2 += tour[i].distance_to(tour[i+1])
            
    print(test_1)
    print(test_2)