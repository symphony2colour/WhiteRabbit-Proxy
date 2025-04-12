import hmac
import hashlib
import json
import logging
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import time

# Constants
SECRET = "3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"
WEBHOOK_URL = "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d"

class Payload:
    def __init__(self, campaign_id, email, message):
        self.campaign_id = campaign_id
        self.email = email
        self.message = message

    def to_dict(self):
        return {
            "campaign_id": self.campaign_id,
            "email": self.email,
            "message": self.message
        }

def calculate_hmac(payload):
    payload_json = json.dumps(payload.to_dict(), separators=(',', ':'))
    hmac_object = hmac.new(SECRET.encode(), payload_json.encode(), hashlib.sha256)
    return hmac_object.hexdigest()

def log_request(handler):
    client_ip = handler.client_address[0]
    method = handler.command
    uri = handler.path
    protocol = handler.protocol_version
    logging.info(f'{client_ip} - - "{method} {uri} {protocol}" 200 -')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log_request(self)
        query_params = parse_qs(self.path.split('?', 1)[-1])
        email = query_params.get('query', [None])[0]

        if not email:
            self.send_error(400, '{"error": "Missing \'query\' query parameter for email"}')
            return

        payload = Payload(campaign_id=1, email=email, message="Clicked Link")
        signature = calculate_hmac(payload)

        try:
            headers = {
                "Content-Type": "application/json",
                "x-gophish-signature": "hmac=" + signature
            }
            response = requests.post(WEBHOOK_URL, json=payload.to_dict(), headers=headers, timeout=10)
            response.raise_for_status()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.content)
        except requests.exceptions.RequestException as e:
            self.send_error(500, f'{{"error": "{str(e)}"}}')

    def log_message(self, format, *args):
        return  # silence default HTTPServer logging

def main():
    logging.basicConfig(level=logging.INFO)
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.timeout = 1  # allow checking every 1 second

    logging.info("Starting server on http://localhost:10000")
    try:
        while True:
            httpd.handle_request()  # handles one request at a time
    except KeyboardInterrupt:
        logging.info("Received Ctrl+C, shutting down server...")
    finally:
        httpd.server_close()
        logging.info("Server has shut down cleanly.")

if __name__ == "__main__":
    main()

