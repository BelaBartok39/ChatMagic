# ----------------------
# magical_chat_server.py
# ----------------------
import socket
import threading
from colorama import Fore, Style, init
import random

init(autoreset=True)  # Initialize colorama

# TODO: Refactor get username, give its own thread?
# TODO: Fix user disconnect, nothing happens now
# TODO: Refactor tone of UI, something other than magic forest


# Playful ASCII art options
WELCOME_ART = [
    r"""
    (\\_/)
    (o.o)
    (> <)
    """,
    r"""
     /\_/\\
    ( o.o )
     > ^ <
    """,
    r"""
    .--. 
    |o_o | 
    |:_/ | 
    //   \ \ 
    (|     | ) 
    /'\_   _/`\ 
    \___)=(___/ 
    """
]

class MagicalChatServer:
    def __init__(self, host='0.0.0.0', port=5050):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"{Fore.YELLOW}✨ Server listening on {self.host}:{self.port}")
        print(f"{Fore.CYAN}🐾 Waiting for magical creatures to connect...")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.start()

    def broadcast(self, message, sender=None):
        with self.lock:
            for client in self.clients:
                if client != sender:
                    try:
                        client[0].send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"{Fore.RED}💥 Error broadcasting message: {e}")
                        self.clients.remove(client)

    def handle_client(self, client_socket, addr):
        try:
            # Send welcome message with random ASCII art
            art = random.choice(WELCOME_ART)
            welcome_msg = f"\n{Fore.MAGENTA}{art}\n{Fore.GREEN}🌌 Welcome to the Magical Chat! 🌠\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Get username
            client_socket.send(f"{Fore.CYAN}🔮 Enter your magical name: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            with self.lock:
                self.clients.append((client_socket, username))
            
            join_msg = f"\n{Fore.YELLOW}🌟 {username} has entered the enchanted forest! 🌳\n"
            self.broadcast(join_msg, (client_socket, username))
            
            while True:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                
                if message.lower() == '/quit':
                    break
                
                msg = f"{Fore.BLUE}🧚 {username}: {Style.RESET_ALL}{message}"
                self.broadcast(msg, (client_socket, username))
                
        except Exception as e:
            print(f"{Fore.RED}🔥 Connection error with {addr}: {e}")
        finally:
            with self.lock:
                self.clients.remove((client_socket, username))
                leave_msg = f"\n{Fore.YELLOW}🍂 {username} vanished in a puff of glitter! ✨\n"
                self.broadcast(leave_msg)
                client_socket.close()

if __name__ == "__main__":
    server = MagicalChatServer()
    server.start()
