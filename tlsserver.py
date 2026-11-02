import socket
import ssl

SERVER_IP = "192.168.128.50"
SERVER_PORT = 5006

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile="server.crt",
    keyfile="privateKey_S.pem"
)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)

        print(f"TLS Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            conn, addr = server.accept()

            try:
                with context.wrap_socket(conn, server_side=True) as tls_conn:
                    print(f"Secure connection from {addr}")
                    print(f"TLS version: {tls_conn.version()}")

                    while True:
                        data = tls_conn.recv(1024)

                        if not data:
                            break

                        print("Received:", data.decode())
                        tls_conn.sendall(data)

            except (ssl.SSLError, OSError) as e:
                print("Connection error:", e)

except KeyboardInterrupt:
    print("\nServer stopped.")

except OSError as e:
    print("Server error:", e)