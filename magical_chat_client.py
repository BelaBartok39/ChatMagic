# ----------------------
# magical_chat_client.py
# ----------------------
import socket
import threading
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

class MagicalChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"{Fore.GREEN}🌈 Connected to the enchanted server!")
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            
            # Send messages
            while self.running:
                message = input(f"{Fore.YELLOW}🌠 You: ")
                self.client_socket.send(message.encode('utf-8'))
                
                if message.lower() == '/quit':
                    self.running = False
                    break
                    
        except Exception as e:
            print(f"{Fore.RED}💫 Connection lost: {e}")
        finally:
            self.client_socket.close()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}{Style.RESET_ALL}\n{Fore.YELLOW}🌠 Enter name: ", end="")
            except Exception as e:
                print(f"{Fore.RED}💥 Error receiving messages: {e}")
                self.running = False
                break

if __name__ == "__main__":
    print(f"{Fore.CYAN}🦄 Welcome to Magical Chat!")
    host = input("🏰 Enter server IP: ")
    client = MagicalChatClient(host, 5050)
    client.start()
