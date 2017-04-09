# VPC Subnet Calculator

[![Build Status](https://travis-ci.org/tomelliff/vpc-subnet-calculator.svg?branch=master)](https://travis-ci.org/tomelliff/vpc-subnet-calculator) [![Coverage Status](https://coveralls.io/repos/github/tomelliff/vpc-subnet-calculator/badge.svg?branch=master)](https://coveralls.io/github/tomelliff/vpc-subnet-calculator?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/b18cc45300364c5c8edf21666daaaff7)](https://www.codacy.com/app/tomelliff/vpc-subnet-calculator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tomelliff/vpc-subnet-calculator&amp;utm_campaign=Badge_Grade)

Basic Python script to calculate subnets from a VPC CIDR range.

For now it just grabs the maximum allowable space for a tier of private subnets and then, using the remaining space, carves out the maximum allowable space for a tier of public subnets.

The intention is that this should be usable as an [external data source for Terraform](https://www.terraform.io/docs/providers/external/data_source.html) before I work out how to reimplement this in Go so it can be a native data source.

## TODO:

- Add [Terraform external data source](https://www.terraform.io/docs/providers/external/data_source.html) compatible input/output
- Configurable number of "tiers" of subnets
- Dynamically get number of AZs for region from AWS
- IPv6 compatibility
