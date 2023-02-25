import scapy.all as scapy
from argparse import ArgumentParser

def get_arguments():
	parser = ArgumentParser(description="Network Gateway")
	parser.add_argument("-i", "--ip", action="store", dest="ip",
	help="Your Network Gateway", metavar="IP", required=True)

	args = parser.parse_args()
	return args

def scan(gateway):
	answers = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=gateway), timeout=1, verbose=False)[0]
	clients_list = []
	for element in answers:
		client_dict = {"IP":element[1].psrc, "MAC":element[1].hwsrc}
		clients_list.append(client_dict)
	return clients_list

def show_results(clients_list):
	print("IP\t\t\t MAC Address")
	for client in clients_list:
		print(client["IP"], "\t\t", client["MAC"])
if __name__ == "__main__":
	args = get_arguments()
	scanning = scan(str(args.ip))
	show_results(scanning)