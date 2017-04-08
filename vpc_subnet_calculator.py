#!/usr/bin/env python
import math

import netaddr


def get_next_binary(integer):
    next_binary = int(math.pow(2, math.ceil(math.log(integer)/math.log(2))))

    # We explicitly want the *next* binary so if integer is already a binary
    # number then we need to recursively call this method with integer + 1
    if next_binary == integer:
        next_binary = get_next_binary(integer + 1)

    return int(next_binary)


def subtract_subnets_from_range(cidr_range, subnets):
    full_range = netaddr.IPNetwork(cidr_range)
    # Assume subtracting equal sized subnets for now
    subnet_mask_bits = netaddr.IPNetwork(subnets[0]).prefixlen

    remaining_subnets = []
    for subnet in full_range.subnet(subnet_mask_bits):
        if str(subnet) not in subnets:
            remaining_subnets.append(str(subnet))

    # Just return the largest single range
    return str(netaddr.cidr_merge(remaining_subnets)[0])


def maximise_subnets(cidr_range, num_subnets):
    full_range = netaddr.IPNetwork(cidr_range)
    full_range_mask_bits = full_range.prefixlen
    subnet_mask_bits = (full_range_mask_bits +
                        int(math.log(get_next_binary(num_subnets), 2)))

    # list(vpc.subnet(mask_bits)) returns list of netaddr.ip.IPNetwork objects
    # We want a list of the string representations instead
    subnets = []
    for subnet in full_range.subnet(subnet_mask_bits):
        if len(subnets) < num_subnets:
            subnets.append(str(subnet))

    return subnets


def calculate_subnets(vpc_cidr_range, num_azs):
    private_subnets = maximise_subnets(vpc_cidr_range, num_azs)
    remaining_space = subtract_subnets_from_range(vpc_cidr_range,
                                                  private_subnets)
    public_subnets = maximise_subnets(remaining_space, num_azs)

    return private_subnets + public_subnets
