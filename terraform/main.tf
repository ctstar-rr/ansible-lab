provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "lab_vpc" {
  cidr_block = "10.10.0.0/16"
  tags = {
    Name = "hybrid-lab-vpc"
  }
}

resource "aws_internet_gateway" "lab_igw" {
  vpc_id = aws_vpc.lab_vpc.id
}

resource "aws_subnet" "lab_subnet" {
  vpc_id                  = aws_vpc.lab_vpc.id
  cidr_block              = "10.10.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_customer_gateway" "palo" {
  bgp_asn    = 65001
  ip_address = var.palo_public_ip
  type       = "ipsec.1"
  tags = {
    Name = "EVE-NG-PaloCGW"
  }
}

resource "aws_vpn_gateway" "lab_vgw" {
  vpc_id = aws_vpc.lab_vpc.id
  tags = {
    Name = "lab-vpn-gw"
  }
}

resource "aws_vpn_connection" "lab_vpn" {
  vpn_gateway_id      = aws_vpn_gateway.lab_vgw.id
  customer_gateway_id = aws_customer_gateway.palo.id
  type                = "ipsec.1"
  static_routes_only  = false

  tunnel1_inside_cidr     = "169.254.21.0/30"
  tunnel1_preshared_key   = var.psk

  tunnel2_inside_cidr     = "169.254.22.0/30"
  tunnel2_preshared_key   = var.psk

  tags = {
    Name = "lab-vpn-bgp"
  }
}

resource "aws_vpn_connection_route" "to_lab" {
  destination_cidr_block = "10.15.0.0/16"
  vpn_connection_id      = aws_vpn_connection.lab_vpn.id
}