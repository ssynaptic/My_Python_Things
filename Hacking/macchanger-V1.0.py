import optparse, re, sys, random
import subprocess as sp

def random_mac(mac):
    x = 0
    for i in mac:
        if i == (":"):
            x += 1
    if x == 5:
        mac = mac.replace(":", "")
        mac = [int(x) for x in mac]
        for i in range(0, 6):
            mac.pop()
        characters = (1, 2, 3, 4, 5, 6, 7, 8,
        9, 0)
        for i in range(0, 6):
            mac.append(random.choice(characters))
        for i in range(2, 16, 3):
            mac.insert(i, ":")
        mac = [str(x) for x in mac]
        mac = "".join(mac)
        return mac
    else:
        return False
def change_mac(interface, mac):
    sp.run(["ifconfig", interface, "down"])
    sp.run(["ifconfig", interface, "hw", "ether", mac])
    sp.run(["ifconfig", interface, "up"])

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", help="Interface to which the MAC address will be changed",
    metavar="INTERFACE", dest="interface", type="string")

    parser.add_option("-m", "--mac", 
    help="The new MAC address to be assigned to the previously given interface",
    metavar="MAC", dest="mac", type="string")

    (options, arguments) = parser.parse_args()
    if options.interface and options.mac:
        return options
    if not options.interface or options.mac:
        parser.error("You did not specify any arguments, run the program with --help to get help")
        sys.exit()

def get_current_mac(interface):
    results = str(sp.check_output(["ifconfig", interface]))
    mac_adress_filtered = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", results)
    if mac_adress_filtered:
        return mac_adress_filtered.group(0)

if __name__ == "__main__":
    try:
        options = get_arguments()
        current_mac = get_current_mac(options.interface)
        new_mac = random_mac(options.mac)
        if current_mac and new_mac:
            print(f"Changing the current MAC Address:", current_mac, 
            "To The New MAC Address:", new_mac)
            change_mac(options.interface, new_mac)

    except:
        print("Error In Program Execution")