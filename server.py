import socket
import os
import logging
import ssl

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

HOST ='192.168.0.105'  
PORT = 8080
WEB_ROOT = 'www' 
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
logging.info(f"Server listening on {HOST}:{PORT}...")

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}...")

def handle_request(request_data):
    lines = request_data.split("\r\n")
    if len(lines) > 0:
        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) == 3:
            method, path, _ = parts
            if method in ["GET", "POST"]:
                return method, path

    return None, None

def generate_response(method, request_path):
    if method == "GET":
        return generate_get_response(request_path)
    elif method == "POST":
        return generate_post_response(request_path)

def generate_get_response(request_path):
    file_path = os.path.join(WEB_ROOT, request_path.lstrip("/"))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content
            return response
    else:
        return b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

def generate_post_response(request_path):
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{request_path}".encode()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)


while True:
    client_socket, client_address = server_socket.accept()
    logging.info(f"Connection from {client_address}")
    print(f"Connection from {client_address}")

    ssl_socket = context.wrap_socket(client_socket, server_side=True)

    request_data = client_socket.recv(1024).decode('utf-8')
    logging.info(f"Request: {request_data}")
    print("Request:", request_data)

    method, request_path = handle_request(request_data)
    if method and request_path:
        response = generate_response(method, request_path)
    else:
        response = b"HTTP/1.1 400 Bad Request\r\n\r\n400 Bad Request"

    client_socket.sendall(response)
    client_socket.close()
