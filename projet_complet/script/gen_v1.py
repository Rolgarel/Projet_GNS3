import json


# génération d'une suite de lignes  contenant un point d'exclamation
def lot_of_pt_ex(nb):
    res = ""
    for i in range(nb):
        res = res + "! \n"
    return res


def introduction(data):
    t = lot_of_pt_ex(4)
    t = t + " \n"
    t = t + "! \n"
    t = t + "! Last configuration change at 00:00:00 UTC Mon Jan 01 2024\n"
    t = t + "! \n"
    t = t + "version 15.2\n"
    t = t + "service timestamps debug datetime msec\n"
    t = t + "service timestamps log datetime msec\n"
    t = t + "! \n"
    t = t + "hostname R" + str(data["name"]) + "\n"
    t = t + "! \n"
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


def neighbors(data, prefixe):
    res = ""
    res = res + "router bgp " + data["AS"] + "\n"
    res = res + " bgp router-id " + data["id"] + "\n"
    res = res + " bgp log-neighbor-changes\n"
    res = res + " no bgp default ipv4-unicast\n"
    for i in data["BGP"]["neighbors"]:
        res = res + " neighbor " + other_router_bgp_address(prefixe, i, data) + " remote-as " + i["AS"] + "\n"
        if i["loopback"] == "true":
            res = res + " neighbor " + other_router_bgp_address(prefixe, i, data) + " update-source Loopback0\n"
    return res


def entracte():
    res = ""
    res = res + " !\n"
    res = res + " address-family ipv4\n"
    res = res + " exit-address-family\n"
    res = res + " !\n"
    return res


def activate(data, prefixe):
    res = ""
    res = res + " address-family ipv6\n"
    for i in data["interface"]:
        res = res + "  network " + network_address(i, data, prefixe) + "\n"
    for j in data["BGP"]["neighbors"]:
        res = res + "  neighbor " + other_router_bgp_address(prefixe, j, data) + " activate\n"
        res = res + "  neighbor " + other_router_bgp_address(prefixe, j, data) + " send-community\n"
        if data["border"] == "true":  # si c'est un routeur de bordure, il applique les communities et filtres
            if j["who"] != "self" and j["who"] == "client":
                res = res + "  neighbor " + other_router_bgp_address(prefixe, j, data) + " route-map CLIENT in\n"
                res = res + "  neighbor " + other_router_bgp_address(prefixe, j, data) + " route-map COMM out\n"
            elif j["who"] != "self" and j["who"] == "peer":
                res = res + "  neighbor " + other_router_bgp_address(prefixe, j, data) + " route-map PEER in\n"

    res = res + " exit-address-family\n"
    res = res + "! \n"
    return res


def bgp(data, prefixe):
    res = neighbors(data, prefixe) + entracte() + activate(data, prefixe)
    return res


def interface(inter, routeur, prefixe):
    s = ""
    s = s + "interface " + inter['name'] + "\n"
    s = s + " no ip address\n"
    if inter["name"] != "Loopback0":
        s = s + " negotiation auto\n"
    s = s + " ipv6 enable\n"
    s = s + " ipv6 address " + interface_address(inter, routeur, prefixe) + "\n"
    if inter['RIP'] == "true":
        s = s + " ipv6 rip mrip enable\n"
    elif inter['OSPF'] == "true":
        s = s + " ipv6 ospf 13 area 0\n"
        if inter['OSPF_COST']['address'] != "":
            s = s + " ipv6 ospf neighbor " + inter['OSPF_COST']['address'] + " cost " + str(inter['OSPF_COST']['cost']) + "\n"
    s = s + "! \n"
    return s


def fast():
    s = "interface FastEthernet0/0\n"
    s = s + " no ip address\n"
    s = s + " shutdown\n"
    s = s + " duplex full\n"
    s = s + "! \n"
    return s


def interfaces(inters, routeur, prefixe):
    s = ""
    for i in inters:
        s = s + interface(i, routeur, prefixe)
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
        s = s + "! \n"
    elif routeur['OSPF']['enable'] == "true":
        s = s + "ipv6 router ospf 13\n"
        s = s + " router-id " + routeur['id'] + "\n"
        if routeur['OSPF']['passive'] != "":
            s = s + " passive-interface " + routeur['OSPF']['passive'] + "\n"
        s = s + "! \n"
    return s


def filtre(routeur):
    res = ""
    client = 0
    peer = 0
    if routeur["border"] == "true":  # si c'est un routeur de bordure, il définit les communities et filtres
        res = res + "route-map COMM permit 10\n"
        res = res + " match community 22\n"
        res = res + "!\n"
        res = res + "route-map COMM deny 20\n!\n"
        for i in routeur["BGP"]["neighbors"]:
            if i["who"] != "self" and i["who"] == "client":
                client = client + 1
            elif i["who"] != "self" and i["who"] == "peer":
                peer = peer + 1
        if client > 0:
            res = res + "route-map CLIENT permit 10\n"
            res = res + " set community " + routeur["AS"] + ":600 additive\n"
        elif peer > 0:
            res = res + "route-map PEER permit 10\n"
        
    return res


