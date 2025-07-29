import socket
import xml.etree.ElementTree as ET

class TCPClientError(Exception):
    """Custom exception for TCP client errors."""
    pass

class TCPClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        """Establish a connection to the server."""
        if self.client_socket:
            raise ConnectionError("Already connected.")
        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5)  # Set a timeout for connection attempts
            self.client_socket.connect((self.host, self.port))
        except socket.timeout:
            raise TCPClientError(f"Connection to {self.host}:{self.port} timed out.")
        except socket.error as e:
            raise TCPClientError(f"Connection error: {e}")

    def send_message(self, message: str):
        """Send a string message to the server."""
        if not self.client_socket:
            raise ConnectionError("Not connected.")
        
        # Encode the message to bytes before sending
        self.client_socket.sendall(message.encode('utf-8'))

    def receive_message(self) -> str:
        """Receives data from a TCP socket until a valid XML message is formed."""
        data = bytearray()
    
        while True:
            try:
                chunk = self.client_socket.recv(1024)  # Read in chunks
                if not chunk:
                    raise ConnectionError("Connection lost while receiving XML.")
            
                data.extend(chunk)
            
                # Try parsing the XML to check if it's complete
                xml_str = data.decode('utf-8')
                ET.fromstring(xml_str)  # This will raise an error if XML is incomplete
            
                return xml_str  # If parsing succeeds, return valid XML

            except ET.ParseError:
                # If XML is not valid yet, continue receiving
                continue
            except socket.error as e:
                raise ConnectionError(f"Socket error while receiving XML: {e}")

    def close(self):
        """Close the connection."""
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
