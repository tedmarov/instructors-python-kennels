import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from locations.request import get_all_locations
from animals import *
from customers import *
from locations import *


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            print(resource, key, value)
            return ( resource, key, value )
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


    def do_GET(self):
        self._set_headers(200)

        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                    pass
                else:
                    response = f"{get_all_locations()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "customers":
                response = f"{get_customers_by_email(value)}"

        self.wfile.write(response.encode())

    def do_POST(self):
        '''Reads post request body'''
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None

        # Add a new animal to the list
        if resource == "animals":
            new_animal = create_animal(post_body)
        elif resource == "customers":
            new_animal = create_customer(post_body)
        elif resource == "locations":
            new_animal = create_animal(post_body)
        elif resource == "employees":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_animal}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        success = False

        if resource == "animals":
            success = update_animal(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())



    def do_DELETE(self):

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            success = delete_animal(id)   # True or False

            if success:
                self._set_headers(204) # SUCCESS, NO CONTENT
            else:
                self._set_headers(404) # Resource doesn't exist 200, 201, 204, 401, 403, 404, 413, 500

        # Encode the new animal and send in response
        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()