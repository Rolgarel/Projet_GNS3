import json

# ouverture du json
file = open('template.json', "r")
data = json.loads(file.read())

s = ""
for i in data["Router"]:
    s = s + i['name'] + "*\n"

with open('res.txt', "w") as f :
    f.write(s) #f.write(s)
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

def introduction(data):
    t = ""
    t = lot_of_pt_ex(7)
    t = t + "! Last configuration change at 00:00:00 UTC Mon Jan 01 2024\n"
    t = t + "!\n"
    t = t + "version 15.2\n"
    t = t + "service timestamps debug datetime msec\n"
    t = t + "service timestamps log datetime msec\n"
    t = t + "!\n"
    t = t + "hostname " + data["name"] + "\n"
    t = t + "!\n"
    t = t + "boot-start-marker\n"
    t = t + "boot-end-marker\n"
    t = t + lot_of_pt_ex(3)
    t = t + "no aaa new-model\n"
    t = t + "no ip icmp rate-limit unreachable\n"
    t = t + "ip cef\n"
    t = t + lot_of_pt_ex(6)
    t = t + "no ip domain lookup\n"
    t = t + "ipv6 unicast-routing\n"
    t = t + "ipv6 cef\n"
    t = t + lot_of_pt_ex(2)
    t = t + "multilink bundle-name authenticated\n"
    t = t + lot_of_pt_ex(9)
    t = t + "ip tcp synwait-time 5\n"
    t = t + lot_of_pt_ex(12)
    return t

def lot_of_pt_ex(nb):
    res = ""
    for i in range (nb):
        res = res + "!\n"
    return res
