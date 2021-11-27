import collections
import itertools
from decimal import *


class Path:

    source = None
    destination = None
    route = None
    path = None
    children = None

    def __init__(self, source, destination, route, parent):
        self.path = []
        self.children = []
        self.source = source
        self.destination = destination
        self.route = route
        if parent is not None:
            self.path = list(itertools.chain(self.path, parent))


    def add_link(self, link):
        self.path.append(link)

    def recursively_search(self, all_paths):
        for link in self.route:
            if link[0] == self.source:

                if link[1] == self.destination:
                    self.path.append(link)
                    all_paths.append(self.path)
                else:
                    new_path = Path(link[1], self.destination, self.route, self.path)
                    new_path.add_link(link)
                    self.children.append(new_path)

        for child in self.children:
            child.recursively_search(all_paths)

    def __str__(self):
        return '[source:' + self.source + '; path:' + str(self.path) + ']'


# This function calculates the probability that a packet is successfully
# transmitted over a link, based on the bit error rate and packet size.
def get_link_success_probability(ber, packet_size):
    probability = (1-ber)**packet_size
    return probability


# Transmission on each link can be either succeeded or failed. Hence, there
# are many different combinations. Each combination could lead to either a
# successful or a failed source to destination transmission, which will be
# checked by the check_transmission_success() function below.
def enumerate_all_combinations(route):
    all_combinations = list(itertools.product([0, 1], repeat=len(route)))
    return all_combinations


# Given a route, enumerates all paths from a source to destination
def enumerate_all_paths(source, destination, route):
    all_paths = []
    children = []
    for link in route:
        if link[0] == source:

            if link[1] == destination:
                all_paths.append([].append(link))
            else:
                new_path = Path(link[1], destination, route, None)
                new_path.add_link(link)
                children.append(new_path)

    for child in children:
        child.recursively_search(all_paths)

    return all_paths




# Given a link failure combination, it is possible to determine whether a packet
# can still be transmitted from source to destination. "route" contains all
# the possible links related to a source to destination packet transmission.
def check_transmission_success(all_paths, route, link_failure_combination):

    # Sanity check
    if len(link_failure_combination) != len(route):
        return []

    map = {}

    # Create a mapping from route to combination
    for i in range(len(route)):
           map[route[i]] = link_failure_combination[i]


    # !
    # for m in map:
    #     print(str(m) + ':' + str(map[m]))
    # !

    success_paths = []

    # ======================
    # For each path from source to destination
    # ======================
    for path in all_paths:
        success_paths.append([])
        # ======================
        # For each link in this particular path
        # ======================
        for link in path:
            m = map.get(link) # retrieve whether this link fails or not in this combination
            if m is not None: # sanity check

                if m == 0: # if link fails
                    success_paths = success_paths[:-1]  # reset path since this one does not work
                    break # break the loop, a transmission fails as long as one link of the path fails

                elif m == 1: # if the link does not fail
                    success_paths[-1].append(link) # this link works

    return success_paths



# Given a packet of a certain size, the route that can be used to transmit the
# packet from source to destination, and the bit error rate on each link, this
# function calculates the probability that the packet can be transmitted
# successfully from source to destination. Besides that, it also outputs other
# information, such as packet loss rate, average time in hour between 2 successive
# packet loss, and most importantly a formula which formulates the probability
# calculation.
def total_success_probability_calculation(bit_error_rate, packet_size, route):
    all_combinations = enumerate_all_combinations(route)
    all_paths = enumerate_all_paths('MCU-4', 'SGA', route)
    p = get_link_success_probability(bit_error_rate, packet_size)

    counter = []

    for combination in all_combinations :
        result = check_transmission_success(all_paths, route, combination)

        # ======================
        # If there exists success paths
        # ======================
        if len(result) > 0:

            s = combination.count(1)
            f = combination.count(0)
            counter.append(tuple([s,f]))

    # ======================
    # Count occurences of same probability
    # ======================
    probs = {}
    for i in counter:
        exists = False
        for j in probs:

            # If already exists in probs
            if str(i) == str(j):
                probs[j] += 1
                exists = True;
                break;

        # Add to probs
        if not exists:
            probs[i] = 1

    print()
    print('=====================================')
    print('For packet size: ' + str(packet_size) + ', bit error rate: ' + str(bit_error_rate) + ', network: ' + str(route))
    print('Success probability on a link: ' + str(p))
    print('Formula: ')
    total_success_probability = 0
    for key in probs:
        print(str(probs[key]) + '*p^' + str(key[0]) + '*(1-p)^' + str(key[1]))
        total_success_probability += Decimal(probs[key]*(p**key[0])*((1-p)**key[1]))
    print('Source to destination transmission success probability: ' + str(total_success_probability))
    print('Packet lost rate: ' + str(1-total_success_probability))
    print('Average time between two packet losses (in hours): ' + str(((10/(1-total_success_probability))/1000)/3600))
    return total_success_probability


if __name__ == '__main__':
    # Each network architecture is represented by all the links that can be used
    # for packet transmission from source to destination.
    network1_route = [("MCU-4", "SW_4"), ("MCU-4", "SW_A"), ("SW_4", "SW_A"), ("SW_4", "SW_2"), ("SW_A", "SW_B"),
                      ("SW_2", "SW_B"), ("SW_2", "SGA"), ("SW_B", "SGA")]
    network2_route = [("MCU-4", "SW_4"), ("SW_4", "SW_A"), ("SW_4", "SW_2"), ("SW_A", "SW_B"), ("SW_2", "SW_B"),
                      ("SW_B", "SGA")]
    network3_route = [("MCU-4", "SW_4"), ("SW_4", "SW_2"), ("SW_2", "SW_B"), ("SW_B", "SGA")]

    # Add your code here, which calculates the success probability for frame transmission
    # from source to destination for different bit error rates, and different network architectures.

    getcontext().prec = 28

    total_success_probability_calculation(10**(-10), 3200, network1_route)
    total_success_probability_calculation(10**(-12), 3200, network1_route)

    total_success_probability_calculation(10**(-10), 3200, network2_route)
    total_success_probability_calculation(10**(-12), 3200, network2_route)

    total_success_probability_calculation(10**(-10), 3200, network3_route)
    total_success_probability_calculation(10**(-12), 3200, network3_route)




