from server import network



server = network()  # start server on local pc

ip = server.get_ip()

client = network(ip, "some ID")# ip and host id


test_message = "hi there"
test_message2 = "hello there"

client.send(test_message)

if server.recive() == test_message:
    print("Sucess")

############################################
client.send(test_message2)

if server.recive() == test_message2:
    print("Seccond Sucess")
