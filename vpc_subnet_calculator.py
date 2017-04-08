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


def calculate_private_subnets(vpc_cidr_range, num_azs):
    vpc = netaddr.IPNetwork(vpc_cidr_range)
    vpc_mask_bits = vpc.prefixlen
    private_subnet_mask_bits = (vpc_mask_bits +
                               int(math.log(get_next_binary(num_azs), 2)))

    # list(vpc.subnet(mask_bits)) returns list of netaddr.ip.IPNetwork objects
    # We want a list of the string representations instead
    private_subnets = []
    for private_subnet in vpc.subnet(private_subnet_mask_bits):
        if len(private_subnets) < num_azs:
            private_subnets.append(str(private_subnet))

    return private_subnets
