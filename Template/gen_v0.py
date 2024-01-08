import json


def lot_of_pt_ex(nb):
    res = ""
    for i in range(nb):
        res = res + "!\n"
    return res


def introduction(data):
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


def neighbors(data):
    res = ""
    res = res + "router bgp " + data["AS"] + "\n"
    res = res + " bgp router-id " + data["id"] + "\n"
    res = res + " bgp log-neighbor-changes\n"
    res = res + " no bgp default ipv4-unicast\n"
    for i in data["BGP"]["neighbors"]:
        res = res + " neighbor " + i["address"] + " remote-as " + i["AS"] + "\n"
        if i["loopback"] == "true":
            res = res + " neighbor " + i["address"] + " update-source Loopback0\n"
    return res


def entracte():
    res = ""
    res = res + " !\n"
    res = res + " address-family ipv4\n"
    res = res + " exit-address-family\n"
    res = res + " !\n"
    return res


def activate(data):
    res = ""
    res = res + " address-family ipv4\n"
    for i in data["interface"]:
        if i["name"] == "Loopback0":
            res = res + "  network " + i["address"] + "\n"
        if i["address"] == "2001:100:102:1::1/64" or i["address"] == "2001:100:101:1::1/64":
            res = res + "  network " + i["address"] + "\n"
    for j in data["BGP"]["neighbors"]:
        res = res + "  neighbor " + j["address"] + " activate\n"
    res = res + " exit-address-family\n"
    res = res + "!\n"
    return res


def bgp(data):
    res = neighbors(data) + entracte() + activate(data)
    return res


def interface(inter):
    s = ""
    s = s + "interface " + inter['name'] + "\n"
    s = s + " no ip address\n"
    s = s + " negotiation auto\n"
    s = s + " ipv6 enable\n"
    s = s + " ipv6 address " + inter['address'] + "\n"
    if inter['RIP'] == "true":
        s = s + " ipv6 rip mrip enable\n"
    elif inter['OSPF'] == "true":
        s = s + " ipv6 ospf 13 area 0\n"
    s = s + "!\n"
    return s


def fast():
    s = "interface FastEthernet0/0\n"
    s = s + " no ip address\n"
    s = s + " shutdown\n"
    s = s + " duplex full\n"
    s = s + "!\n"
    return s


def interfaces(inters):
    s = ""
    for i in inters:
        s = s + interface(i)
        if i['name'] == "Loopback0":
            s = s + fast()
    return s


def end():
    s = "control-plane\n!\n!\n"
    s = s + "line con 0\n"
    s = s + " exec-timeout 0 0\n"
    s = s + " privilege level 15\n"
    s = s + " logging synchronous\n"
    s = s + " stopbits 1\n"
    s = s + "line aux 0\n"
    s = s + " exec-timeout 0 0\n"
    s = s + " privilege level 15\n"
    s = s + " logging synchronous\n"
    s = s + " stopbits 1\n"
    s = s + "line vty 0 4\n"
    s = s + " login\n!\n!\n"
    s = s + "end"
    return s


def proto(routeur):
    s = ""
    if routeur['RIP']['enable'] == "true":
        s = s + "ipv6 router rip mrip\n"
        s = s + " redistribute connected\n"
        s = s + "!\n"
    elif routeur['OSPF']['enable'] == "true":
        s = s + "ipv6 router ospf 13\n"
        s = s + " router-id " + routeur['id'] + "\n"
        if routeur['OSPF']['passive'] != "":
            s = s + " passive-interface " + routeur['OSPF']['passive'] + "\n"
        s = s + "!\n"
    return s


def tail(routeur):
    s = "ip forward-protocol nd\n!\n!\n"
    s = s + "no ip http server\n"
    s = s + "no ip http secure-server\n!\n"
    s = s + proto(routeur)
    s = s + "!\n!\n!\n"
    s = s + end()
    return s


# début

# ouverture du json
file = open('routeurs.json', "r")
data = json.loads(file.read())

s = ""
for i in data['Router']:
    s = introduction(i) + interfaces(i['interface']) + bgp(i) + tail(i)
    # print(s)
    # print(i['name'] + '.cdf')
    with open(i['name'] + '.cdf', "w") as f:
        f.write(s)
        f.close()

# fermeture du json
file.close()
