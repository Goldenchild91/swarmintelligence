import random

#Swarm Intelligence
#Ella Mohanram
#April 22, 2023

#uses ant colony optimization to solve the CVRP
class CVRP_ACO:
    #depot has not been visited yet
    not_visited = 0

    #depot has already been visited
    visited = 1

    #probability that truck chooses next depot randomly
    random_depot_factor = 0.1

    #maximum number of random tries before a truck just comes home
    max_tries = 5

    #alpha value for the probabilistic selection algorithm
    alpha = 1

    #beta value for the probabilistic selection algorithm
    beta = 2

    #number of trucks to use as ants as a %age of the number of depots
    number_of_trucks_factor = 0.5

    #number of times to repeat algorithm
    total_iterations = 1000

    #%age of pheromones to preserve after each iteration
    evaporation_rate = 0.4

    #max amount the truck can carry at any one time
    max_load = 15

    #distances between each depot (symmetrical)
    distance_matrix = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0]
    ]

    #loads present at each depot
    loads = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]

    #initialize pheromone matrix to 1
    #returns: initalized pheromone trails
    def setup_pheromones(self):
        pheromone_trails = [[1]*len(CVRP_ACO.loads) for i in range(len(CVRP_ACO.loads))]
        return pheromone_trails

    #create initial population of trucks
    #returns: initialized population of trucks
    def setup_trucks(self):
        my_trucks = []
        num_trucks = round(len(CVRP_ACO.loads) * CVRP_ACO.number_of_trucks_factor)
        for i in range(num_trucks):
            my_trucks.append(Truck())

        return my_trucks

    #updates pheromone matrix to include evaporation and deposit
    def update_pheromones(self, pheromone_trails, my_trucks):
        pheromone_trails = [[pheromone * CVRP_ACO.evaporation_rate for pheromone in pheromone_trail] for pheromone_trail in pheromone_trails]

        for truck in my_trucks:
            deposit_value = (1/truck.get_distance_traveled()) * 1000
            for i in range(len(truck.route) - 1):
                depot_one = truck.route[i]
                depot_two = truck.route[i + 1]
                pheromone_trails[depot_one][depot_two] += deposit_value

    #tries to move each truck to a new depot
    def move_trucks(self, pheromone_trails, my_trucks):
        for truck in my_trucks:
            truck.visit_depot(pheromone_trails)

    #check if all trucks are done picking up loads
    #returns: true if each truck is done route, else false
    def done_routes(self, my_trucks):
        for truck in my_trucks:
            if not truck.done_route():
                return False

        return True

    #finds best truck in myTrucks (the shortest route)
    #returns: Truck in myTrucks with minimum return value from get_distance_traveled()
    def get_best(self, my_trucks):
        minimum_route = 100000
        best_truck = None

        for truck in my_trucks:
            if truck.get_distance_traveled() < minimum_route:
                minimum_route = truck.get_distance_traveled()
                best_truck = truck

        return best_truck

    #run the ACO algorithm
    def solve(self):
        pheromone_trails = CVRP_ACO.setup_pheromones(self)
        best_truck = None

        for i in range(0, CVRP_ACO.total_iterations):
            truck_colony = CVRP_ACO.setup_trucks(self)
            while not CVRP_ACO.done_routes(self, truck_colony):
                CVRP_ACO.move_trucks(self, pheromone_trails, truck_colony)
            CVRP_ACO.update_pheromones(self, pheromone_trails, truck_colony)
            best_truck = CVRP_ACO.get_best(self, truck_colony)

        best_route = best_truck.route
        best_distance = best_truck.get_distance_traveled()

        if best_route[-1] != 0:
            best_route.append(0)
            best_distance += CVRP_ACO.distance_matrix[best_route[-1]][0]

        print("Best Route: " + str(best_route))
        print("Best Distance: " + str(best_distance))
        print("Pheromone Trails: " + str(pheromone_trails))


