output "vpn_connection_id" {
  value = aws_vpn_connection.lab_vpn.id
}

output "tunnel1_inside_cidr" {
  value = aws_vpn_connection.lab_vpn.tunnel1_inside_cidr
}

output "tunnel2_inside_cidr" {
  value = aws_vpn_connection.lab_vpn.tunnel2_inside_cidr
}