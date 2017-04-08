#!/usr/bin/env python
from __future__ import print_function
import argparse
import math

import netaddr


def get_next_binary(integer):
    next_binary = int(math.pow(2, math.ceil(math.log(integer) / math.log(2))))

    # We explicitly want the *next* binary so if integer is already a binary
    # number then we need to recursively call this method with integer + 1
    if next_binary == integer:
        next_binary = get_next_binary(integer + 1)

    return int(next_binary)


def subtract_subnets_from_range(cidr_range, subnets):
    full_range = netaddr.IPNetwork(cidr_range)
    # Assume subtracting equal sized subnets for now
    subnet_mask_bits = netaddr.IPNetwork(subnets[0]).prefixlen
    remaining_subnets = [str(subnet)
                         for subnet in full_range.subnet(subnet_mask_bits)
                         if str(subnet) not in subnets]

    # Just return the largest single range
    return str(netaddr.cidr_merge(remaining_subnets)[0])


def maximise_subnets(cidr_range, num_subnets):
    MAX_AWS_VPC_SUBNET_BIT_MASK = 28
    MIN_AWS_VPC_SUBNET_BIT_MASK = 16
    full_range = netaddr.IPNetwork(cidr_range)
    full_range_mask_bits = full_range.prefixlen
    subnet_mask_bits = (full_range_mask_bits +
                        int(math.log(get_next_binary(num_subnets), 2)))
    if subnet_mask_bits > MAX_AWS_VPC_SUBNET_BIT_MASK:
        raise ValueError('Minimum subnet size is /{}'.format(
                         MAX_AWS_VPC_SUBNET_BIT_MASK))
    elif subnet_mask_bits < MIN_AWS_VPC_SUBNET_BIT_MASK:
        raise ValueError('Maximum subnet size is /{}'.format(
                         MIN_AWS_VPC_SUBNET_BIT_MASK))

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


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Calculate subnets for an AWS VPC')
    parser.add_argument('vpc_cidr_range',
                        help='eg. 10.0.0.0/16')
    parser.add_argument('num_azs', type=int,
                        help='Number of AZs to use')
    args = parser.parse_args()

    return (args.vpc_cidr_range, args.num_azs)


def main():
    vpc_cidr_range, num_azs = arg_parser()
    subnets = calculate_subnets(vpc_cidr_range, num_azs)
    for subnet in subnets:
        print(subnet)


if __name__ == '__main__':
    main()
