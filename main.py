import os
import socket
import threading
import json

HOST = '0.0.0.0'  # Nasłuchiwanie na wszystkich interfejsach
BASE_DIR = './static'  # Katalog z zasobami statycznymi
CONFIG_FILE = 'config.json'  # Plik konfiguracyjny
threads = []  # Lista do śledzenia wątków

# Ładowanie konfiguracji
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

config = load_config()
PORT = config.get("port", 8080)  # Ustawienie domyślnego portu

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("----------------------------------------------------------------------------------------")
        print(request)
        print("----------------------------------------------------------------------------------------")

        # Analiza pierwszej linii żądania HTTP
        lines = request.splitlines()
        if len(lines) > 0:
            request_line = lines[0]
            method, path, _ = request_line.split()

            if method != 'GET':
                send_response(client_socket, 405, 'Method Not Allowed')
                return

            # Sprawdzanie konfiguracji
            if path in config:
                path = config[path]

            # Oczyszczanie ścieżki
            sanitized_path = os.path.abspath(os.path.join(BASE_DIR, path.lstrip('/')))
            print(f"Ścieżka do pliku żądanego przez klienta: {sanitized_path}")

            if not os.path.exists(sanitized_path) or not os.path.isfile(sanitized_path):
                send_response(client_socket, 404, 'Not Found')
                return

            # Wysyłanie zawartości pliku
            with open(sanitized_path, 'rb') as file:
                content = file.read()
            send_response(client_socket, 200, 'OK', content, get_content_type(sanitized_path))
    except Exception as e:
        print(f"Błąd: {e}")
        send_response(client_socket, 500, 'Internal Server Error')
    finally:
        print("Rozłączono z klientem")
        client_socket.close()


def send_response(client_socket, status_code, status_message, body=None, content_type='text/plain'):
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    if body:
        response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"

    client_socket.send(response.encode('utf-8'))
    if body:
        client_socket.send(body)


def get_content_type(file_path):
    if file_path.endswith('.html'):
        return 'text/html'
    elif file_path.endswith('.css'):
        return 'text/css'
    elif file_path.endswith('.js'):
        return 'application/javascript'
    elif file_path.endswith('.txt'):
        return 'text/plain'
    else:
        return 'application/octet-stream'


def start_server():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Połączono z {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
            threads.append(client_thread)  # Dodanie wątku do listy
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")
    finally:
        for thread in threads:
            thread.join()  # Oczekiwanie na zakończenie wątku
        server_socket.close()

if __name__ == '__main__':
    start_server()
