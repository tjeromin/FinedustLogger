from wsgiref.simple_server import make_server, demo_app
from app import app as application

with make_server('', 5000, demo_app) as httpd:
    print("Serving HTTP on port 5000...")

    # Respond to requests until process is killed
    httpd.serve_forever()
