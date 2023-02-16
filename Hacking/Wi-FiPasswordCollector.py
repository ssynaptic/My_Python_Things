import subprocess as sp
import re

if __name__ == "__main__":
    print("Obtaining Avaiable Networks")
    networks = sp.run(["netsh", "wlan", "show",
    "profiles"],capture_output=True).stdout.decode()
    profiles = re.findall("Perfil de todos los usuarios\s+:\s(.*)\r",
    networks)

    wifi_networks = {}
    if len(profiles) != 0:
        print("Las redes encontradas son: \n")
        for i in profiles:
            print(i, "\n")

        for i in profiles:
            profile_details = sp.run(["netsh", "wlan", "show", "profile",
            f"name={i}", "key=clear"], capture_output=True).stdout.decode()
            password = re.findall("Contenido de la clave\s+:\s+(.*)\r",
            profile_details)
            wifi_networks.update({i:password})
        print("""A continuacion se muestra las redes con sus respectivas
contraseñas:\n""")
        print(wifi_networks)
    else:
        print("No pudimos encontrar redes disponibles")
