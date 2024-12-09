from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"[ERROR] Could not determine local IP: {e}")
        return "127.0.0.1"

class FileHandler(BaseHTTPRequestHandler):
    file_path = r""  # Replace with your file path
    file_name = os.path.basename(file_path)

    def do_GET(self):
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{self.file_name}"')
                self.end_headers()

                with open(self.file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

def run_server(port=8080):
    ip = get_local_ip()
    server_address = (ip, port)
    httpd = HTTPServer(server_address, FileHandler)
    print(f"Serving file '{FileHandler.file_name}' at http://{ip}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
