import os

def collect_tunnel_data(tunnel_num):
    print(f"\n--- Tunnel {tunnel_num} Configuration ---")
    tunnel_interface = input("Tunnel interface number (e.g., 1): ")
    tunnel_ip = input("Tunnel interface IP with /30 (e.g., 169.254.21.2/30): ")
    aws_peer_ip = input("AWS peer IP (e.g., 169.254.21.1): ")
    wan_ip = input("Local WAN IP (e.g., 108.77.196.222): ")
    ike_psk = input("IKE pre-shared key: ")
    ike_profile = f"ike-profile-{tunnel_num}"
    ipsec_profile = f"ipsec-profile-{tunnel_num}"
    ike_gateway = f"ike-gw-{tunnel_num}"
    ipsec_tunnel = f"ipsec-tunnel-{tunnel_num}"
    bgp_peer_name = f"aws-bgp-peer-{tunnel_num}"
    local_asn = input("Local ASN (e.g., 65001): ")
    remote_asn = input("AWS ASN (e.g., 64512): ")
    return {
        "interface": tunnel_interface,
        "tunnel_ip": tunnel_ip,
        "peer_ip": aws_peer_ip,
        "wan_ip": wan_ip,
        "psk": ike_psk,
        "ike_profile": ike_profile,
        "ipsec_profile": ipsec_profile,
        "ike_gateway": ike_gateway,
        "ipsec_tunnel": ipsec_tunnel,
        "bgp_peer_name": bgp_peer_name,
        "local_asn": local_asn,
        "remote_asn": remote_asn
    }

def generate_config(tunnels):
    config_lines = ["configure"]
    for t in tunnels:
        config_lines += [
            f"edit network interface tunnel units tunnel.{t['interface']}",
            f" set ip {t['tunnel_ip']}",
            " set mtu 1427",
            "top",
            f"set zone untrust network layer3 tunnel.{t['interface']}",
            f"set network virtual-router default interface tunnel.{t['interface']}",
            "",
            f"edit network ike crypto-profiles ike-crypto-profiles {t['ike_profile']}",
            " set dh-group group2",
            " set hash sha1",
            " set lifetime seconds 28800",
            " set encryption aes-128-cbc",
            "top",
            f"edit network ike crypto-profiles ipsec-crypto-profiles {t['ipsec_profile']}",
            " set esp authentication sha1",
            " set esp encryption aes-128-cbc",
            " set dh-group group2",
            " set lifetime seconds 3600",
            "top",
            f"edit network ike gateway {t['ike_gateway']}",
            " set protocol version ikev2",
            f" set protocol ikev2 ike-crypto-profile {t['ike_profile']}",
            " set protocol ikev2 dpd enable yes interval 10",
            f" set authentication pre-shared-key key {t['psk']}",
            " set protocol-common nat-traversal enable yes",
            f" set local-address ip {t['wan_ip']}",
            " set local-address interface ethernet1/1",
            f" set peer-address ip {t['peer_ip']}",
            "top",
            f"edit network tunnel ipsec {t['ipsec_tunnel']}",
            f" set auto-key ipsec-crypto-profile {t['ipsec_profile']}",
            f" set auto-key ike-gateway {t['ike_gateway']}",
            f" set tunnel-interface tunnel.{t['interface']}",
            " set anti-replay yes",
            "top",
            f"edit network virtual-router default protocol bgp",
            f" set router-id {t['wan_ip']}",
            " set install-route yes",
            " set enable yes",
            f" set local-as {t['local_asn']}",
            f"  edit peer-group AWS-BGP",
            f"   edit peer {t['bgp_peer_name']}",
            f"    set peer-as {t['remote_asn']}",
            "    set connection-options keep-alive-interval 10",
            "    set connection-options hold-time 30",
            "    set enable yes",
            f"    set local-address ip {t['tunnel_ip']}",
            f"    set local-address interface tunnel.{t['interface']}",
            f"    set peer-address ip {t['peer_ip']}",
            "    top",
            "top",
            ""
        ]
    return "\n".join(config_lines)

def main():
    tunnel_count = int(input("How many IPSec tunnels do you want to configure? "))
    tunnels = []
    for i in range(1, tunnel_count + 1):
        tunnels.append(collect_tunnel_data(i))

    config = generate_config(tunnels)

    print("\n\n=== Generated Palo Alto Configuration ===\n")
    print(config)

    output_path = os.path.join(os.getcwd(), "palo_ipsec_config.txt")
    with open(output_path, "w") as f:
        f.write(config)

    print(f"\nConfig also saved to: {output_path}")

if __name__ == "__main__":
    main()