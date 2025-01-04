import os
import socket
import threading
import json
import logging

HOST = '0.0.0.0'  # Nasłuchiwanie na wszystkich interfejsach
CONFIG_FILE = 'config.json'  # Plik konfiguracyjny
threads = []  # Lista do śledzenia wątków

logging.basicConfig(level=logging.INFO)

# Ładowanie konfiguracji
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

config = load_config()

def handle_client(client_socket, base_dir):
    try:
        request = client_socket.recv(4096).decode('utf-8')
        logging.info("Received request:")
        logging.info(request)

        # Analiza pierwszej linii żądania HTTP
        lines = request.splitlines()
        if len(lines) > 0:
            request_line = lines[0]
            method, path, _ = request_line.split()

            if method not in ['GET', 'HEAD']:
                send_response(client_socket, 405, 'Method Not Allowed')
                return

            # Oczyszczanie ścieżki
            sanitized_path = os.path.abspath(os.path.join(base_dir, path.lstrip('/')))
            if os.path.isdir(sanitized_path):
                sanitized_path = os.path.join(sanitized_path, 'index.html')
            logging.info(f"Ścieżka do pliku żądanego przez klienta: {sanitized_path}")

            if not os.path.exists(sanitized_path) or not os.path.isfile(sanitized_path):
                send_response(client_socket, 404, 'Not Found')
                return

            # Wysyłanie zawartości pliku
            if method == 'HEAD':
                send_response(client_socket, 200, 'OK', content=None, content_type=get_content_type(sanitized_path))
                return

            with open(sanitized_path, 'rb') as file:
                content = file.read()
            send_response(client_socket, 200, 'OK', content, get_content_type(sanitized_path))
    except Exception as e:
        logging.error(f"Błąd: {e}")
        send_response(client_socket, 500, 'Internal Server Error')
    finally:
        logging.info("Rozłączono z klientem")
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
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif file_path.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream'


def start_server(port, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port))
    server_socket.listen(5)
    logging.info(f"Serwer nasłuchuje na {HOST}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Połączono z {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, base_dir))
            client_thread.start()
            threads.append(client_thread)  # Dodanie wątku do listy
    except KeyboardInterrupt:
        logging.info("Zatrzymywanie serwera...")
    finally:
        for thread in threads:
            thread.join()  # Oczekiwanie na zakończenie wątku
        server_socket.close()

if __name__ == '__main__':
    servers = config.get("servers", [])
    for server in servers:
        port = server.get("port", 8080)
        base_dir = server.get("base_dir", './static')
        server_thread = threading.Thread(target=start_server, args=(port, base_dir))
        server_thread.start()
        threads.append(server_thread)
