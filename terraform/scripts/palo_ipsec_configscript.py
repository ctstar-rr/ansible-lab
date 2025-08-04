import datetime

# Map user selection to config values
encryption_options = {
    1: "aes-128-cbc",
    2: "aes-256-cbc",
    3: "des",
    4: "3des"
}

authentication_options = {
    1: "sha1",
    2: "sha256"
}

dh_group_options = {
    1: "group2",
    2: "group5",
    3: "group14"
}

import_next_hop_options = {
    1: "original",
    2: "use-peer"
}

export_next_hop_options = {
    1: "resolve",
    2: "use-self"
}

def get_option(prompt, options):
    print(prompt)
    for key, val in options.items():
        print(f"{key}. {val}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if choice in options:
                return options[choice]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    config_lines = []

    print("\n--- Tunnel Interface ---")
    tunnel_num = input("Tunnel interface number (e.g., 1): ")
    tunnel_ip = input("Tunnel interface IP (e.g., 169.254.1.2/30): ")
    mgmt_profile = input("Interface management profile (e.g., PING_ONLY): ")
    zone = input("Security zone (e.g., CORP_TUNNEL): ")
    virtual_router = input("Virtual router name (e.g., default): ")
    tunnel_desc = input("Enter a description for this tunnel interface (optional): ")

    config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} ip {tunnel_ip}")
    config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} mtu 1427")
    config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} interface-management-profile {mgmt_profile}")
    config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} zone {zone}")
    config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} virtual-router {virtual_router}")

    if tunnel_desc.strip():
        config_lines.append(f"set network interface tunnel units tunnel.{tunnel_num} comment \"{tunnel_desc}\"")

    print("\n--- BGP Configuration ---")
    bgp_peer_group = input("Enter BGP peer group name: ")
    import_next_hop = get_option("Select import next-hop behavior:", import_next_hop_options)
    export_next_hop = get_option("Select export next-hop behavior:", export_next_hop_options)

    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} import next-hop {import_next_hop}")
    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} export next-hop {export_next_hop}")
    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} soft-reset-with-stored-info enable yes")

    print("\n--- BGP Peer Configuration ---")
    peer_name = input("Enter peer name: ")
    peer_asn = input("Enter peer AS number: ")
    peer_ip = input("Enter peer IP address: ")

    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} peer {peer_name} peer-as {peer_asn}")
    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} peer {peer_name} local-address ip {tunnel_ip}")
    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} peer {peer_name} local-address interface tunnel.{tunnel_num}")
    config_lines.append(f"set network virtual-router {virtual_router} protocol bgp peer-group {bgp_peer_group} peer {peer_name} peer-address ip {peer_ip}")

    # Save output to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"palo_ipsec_config_{timestamp}.txt"
    with open(output_filename, "w") as f:
        for line in config_lines:
            f.write(line + "\n")

    print("\n=== Generated Palo Alto Configuration ===\n")
    for line in config_lines:
        print(line)

    print(f"\nConfig saved to: {output_filename}")

if __name__ == "__main__":
    main()
