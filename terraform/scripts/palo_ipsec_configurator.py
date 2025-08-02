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
    print("\n--- Tunnel Interface ---")
    tunnel_num = input("Tunnel interface number (e.g., 1): ")
    tunnel_ip = input("Tunnel interface IP (e.g., 169.254.1.2/30): ")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"palo_ipsec_config_{timestamp}.txt"

    with open(output_filename, "w") as f:
        f.write(f"set network interface tunnel units tunnel.{tunnel_num} ip {tunnel_ip}\n")
        f.write(f"set network interface tunnel units tunnel.{tunnel_num} mtu 1427\n")
        f.write(f"\n")

    print("\n--- IPSec Crypto Profile ---")
    ipsec_name = input("IPSec crypto profile name: ")
    ipsec_encryption = get_option("Select encryption:", encryption_options)
    ipsec_auth = get_option("Select authentication:", authentication_options)
    ipsec_dh_group = get_option("Select DH Group:", dh_group_options)
    ipsec_lifetime = input("Lifetime (seconds): ")

    print("\n--- IKE Crypto Profile ---")
    ike_name = input("IKE crypto profile name: ")
    ike_encryption = get_option("Select encryption:", encryption_options)
    ike_auth = get_option("Select authentication:", authentication_options)
    ike_dh_group = get_option("Select DH Group:", dh_group_options)
    ike_lifetime = input("Lifetime (seconds): ")

    print("\n--- IKE Gateway ---")
    ike_gateway_name = input("IKE Gateway name: ")
    ike_version = input("IKE Version (IKEv1/IKEv2): ")
    ike_interface = input("Interface name (e.g., tunnel.1): ")
    local_ip = input("Local IP address: ")
    peer_ip = input("Remote peer IP address: ")
    ike_crypto_profile = ike_name
    psk = input("Pre-shared key: ")

    print("\n--- IPSec Tunnel ---")
    ipsec_tunnel_name = input("IPSec tunnel name: ")

    print("\n--- BGP Configuration ---")
    router_id = input("BGP Router ID (e.g., WAN IP): ")
    local_as = input("Local AS number: ")
    peer_group = input("Peer group name: ")
    bgp_peer_ip = input("BGP Peer IP address: ")
    remote_as = input("Remote AS number: ")
    import_rule = input("Import rule name: ")
    export_rule = input("Export rule name: ")
    redistribute_profile = input("Redistribution profile name (optional): ")

    with open(output_filename, "a") as f:
        f.write(f"set network ike crypto-profile {ike_name} dh-group {ike_dh_group}\n")
        f.write(f"set network ike crypto-profile {ike_name} authentication sha {ike_auth}\n")
        f.write(f"set network ike crypto-profile {ike_name} encryption {ike_encryption}\n")
        f.write(f"set network ike crypto-profile {ike_name} lifetime seconds {ike_lifetime}\n")
        f.write(f"\n")
        f.write(f"set network tunnel ipsec-crypto-profile {ipsec_name} encryption {ipsec_encryption}\n")
        f.write(f"set network tunnel ipsec-crypto-profile {ipsec_name} authentication {ipsec_auth}\n")
        f.write(f"set network tunnel ipsec-crypto-profile {ipsec_name} dh-group {ipsec_dh_group}\n")
        f.write(f"set network tunnel ipsec-crypto-profile {ipsec_name} lifetime seconds {ipsec_lifetime}\n")
        f.write(f"\n")
        f.write(f"set network ike gateway {ike_gateway_name} protocol {ike_version}\n")
        f.write(f"set network ike gateway {ike_gateway_name} interface {ike_interface}\n")
        f.write(f"set network ike gateway {ike_gateway_name} local-address ip {local_ip}\n")
        f.write(f"set network ike gateway {ike_gateway_name} peer-address ip {peer_ip}\n")
        f.write(f"set network ike gateway {ike_gateway_name} authentication pre-shared-key key {psk}\n")
        f.write(f"set network ike gateway {ike_gateway_name} nat-traversal enable true\n")
        f.write(f"set network ike gateway {ike_gateway_name} ike-crypto-profile {ike_crypto_profile}\n")
        f.write(f"set network ike gateway {ike_gateway_name} dpd enable true\n")
        f.write(f"\n")
        f.write(f"set network ipsec tunnel {ipsec_tunnel_name} auto-key ike-gateway {ike_gateway_name}\n")
        f.write(f"set network ipsec tunnel {ipsec_tunnel_name} auto-key ipsec-crypto-profile {ipsec_name}\n")
        f.write(f"set network ipsec tunnel {ipsec_tunnel_name} tunnel-interface tunnel.{tunnel_num}\n")
        f.write(f"\n")
        f.write(f"set network virtual-router default protocol bgp router-id {router_id}\n")
        f.write(f"set network virtual-router default protocol bgp enable yes\n")
        f.write(f"set network virtual-router default protocol bgp local-as {local_as}\n")
        f.write(f"set network virtual-router default protocol bgp peer-group {peer_group} enable yes\n")
        f.write(f"set network virtual-router default protocol bgp peer-group {peer_group} peer {bgp_peer_ip} peer-as {remote_as}\n")
        f.write(f"set network virtual-router default protocol bgp peer-group {peer_group} peer {bgp_peer_ip} enable yes\n")
        f.write(f"set network virtual-router default protocol bgp import rule {import_rule}\n")
        f.write(f"set network virtual-router default protocol bgp export rule {export_rule}\n")
        if redistribute_profile:
            f.write(f"set network virtual-router default protocol bgp redistribute profile {redistribute_profile}\n")

    print(f"\nPalo IPSec config saved to {output_filename}")


if __name__ == "__main__":
    main()
