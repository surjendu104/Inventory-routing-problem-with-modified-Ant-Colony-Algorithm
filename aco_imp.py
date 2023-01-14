import sys
import random
import math
import copy

# sys.stdin=open('input.txt',"r")
sys.stdout = open("output.txt", "w")

"""Some predeclaired Constants"""
vehicle_capacity = 200
customer_number = 50
no_of_vehicles_needed = 0  # Initially
period = 5
tau_0 = 0.0
Q = 1.0
m = 25
F = 5
V = 10
rho = 0.1
alpha, beta = 1, 5

# Depo location is (0,0) and inventory level 5000(say)
customer_list = [{"x": 0, "y": 0, "dt": [], "I": 5000}]
gen_number = 200


"""Random Input generation"""

for i in range(customer_number):
    customer = {"x": 0, "y": 0, "h": 0, "dt": [], "I": 0}

    customer["x"] = random.randrange(-100, 100)
    customer["y"] = random.randrange(-100, 100)
    customer["h"] = random.randrange(10)
    # Generating random demand for each customer for each period
    for j in range(period):
        customer["dt"].append(random.randrange(100))
    customer["I"] = random.randrange(100)

    customer_list.append(customer)

"""Printing the customer list"""
print("Customer List")
for i in range(customer_number + 1):
    sys.stdout.write("\n%d: " % i)
    print(customer_list[i])

"""Function to calculate distance from one node to another"""


def distance_between_two_node(x1, x2, y1, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


"""Calculating Distance from one Customer TO all Other Customer"""
distance_matrix = []
for i in range(customer_number + 1):
    distance_array = []
    for j in range(customer_number + 1):
        distance_array.append(
            int(
                distance_between_two_node(
                    customer_list[i]["x"],
                    customer_list[j]["x"],
                    customer_list[i]["y"],
                    customer_list[j]["y"],
                )
            )
        )
    distance_matrix.append(distance_array)

distance = copy.deepcopy(distance_matrix)

"""Printing distance Matrix"""
print("\nDisatance Matrix")
for i in range(customer_number + 1):
    sys.stdout.write("\n%d: " % i)
    print(distance_matrix[i])

"""Extarct/Filter minimum distance of each cuatomer"""


def mini(dist_array):
    minimum_dist = sys.maxsize
    for i in range(1, len(dist_array)):
        if dist_array[i] == 0:
            continue
        else:
            minimum_dist = min(minimum_dist, dist_array[i])
    return [minimum_dist, dist_array.index(minimum_dist)]


# Printing some result generated so far
min_dist = []
"""This is later going to be the total distance we need to travel if we don't have any Time Period and Demand Constraint"""
ideally_total_distance = 0
ideally_initial_path = []
k = 0

"""Getting meinimum distant node for each cuatomer and print with index"""
print("\nMinimum distant Node for each customer : ")
for i in range(customer_number):
    sys.stdout.write("\n%d: " % k)
    ideally_initial_path.append(k)
    # return a array with two eleemnt-->min_diatance and index as path
    min_dist = mini(distance[k])
    k = min_dist[1]
    ideally_total_distance += min_dist[0]

    print(min_dist[0], min_dist[1])

    for j in range(customer_number + 1):
        distance[j][min_dist[1]] = 0

"""Lastly we have to reach to depo so we append this last node index and distance between (0,0) to the node"""
ideally_initial_path.append(k)
ideally_total_distance += int(
    distance_between_two_node(0, customer_list[k]["x"], 0, customer_list[k]["y"])
)

"""Pheromone density(initial)"""
tau_0 = 1.0 / ideally_total_distance

print("General Initial Path : {}".format(ideally_initial_path))
print("General Total Distance : {}".format(ideally_total_distance))
print("Tau_INITIAL : {}".format(tau_0))


"""Generate Pheromone Matrix"""
pheromone_matrix = []
for i in range(customer_number + 1):
    pheromone = []
    for j in range(customer_number + 1):
        if distance_matrix[i][j] == 0:
            pheromone.append(0.0)
        else:
            pheromone.append(tau_0)
    pheromone_matrix.append(pheromone)

"""Some printing"""
print("\nDisatance Matrix")
for i in range(customer_number + 1):
    sys.stdout.write("\n%d: " % i)
    print(distance_matrix[i])
print("\nPheromone Matrix")
for i in range(customer_number + 1):
    sys.stdout.write("\n%d: " % i)
    print(pheromone_matrix[i])


"""Probability function to choose the best route"""
"""State Transition Probability"""


def probability(route):
    r = []
    customer_instance = []
    for i in range(1, customer_number + 1):
        r.append(i)

    for i in r:
        if i not in route:
            customer_instance.append(i)

    sigma = 0
    rev_route = route[-1]

    """ When q<q0 then according to Biased Roulette Method with state transition probability is
        max(sigma) where sigma=((tau_ij)^alpha)/((c_ij)^beta)
    """
    for i in customer_instance:
        if rev_route != i:
            try:

                sigma += (pheromone_matrix[rev_route][i] ** alpha) * (
                    (1.0 / distance_matrix[rev_route][i]) ** beta
                )
            except ZeroDivisionError:  # Ignore if the deominator is 0
                continue
    p_max = 0.0
    for i in customer_instance:
        p_ij = 0.0

        # If the path is not visited then
        if rev_route != i:
            try:
                p_ij = (pheromone_matrix[rev_route][i] ** alpha) * (
                    (1.0 / distance_matrix[rev_route][i]) ** beta
                )
            except ZeroDivisionError:  # Ignore if the deominator is 0
                continue
            if p_ij > p_max:
                p_max = p_ij
                try:
                    b = i
                except:
                    print("Can be taken")
    return [p_max, b]


"""Claculate the path distance for the given route"""


def path_distance(route, glob=False):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance_matrix[route[i]][route[i + 1]]
    return dist


"""Function to Update the pheromone after each iteration"""


def update_pheromone(route, glob=False):
    print(route)
    dist = path_distance(route)

    """For loop only for if we want ot update it locally"""
    for i in range(len(route) - 1):
        pheromone_local[route[i]][route[i + 1]] += Q / dist

    """This one for global update"""
    if glob:
        for i in range(customer_number):
            for j in range(customer_number):
                pheromone_matrix[i][j] += (
                    rho * pheromone_matrix[i][j] + pheromone_local[i][j]
                )
    return dist


"""Run the process for certain number of generation and filter best route and best distance in each iteartion"""

global best_route, best_distance
best_route = []
best_distance = ideally_total_distance
track_min_distance = []  # For Ploting the graph

for n in range(gen_number):
    print("\nIteration No: {}".format(n))

    """Start with random root"""
    ant_route = []
    for i in range(m):
        ant = []
        ant.append(random.randint(1, customer_number))
        ant_route.append(ant)

    """Calculate the Probabilty for each route and extract the max"""
    for i in range(m):
        a = []
        for j in range(customer_number - 1):
            p1 = probability(ant_route[i])
            # Get the index of maximum probability route
            ant_route[i].append(p1[1])

    """Get the minimum path distane for maximum probabilty route"""
    di = []
    for i in range(m):
        di.append(path_distance(ant_route[i]))
    # sys.stdout.write("Minimum Distance: ")
    print("Minimum Distance : {}".format(min(di)))
    track_min_distance.append(min(di))
    ant = di.index(min(di))

    """Copy the Pheromone Matrix to manipulate"""
    pheromone_local = copy.deepcopy(pheromone_matrix)

    """Finally Get the best route and best distance"""
    if update_pheromone(ant_route[ant], True) < best_distance:
        best_distance = update_pheromone(ant_route[ant], True)
        best_route = ant_route[i]
    print(update_pheromone(ant_route[ant], True))


print("********\nBest Distance : {}".format(best_distance))
print("Best Routes")
print(best_route)

demand = 0
"""Total demand"""
for i in range(1, len(customer_list)):
    print(customer_list[i]["dt"])
    for j in range(period):
        demand += customer_list[i]["dt"][j]


no_of_vehicles_needed = demand // vehicle_capacity + (
    1 if demand % vehicle_capacity == 1 else 0
)


