import itertools
from decimal import *


# This function calculates the probability that a packet is successfully
# transmitted over a link, based on the bit error rate and packet size.
def get_link_success_probability(ber, packet_size):
    probability = (1-ber)**packet_size;
    return probability


# Transmission on each link can be either succeeded or failed. Hence, there
# are many different combinations. Each combination could lead to either a
# successful or a failed source to destination transmission, which will be
# checked by the check_transmission_success() function below.
def enumerate_all_combinations(route):
    all_combinations = list(itertools.product([0, 1], repeat=len(route)))
    return all_combinations


# Given a link failure combination, it is possible to determine whether a packet
# can still be transmitted from source to destination. "route" contains all
# the possible links related to a source to destination packet transmission.
def check_transmission_success(source, destination, route, link_failure_combination):
    path = []
    for link in route:
        if link[0] == source:
            path.append(link)
            source = link[1]
            if link[1] == destination:
                print(route)
                print(str(path))





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

    combinations = enumerate_all_combinations(network2_route)
    #for c in combinations:
    check_transmission_success('MCU-4', 'SGA', network2_route, None)
