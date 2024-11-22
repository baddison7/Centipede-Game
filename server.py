import socket, time
from _thread import start_new_thread


server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Binding error: {e}")

player_cap = 3
s.listen(player_cap)
print("Waiting for a connection, Server Started")

class game:
    def __init__(self):
        self.player_count = 0
        self.round = -1
        self.current_player = 1  # Start with player 1
        self.game_state = 'waiting'
        self.end_round = 0

    def next_turn(self):
        self.round += 1
        if self.round % self.player_count == 0: self.current_player = self.player_count
        else: self.current_player = self.round % self.player_count


class player:
    def __init__(self, conn, addr, player_num):
        self.conn = conn
        self.addr = addr
        self.player_num = player_num
        self.total = 0
        self.counted = False
    
    def turn(self, round):
        if round != -1: self.conn.send(str.encode(f'round {round}'))

# Client handler function
def client_thread(conn, addr, player_number):
    p = player(conn, addr, player_number)
    print("Connected to:", p.addr, "as player", p.player_num)
    p.conn.send(str.encode("Connected to server"))

    # part to see who starts the game
    if p.player_num != 1:
        while True:
            if g.player_count == player_cap:
                g.game_state = 'running'
                g.round = 1
                break
            else:
                time.sleep(0.1) # Avoid busy-waiting

    # game loop
    while True:
        try:
            if g.current_player == p.player_num:
                if g.game_state == 'running':
                    p.counted = False
                    p.turn(g.round)
                    data = p.conn.recv(2048)
                    if not data:
                        print(f"Player {p.player_num} disconnected")
                        break
                    msg = data.decode("utf-8")
                    if msg == 'take':
                        p.total += 4*2**(g.round -1)
                        g.end_round = g.round
                        p.counted = True
                        p.conn.send(str.encode(f'game over, total: {p.total}'))
                        g.game_state = 'over'
                    g.next_turn()

                elif g.game_state == 'over':
                    if p.counted == False:
                        p.counted = True
                        p.total += 1*2**(g.end_round -1)
                        g.next_turn()
                        p.conn.send(str.encode(f'game over, total: {p.total}'))
                    elif p.counted == True:
                        g.game_state == 'running'
                        g.round = 1
                        g.end_round = 0

                        # MAKE RESET FUNCTIONS FOR P AND G AND UR DONE

            else:
                time.sleep(0.1)  # Avoid busy-waiting
        except Exception as e:
            print(f"Error with {addr}: {e}")
            break

    conn.close()

g = game()
while True:
    conn, addr = s.accept()
    g.player_count += 1
    start_new_thread(client_thread, (conn, addr, g.player_count))