# models the truck (ant)
class Truck(CVRP_ACO):
    # are route, visited depots, load class variables or what?
    # route traveled thus far
    route = [0]

    # true for each depot if visited, else false
    visited_depots = [0] * len(CVRP_ACO.loads)

    # load currently being carried
    load = 0

    # calculates distance traveled
    # return: sum of distances between each pair of elements in route
    def get_distance_traveled(self):
        distance = 0

        for i in range((len(self.route) - 1)):
            distance += CVRP_ACO.distance_matrix[self.route[i]][self.route[i + 1]]

        return distance

    # checks if all depots are visited
    # returns: true if each element in visited_depots == VISITED, else false
    def done_route(self):
        for depot in self.visited_depots:
            if depot == CVRP_ACO.not_visited:
                return False
        return True

    # tries to visit a specific depot
    # param: num: the number of the depot to visit
    # return: true if it is possible to visit this depot, else false
    def add_depot(self, num):
        new_load = CVRP_ACO.loads[num]

        if num == self.route[len(self.route) - 1]:
            return False
        elif num == 0:
            self.route.append(0)
            self.visited_depots[0] = 1
            self.load = 0
            return True
        else:
            if self.load + new_load > CVRP_ACO.max_load:
                return False
            else:
                self.load += new_load
                self.visited_depots[num] = CVRP_ACO.visited
                self.route.append(num)
                return True

    # tells truck to visit a depot (either randomly or probabilistically)
    def visit_depot(self, pheromone_trails):
        if not self.done_route():
            if random.random() < CVRP_ACO.random_depot_factor:
                self.visit_random_depot()
            else:
                self.visit_probabilistic_depot(pheromone_trails)

    # tells truck to visit a depot randomly
    def visit_random_depot(self):
        done = False
        num_tries = 0

        while not done and num_tries < CVRP_ACO.max_tries:
            num_tries += 1
            depot = int(random.random() * len(CVRP_ACO.loads))
            done = self.add_depot(depot)

        if not done:
            self.add_depot(0)

    # tells truck to visit a depot probabilistically
    def visit_probabilistic_depot(self, pheromone_trails):
        depot = self.roulette_wheel_selection(pheromone_trails)
        self.add_depot(depot)

    # selects a depot probabilistically using roulette wheel
    # returns: number of depot to visit
    def roulette_wheel_selection(self, pheromone_trails):
        depot_probs = self.get_depot_probs(pheromone_trails)

        if len(depot_probs) == 0:
            return 0

        random_probability = random.random()
        i = 0
        while random_probability > list(depot_probs.values())[i]:
            random_probability -= list(depot_probs.values())[i]
            i += 1

        return list(depot_probs.keys())[i]

    # generates list of probabilities for roulette wheel
    # returns: list of pairs (scaled to 1.0)
    def get_depot_probs(self, pheromone_trails):
        current_attraction = self.visited_depots[-1]
        all_attractions = range(0, len(CVRP_ACO.loads))
        possible_attractions = []

        for all_attraction in all_attractions:
            if (self.visited_depots[all_attraction] == CVRP_ACO.not_visited) and (self.load + CVRP_ACO.loads[all_attraction] <= CVRP_ACO.max_load):
                possible_attractions.append(all_attraction)
        if len(possible_attractions) == 0:
            return {0:1}

        depot_probs = {}
        total_probabilities = 0

        for attraction in possible_attractions:
            if current_attraction != attraction:
                pheromones_on_path = (pheromone_trails[current_attraction][attraction]) ** CVRP_ACO.alpha
                heuristic_for_path = (1/ (CVRP_ACO.distance_matrix[current_attraction][attraction])) ** CVRP_ACO.beta
                probability = pheromones_on_path * heuristic_for_path
                total_probabilities += probability
                depot_probs[attraction] = probability

        for key, value in depot_probs.items():
            value /= total_probabilities
            depot_probs[key] = value

        return depot_probs


swarm = CVRP_ACO()
swarm.solve()