i, r = 0, 0
vehicle_route, route, deliveryT, vrT = [], [], [], []

for i in range(period):
    delivery = []
    vehicle_route.append(route)
    route, vr = [], []
    r = 0

    for j in range(customer_number):
        delivery.append(customer_list[best_route[j]]["dt"][i])
        r += customer_list[best_route[j]]["dt"][i]

        route.append(best_route[j])
        vr.append(best_route[j])

        if r > vehicle_capacity:
            vehicle_route.append(route)
            route = []
            r = 0
    if [] in vehicle_route:
        vehicle_route.remove([])
    deliveryT.append(delivery)
    vrT.append(vr)

"""************************************************************************"""
print("\nTotal Demand : {}".format(demand))
print("No of vehilcle Neede : {}".format(no_of_vehicles_needed))
print("Veichle Route : ", end=" ")
print(vehicle_route)

print("Length of Veichle Route : ", end=" ")
print(len(vehicle_route))

print("Sequence of vehicle in each route : ", end=" ")
print(vrT)

print("Delivery in each period : ", end=" ")
print(deliveryT)
"""************************************************************************"""

"""Calculation of INVENTORY COST"""
inventory_cost = 0
for i in range(period):
    for j in range(1, customer_number):
        inventory_cost += customer_list[j]["h"] * (
            customer_list[j]["I"] + customer_list[j]["dt"][i]
        )
print("Inventory Cost : ", end=" ")
print(inventory_cost)

"""Calculation of Single ROUTING COST"""
visited_node = [[0] * len(distance_matrix)] * len(distance_matrix)
single_routing_cost = 0
single_routing_cost += (best_distance * period) + (
    len(vehicle_route) * distance_matrix[best_route[0]][best_route[-1]]
)
print("Single Routing Cost : ", end=" ")
print(single_routing_cost)


"""Calculation of FIXED COST"""

fixed_cost = len(vehicle_route) * customer_number
print("Fixed cost : ", end=" ")
print(fixed_cost)

print("Total cost : ", end=" ")
print(inventory_cost + V * single_routing_cost + F * fixed_cost)
