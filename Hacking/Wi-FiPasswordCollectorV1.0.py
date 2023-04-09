# This script will obtain all the Wi-Fi networks with their passwords
# from the machine where it is hosted and then send the content to other
# devices where the "Client.py" script is running.

# The ip address and port of the server must be specified in the PRMTR.json file

import subprocess as sp
import re, time, sys, platform, json

if __name__ == "__main__":
    try:
        if platform.system() != ("Windows"):
            print("Este programa solo funciona en Windows")
        print("Obtaining Avaiable Networks")
        networks = sp.run(["netsh", "wlan", "show",
        "profiles"],capture_output=True).stdout.decode("latin1")
        profiles = re.findall("Perfil de todos los usuarios\s+:\s(.*)\r",
        networks)

        wifi_networks = {}
        if len(profiles) != 0:
            print("Las redes encontradas son: \n")
            for i in profiles:
                print(i, "\n")

            for i in profiles:
                profile_details = sp.run(["netsh", "wlan", "show", "profile",
                f"name={i}", "key=clear"], capture_output=True).stdout.decode("latin1")
                password = re.findall("Contenido de la clave\s+:\s+(.*)\r",
                profile_details)
                wifi_networks.update({i:password})
            print("""A continuacion se muestra las redes con sus respectivas
contraseñas:\n""")
            print(wifi_networks)
            print("""\nEste programa se cerrara dentro de 60 segundos.\n
Tambien puede ver el archivo NETWORKS.txt en el que se encuentran las redes
con sus respectivas contraseñas""")
            with open("NETWORKS.txt", "a+") as file:
                file.write("NETWORK/PASSWORD\n\n")
                file.write(str(wifi_networks))
            time.sleep(60)
            sys.exit()
        else:
            print("No pudimos encontrar redes disponibles")
    except KeyboardInterrupt:
        if wifi_networks:
            sys.exit()
        else:
            print("\nHa cancelado la ejecucion del programa")
    except:
        print("Ha ocurrido un error")
