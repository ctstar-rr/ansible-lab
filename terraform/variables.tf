variable "palo_public_ip" {
  description = "Your Palo Alto firewall's public IP"
  type        = string
}

variable "psk" {
  description = "Pre-shared key for VPN tunnel"
  type        = string
  sensitive   = true
}