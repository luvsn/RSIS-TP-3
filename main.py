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


class Architecture:

    combinations = None
    paths = None

    def __init__(self):
        self.combinations = combinations
        self.paths = paths


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




# Given a packet of a certain size, the route that can be used to transmit the
# packet from source to destination, and the bit error rate on each link, this
# function calculates the probability that the packet can be transmitted
# successfully from source to destination. Besides that, it also outputs other
# information, such as packet loss rate, average time in hour between 2 successive
# packet loss, and most importantly a formula which formulates the probability
# calculation.
def total_success_probability_calculation(bit_error_rate, packet_size, route):
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

    # total_success_probability_calculation(10**(-10), 3200, network1_route)
    # total_success_probability_calculation(10**(-12), 3200, network1_route)
    #
    # total_success_probability_calculation(10**(-10), 3200, network2_route)
    # total_success_probability_calculation(10**(-12), 3200, network2_route)
    #
    # total_success_probability_calculation(10**(-10), 3200, network3_route)
    # total_success_probability_calculation(10**(-12), 3200, network3_route)

    combinations = enumerate_all_combinations(network1_route)
    paths = enumerate_all_paths('MCU-4', 'SGA', network1_route)
    print(str(combinations))
    print(str(paths))
    #for c in combinations:
    #check_transmission_success('MCU-4', 'SGA', network1_route, None)
