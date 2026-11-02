import socket
import ssl

SERVER_IP = "192.168.128.50"
SERVER_PORT = 5006

context = ssl.create_default_context(
    cafile="ca.crt"
)

try:
    with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:

        with context.wrap_socket(
            sock,
            server_hostname="192.168.128.50"
        ) as tls_client:

            print("Connected securely to TLS Server")
            print("TLS version:", tls_client.version())

            while True:
                msg = input("Message (or 'exit' to quit): ")

                if msg.lower() == "exit":
                    break

                tls_client.sendall(msg.encode())

                data = tls_client.recv(1024)

                if not data:
                    print("Server disconnected.")
                    break

                print("Server replied:", data.decode())

except ssl.SSLError as e:
    print("TLS error:", e)

except OSError as e:
    print("Connection error:", e)

except KeyboardInterrupt:
    print("\nClient stopped.")