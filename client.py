import socket
import ssl

# Define the server address and port
SERVER_HOST = '192.168.0.105'  # Server's IP address or hostname
SERVER_PORT = 8080

# Paths to client certificate and private key
CLIENT_CERT_FILE = 'client.crt'
CLIENT_KEY_FILE = 'client.key'

def send_request(request):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # Load client certificate and private key
        context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)

        # Connect to the server
        ssl_socket = context.wrap_socket(client_socket, server_hostname=SERVER_HOST)
        ssl_socket.connect((SERVER_HOST, SERVER_PORT))

        # Send the request to the server
        ssl_socket.sendall(request.encode('utf-8'))

        # Receive response from the server
        response = ssl_socket.recv(1024).decode('utf-8')
        print("Response from server:", response)
    finally:
        # Close the connection
        ssl_socket.close()

if __name__ == "__main__":
    try:
        while True:
            # Get the input URL from the user
            url = input("Enter URL (e.g., /index.html): ")
            
            # Choose the request method (GET or POST)
            method = input("Enter request method (GET or POST): ").upper()
            
            if method == "GET":
                # Prepare the HTTP GET request
                request = f"GET {url} HTTP/1.1\r\nHost: localhost\r\n\r\n"
            elif method == "POST":
                # Prepare the HTTP POST request with sample data
                data = input("Enter data to POST: ")
                request = f"POST {url} HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(data)}\r\n\r\n{data}"
            else:
                print("Invalid request method. Please enter GET or POST.")
                continue

            # Send the request to the server and print the response
            send_request(request)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
