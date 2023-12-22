import json

# ouverture du json
file = open('file.json', "r")
data = json.loads(file.read())

s = ""
for i in data["Router"]:
    s = s + i['name'] + "*\n"

with open('res.txt', "w") as f :
    f.write(s)
    f.close()


# fermeture du json
file.close()


def interface(inter):
    s = ""
    s = s + "interface " + inter.name + "\n"
    s = s + " no ip address\n"
    s = s + " negotiation auto\n"
    s = s + " ipv6 enable\n"
    s = s + " ipv6 address " + "\n"
    if True :
        s = s + " ipv6 rip mrip enable\n"
    else :
        s = s + ""
    s = s + "!\n"
    return s