def tail(routeur):
    s = "ip forward-protocol nd\n!\n"
    s = s + "ip bgp-community new-format\n"
    if routeur["border"] == "true":
        s = s + "ip community-list 22 permit " + str(routeur["AS"]) + ":600\n!\n" 
    s = s + "no ip http server\n"
    s = s + "no ip http secure-server\n!\n"
    s = s + proto(routeur)
    s = s + "!\n"
    s = s + filtre(routeur)
    s = s + "!\n!\n!\n"
    s = s + end()
    return s


def loopback_address(routeur, prefixe, net):
    res = prefixe['intra'] + str(int(routeur['name'] / 10)) + ":"
    res = res + str(11*(routeur['name'] % 10))
    if not net:
        res = res + "::1" + prefixe['mask']
    else:
        res = res + "::" + prefixe['mask']
    return res


# fonction générant les adresses des réseaux pour la partie network advertisement de la configuration
def network_address(inter, routeur, prefixe):
    # Si le sous-réseau correspond à un LAN
    if inter['voisin'] < 0:
        res = prefixe['intra'] + str(int(routeur['name'] / 10)) + ":"
        res = res + str(abs(inter['voisin']))
        res = res + "::" + prefixe['mask']
    # Si le sous-réseau correspond à un loopback
    elif inter['voisin'] == 0:
        res = loopback_address(routeur, prefixe, True)
    # Si le sous-réseau correspond à un lien avec un routeur
    else:
        # Si dans le même AS
        if int(routeur['name'] / 10) == int(inter['voisin'] / 10):
            res = prefixe['intra'] + str(int(routeur['name'] / 10)) + ":"
            res = res + str(max(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + str(min(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + "::" + prefixe['mask']
        # Sinon
        else:
            res = prefixe['extra']
            res = res + str(max(int(routeur['name'] / 10), int(inter['voisin'] / 10)))
            res = res + str(min(int(routeur['name'] / 10), int(inter['voisin'] / 10)))
            res = res + str(max(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + "::" + prefixe['mask']
    return res


# fonction générant les adresses des interfaces pour la partie interface de la configuration
def interface_address(inter, routeur, prefixe):
    # Si le sous-réseau correspond à un LAN
    if inter['voisin'] < 0:
        res = prefixe['intra'] + str(int(routeur['name'] / 10)) + ":"
        res = res + str(abs(inter['voisin']))
        res = res + "::" + str(1) + prefixe['mask']
    # Si le sous-réseau correspond à un loopback
    elif inter['voisin'] == 0:
        res = loopback_address(routeur, prefixe, False)
    # Si le sous-réseau correspond à un lien avec un routeur
    else:
        # Si dans le même AS
        if int(routeur['name']/10) == int(inter['voisin']/10):
            res = prefixe['intra'] + str(int(routeur['name']/10)) + ":"
            res = res + str(max(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + str(min(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + "::" + str(routeur['name'] % 10) + prefixe['mask']
        # Sinon
        else:
            res = prefixe['extra']
            res = res + str(max(int(routeur['name']/10), int(inter['voisin']/10)))
            res = res + str(min(int(routeur['name']/10), int(inter['voisin']/10)))
            res = res + str(max(routeur['name'] % 10, inter['voisin'] % 10))
            res = res + "::" + str(int(routeur['name']/10)) + prefixe['mask']
    return res


# génération des adresses des voisins BGP
def other_router_bgp_address(prefixe, neighbor, self):
    # Si dans le même AS (adresse de loopback)
    if self['AS'] == neighbor['AS']:
        res = prefixe['intra'] + str(int(self['name']/10)) + ":"
        res = res + str(11*(neighbor['voisin'] % 10))
        res = res + "::1"
    # Sinon
    else:
        res = prefixe['extra']
        res = res + str(max(int(self['name'] / 10), int(neighbor['voisin'] / 10)))
        res = res + str(min(int(self['name'] / 10), int(neighbor['voisin'] / 10)))
        res = res + str(max(self['name'] % 10, neighbor['voisin'] % 10))
        res = res + "::" + str(int(neighbor['voisin'] / 10))
    return res


if __name__ == "__main__":
    # début

    # ouverture du json
    file = open('routeurs.json', "r")
    data = json.loads(file.read())

    s = ""
    for i in data['Router']:
        s = introduction(i) + interfaces(i['interface'], i, data['Prefixes']) + bgp(i, data['Prefixes']) + tail(i)
        # print(s)
        # print(i['name'] + '.cdf')
        with open(i['PATH'] + i['file'], "w") as f:
            f.write(s)
            f.close()

    # fermeture du json
    file.close()
