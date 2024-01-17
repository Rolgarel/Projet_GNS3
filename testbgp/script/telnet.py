import telnetlib
import gns3fy

HOST = "localhost"
PROJECT_ID = "a2e5c444-949d-4ae8-99de-55957d4e9dc4"
server = gns3fy.Gns3Connector("http://" + HOST + ":3080")
project = gns3fy.Project(name="modele_reduit", connector=server)
project.get()
project.open()

nodes = server.nodes
for i in nodes:
    print(i)

# tn = telnetlib.Telnet(HOST, 5001)

# tn.write("")

tn.write(b"int Loopback0")
tn.write(b"shutdown")

# l = tn.read_all()
# print(l)
