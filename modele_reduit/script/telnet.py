import telnetlib
import gns3fy
import time


HOST = "localhost"
# port du routeur (généralement dans les 5000)
port = 5000


try:
    # ouverture de la connexion avec le routeur
    tn = telnetlib.Telnet(HOST, port)

    # création de la suite de lignes de commandes
    s = "conf t\r"
    s = s + "interface Loopback0\r"
    s = s + "no shutdown\r"
    s = s + "end\r"

    # transmission de la suite de lignes de commandes
    tn.write(s.encode())

except Exception as err:
    print("Erreur: connexion impossible ou transmission de commande impossible", err)
