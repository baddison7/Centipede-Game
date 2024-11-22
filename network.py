import socket, time, re, os

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()
        self.round = 0

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(self.client.recv(2048).decode())
        except Exception as e:
            print(f"Connection error: {e}")
            exit()
    
    def turn(self):
        print(f'large pot: {4*2**(self.round - 1)}\nSmall pot: {1*2**(self.round - 1)}\nPass or Take')
        action = input("Your move (pass/take): ").lower()
        while action not in ['pass', 'take']:
            print("Invalid input. Please choose 'pass' or 'take'.")
            action = input("Your move (pass/take): ").lower()
        self.client.send(str.encode(action))

    
    def listen_for_turn(self):
        while True:
            try:

                response = self.client.recv(2048).decode()
                if response != '': 
                    print(response)
                    if "round" in response:
                        match = re.match(r"^.*\b(\d+)$", response)
                        if match:
                            self.round = int(match.group(1))
                        self.turn()
            except Exception as e:
                print(f"Error: {e}")
                # break

n = Network()
n.listen_for_turn()



# im going to to a/my nut in a minut
# because you push me so far